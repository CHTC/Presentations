#!/usr/bin/env python3
"""Generate presentation markdown stubs from an Indico event.

Uses the Indico HTTP export API (``/export/event/<id>.json``) rather than
scraping HTML.  Nothing is downloaded locally: each generated file links back
to the material hosted on the Indico instance.

Contributions without any attached material are skipped, since there is
nothing to link to.

Examples
--------
    # preview what would be written
    .scripts/scrape_indico_website.py https://indico.cern.ch/event/1659396/ --dry-run

    # write the files, tagging them for the HTCondor site
    .scripts/scrape_indico_website.py https://indico.cern.ch/event/1659396/ \
        --event "European HTCondor Workshop 2026" \
        --publish-on htcondor --keyword HTCondor
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

USER_AGENT = "CHTC-presentations-indico-import/1.0 (+https://github.com/CHTC)"

# Attachment content types that we are willing to call "slides".
SLIDE_EXTENSIONS = {
    ".pdf": "PDF",
    ".pptx": "PPTX",
    ".ppt": "PPT",
    ".odp": "ODP",
    ".key": "Keynote",
}


# --------------------------------------------------------------------------
# Indico API
# --------------------------------------------------------------------------

def parse_event_url(raw: str) -> tuple[str, str]:
    """Return ``(base_url, event_id)`` for an Indico event/contribution URL.

    Accepts a bare event id only when --base-url is supplied by the caller.
    """
    parsed = urllib.parse.urlparse(raw)
    if not parsed.scheme:
        raise ValueError(f"not a URL: {raw!r}")
    match = re.search(r"/event/(\d+)", parsed.path)
    if not match:
        raise ValueError(f"could not find an event id in {raw!r}")
    base = f"{parsed.scheme}://{parsed.netloc}"
    return base, match.group(1)


def ssl_context() -> ssl.SSLContext | None:
    """Fall back to certifi's bundle on interpreters with no CA store.

    Several python.org macOS builds ship without running ``Install Certificates``,
    which makes every HTTPS request fail verification.
    """
    try:
        import certifi
    except ImportError:
        return None
    return ssl.create_default_context(cafile=certifi.where())


def fetch_event(base_url: str, event_id: str, token: str | None) -> dict:
    """Pull the event plus its contributions from the Indico export API."""
    query = urllib.parse.urlencode({"detail": "subcontributions", "pretty": "no"})
    url = f"{base_url}/export/event/{event_id}.json?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    def get(context=None):
        with urllib.request.urlopen(request, timeout=60, context=context) as response:
            return json.load(response)

    try:
        try:
            payload = get()
        except urllib.error.URLError as exc:
            if not isinstance(exc.reason, ssl.SSLCertVerificationError):
                raise
            context = ssl_context()
            if context is None:
                raise SystemExit(
                    f"TLS verification failed for {url} and certifi is not installed.\n"
                    "Run the 'Install Certificates.command' that ships with your Python, "
                    "or 'pip install certifi'."
                ) from exc
            print("note: system CA store unusable, falling back to certifi", file=sys.stderr)
            payload = get(context)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Indico returned HTTP {exc.code} for {url}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"could not reach {url}: {exc.reason}") from exc

    results = payload.get("results") or []
    if not results:
        raise SystemExit(f"no event data returned for event {event_id}")
    return results[0]


def iter_talks(event: dict):
    """Yield every contribution and subcontribution of the event."""
    for contribution in event.get("contributions") or []:
        yield contribution
        for sub in contribution.get("subContributions") or []:
            # Subcontributions inherit the parent's schedule and URL base.
            sub = dict(sub)
            sub.setdefault("startDate", contribution.get("startDate"))
            sub.setdefault("url", contribution.get("url"))
            yield sub


# --------------------------------------------------------------------------
# Field extraction
# --------------------------------------------------------------------------

class _TextExtractor(HTMLParser):
    """Collapse an Indico HTML description into readable plain text."""

    BLOCK_TAGS = {
        "p", "div", "br", "li", "ul", "ol", "tr", "table",
        "h1", "h2", "h3", "h4", "h5", "h6", "blockquote",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")
        if tag == "li":
            self.parts.append("- ")

    def handle_endtag(self, tag):
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)

    def text(self) -> str:
        return "".join(self.parts)


def html_to_text(raw: str | None) -> str:
    """Normalise an Indico description (HTML or plain text) into paragraphs."""
    if not raw:
        return ""
    if re.search(r"<[a-zA-Z/][^>]*>", raw):
        extractor = _TextExtractor()
        extractor.feed(raw)
        text = extractor.text()
    else:
        text = html.unescape(raw)

    text = text.replace("\xa0", " ").replace("\r\n", "\n").replace("\r", "\n")
    # Indico descriptions are frequently hard-wrapped mid-sentence; unwrap
    # single newlines but keep paragraph breaks.
    text = re.sub(r"(?<!\n)\n(?!\n)(?!- )", " ", text)
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def tidy_name(part: str) -> str:
    """Indico stores some names in all caps; make them match the repo style."""
    if part.isupper() and len(part) > 1:
        return part.title()
    return part


def speaker_names(talk: dict) -> list[str]:
    people = talk.get("speakers") or talk.get("primaryauthors") or []
    names = []
    for person in people:
        first = tidy_name((person.get("first_name") or "").strip())
        last = tidy_name((person.get("last_name") or "").strip())
        full = " ".join(filter(None, (first, last))) or (person.get("fullName") or "").strip()
        if full and full not in names:
            names.append(full)
    return names


def attachments(talk: dict) -> list[dict]:
    found = []
    for folder in talk.get("folders") or []:
        for attachment in folder.get("attachments") or []:
            if attachment.get("is_protected"):
                continue
            found.append(attachment)
    return found


def link_name(attachment: dict, seen: set[str]) -> str:
    """Pick a human-readable label for an attachment link."""
    title = (attachment.get("title") or "").strip()
    filename = (attachment.get("filename") or "").strip()
    stem, extension = os.path.splitext(filename or title)
    label = title

    # When the title is just the file name, describe the material instead.
    if filename and title in (filename, stem) and extension.lower() in SLIDE_EXTENSIONS:
        label = f"Presentation Slides ({SLIDE_EXTENSIONS[extension.lower()]})"
    elif extension.lower() in SLIDE_EXTENSIONS and title.endswith(extension):
        label = stem

    label = label or "Presentation Material"
    if label in seen:
        suffix = 2
        while f"{label} ({suffix})" in seen:
            suffix += 1
        label = f"{label} ({suffix})"
    seen.add(label)
    return label


def build_links(talk: dict) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    seen: set[str] = set()
    for attachment in attachments(talk):
        url = attachment.get("link_url") or attachment.get("download_url")
        if not url:
            continue
        links.append({"name": link_name(attachment, seen), "value": url})
    contribution_url = talk.get("url")
    if contribution_url:
        links.append({"name": "Indico Agenda", "value": contribution_url})
    return links


def slugify(title: str, words: int = 4) -> str:
    """Match the repo's existing ``YYYY-MM-DD-first-four-words`` convention."""
    cleaned = re.sub(r"[^a-z0-9\s]", "", title.lower().replace("-", " "))
    slug = "-".join(cleaned.split()[:words])
    return slug or "untitled"


def talk_date(talk: dict) -> str | None:
    start = talk.get("startDate") or {}
    return start.get("date")


# --------------------------------------------------------------------------
# YAML front matter
# --------------------------------------------------------------------------

def yaml_double_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_block(key: str, text: str, indent: str = "  ") -> str:
    body = "\n".join(indent + line if line else "" for line in text.split("\n"))
    return f"{key}: |\n{body}"


def render_front_matter(record: dict) -> str:
    lines = ["---"]
    lines.append(f"title: {yaml_double_quote(record['title'])}")
    presenter = record["presenter"]
    lines.append(f"presenter: {yaml_double_quote(presenter) if presenter else 'null'}")
    lines.append(f"event: {yaml_double_quote(record['event'])}")
    lines.append(f"date: '{record['date']}'")

    if record["publish_on"]:
        lines.append("publish_on:")
        lines.extend(f"  - {target}" for target in record["publish_on"])
    else:
        lines.append("publish_on: []")

    if record["description"]:
        lines.append(yaml_block("description", record["description"]))
    else:
        lines.append("description: null")

    lines.append("image: null")

    if record["keywords"]:
        lines.append("keywords:")
        lines.extend(f"  - {keyword}" for keyword in record["keywords"])
    else:
        lines.append("keywords: []")

    lines.append("youtube_video_id: null")

    if record["links"]:
        lines.append("links:")
        for link in record["links"]:
            lines.append(f"  - name: {yaml_double_quote(link['name'])}")
            lines.append(f"    value: {link['value']}")
    else:
        lines.append("links: null")

    lines.append("---")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def build_record(talk: dict, event_name: str, publish_on: list[str],
                 extra_keywords: list[str], keyword_map: dict[str, str],
                 use_tracks: bool) -> dict | None:
    title = (talk.get("title") or "").strip()
    date = talk_date(talk)
    if not title or not date:
        return None

    links = build_links(talk)
    # The Indico agenda link alone is not material worth publishing.
    if not any(link["name"] != "Indico Agenda" for link in links):
        return None

    from_indico = [k.strip() for k in (talk.get("keywords") or []) if k.strip()]
    if use_tracks and talk.get("track"):
        from_indico.append(talk["track"].strip())

    keywords = []
    for keyword in from_indico:
        mapped = keyword_map.get(keyword.casefold(), keyword)
        # An empty mapping target drops the keyword entirely.
        keywords.extend(part for part in mapped.split("|") if part)
    keywords = list(dict.fromkeys(keywords + extra_keywords))

    return {
        "title": title,
        "presenter": ", ".join(speaker_names(talk)),
        "event": event_name,
        "date": date,
        "publish_on": publish_on,
        "description": html_to_text(talk.get("description")),
        "keywords": keywords,
        "links": links,
        "filename": f"{date}-{slugify(title)}.md",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create presentation markdown files from an Indico event via its API.",
    )
    parser.add_argument("event_url", help="Indico event or contribution URL")
    parser.add_argument("-o", "--output", default=".",
                        help="directory to write the markdown files into (default: current directory)")
    parser.add_argument("--event", dest="event_name",
                        help="value for the 'event' front matter field (default: the Indico event title)")
    parser.add_argument("--publish-on", nargs="*", default=[], metavar="SITE",
                        help="sites to list under publish_on, e.g. path osg htcondor")
    parser.add_argument("--keyword", action="append", default=[], metavar="KEYWORD",
                        help="extra keyword to add to every presentation (repeatable)")
    parser.add_argument("--keyword-map", action="append", default=[], metavar="FROM=TO",
                        help="rewrite an Indico keyword or track, e.g. 'Condor and AI=AI'. "
                             "Use 'A|B' to expand into several, or 'FROM=' to drop it. "
                             "Repeatable; matching is case-insensitive.")
    parser.add_argument("--no-track-keyword", dest="use_tracks", action="store_false",
                        help="do not turn the Indico track name into a keyword")
    parser.add_argument("--overwrite", action="store_true",
                        help="replace files that already exist (default: leave them alone)")
    parser.add_argument("--dry-run", action="store_true",
                        help="report what would be written without touching the filesystem")
    parser.add_argument("--token", default=os.environ.get("INDICO_API_TOKEN"),
                        help="Indico API token for non-public events (or set INDICO_API_TOKEN)")
    args = parser.parse_args(argv)

    try:
        base_url, event_id = parse_event_url(args.event_url)
    except ValueError as exc:
        parser.error(str(exc))

    keyword_map = {}
    for mapping in args.keyword_map:
        if "=" not in mapping:
            parser.error(f"--keyword-map expects FROM=TO, got {mapping!r}")
        source, target = mapping.split("=", 1)
        keyword_map[source.strip().casefold()] = target.strip()

    event = fetch_event(base_url, event_id, args.token)
    event_name = args.event_name or (event.get("title") or f"Indico event {event_id}").strip()
    print(f"Event {event_id}: {event.get('title')} ({base_url})", file=sys.stderr)

    written = skipped_existing = skipped_no_material = 0
    for talk in iter_talks(event):
        record = build_record(talk, event_name, args.publish_on, args.keyword,
                              keyword_map, args.use_tracks)
        if record is None:
            skipped_no_material += 1
            title = (talk.get("title") or "<untitled>").strip()
            print(f"  skip (no material): {title}", file=sys.stderr)
            continue

        path = os.path.join(args.output, record["filename"])
        if os.path.exists(path) and not args.overwrite:
            skipped_existing += 1
            print(f"  skip (exists): {record['filename']}", file=sys.stderr)
            continue

        if args.dry_run:
            print(f"  would write: {record['filename']}", file=sys.stderr)
        else:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(render_front_matter(record))
            print(f"  wrote: {record['filename']}", file=sys.stderr)
        written += 1

    print(
        f"\n{written} presentation(s) {'to write' if args.dry_run else 'written'}; "
        f"{skipped_no_material} skipped with no material; "
        f"{skipped_existing} already present.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
