import csv
import yaml
import re
import os

def shorten_word_list(word_list, max_length=4):
    """Shorten a list of words to a maximum length."""
    return word_list[:max_length] if len(word_list) > max_length else word_list

def create_slug(date, title):
    """Create a URL-friendly slug from the title."""
    friendly_title: str = re.sub(r'[^a-zA-Z0-9 -]','',title.lower()).replace(' ', '-')
    print(friendly_title)
    friendly_title = '-'.join(shorten_word_list(friendly_title.split('-')))  # Limit to first 4 words
    return date + '-' + friendly_title

def split_by_pipe(value):
    """Split a string by pipe character and return a list."""
    return [v.strip() for v in value.strip().split('|') if len(v) != 0] if value else []

def convert_csv_to_yml(csv_file):
    written_files = []

    with open(csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]

        for row in data:
            title = row['Title'].strip()
            presenter_name = row['Presenter Name'].strip()
            event = row['Event'].strip()
            presentation_date = row['Presentation Date (YYYY-MM-DD'].strip()
            publish_on = split_by_pipe(row['Publish On: path|osg|chtc|htcondor|pelican'])
            description = row['Description'].strip()
            image_url = row['Image URL'].strip()
            alt_image = row['Alt Image'].strip()
            keywords = split_by_pipe(row['Keywords'])
            video_id_or_maybe_url = row['Youtube video ID'].split()
            slides_link = row['Public slides link'].strip()

            if not title:
                raise ValueError("Title is required in each row.")
            if not presenter_name:
                print(f"Warning: No presenter name for title '{title}'")
                continue
            if not event:
                print(f"Warning: No event for title '{title}'")
                continue
            if not presentation_date:
                print(f"Warning: No presentation date for title '{title}'")
                continue
            if len(publish_on) == 0:
                print(f"Warning: No publish path for title '{title}'")
                continue
            if not description:
                print(f"Warning: No description for title '{title}'")
                continue
            if not image_url:
                # print(f"Warning: No image URL for title '{title}'")
                # continue
                pass
            if not alt_image:
                # print(f"Warning: No alt image for title '{title}'")
                # continue
                pass
            if not video_id_or_maybe_url:
                # print(f"Warning: No video ID for title '{title}'")
                continue
            if not slides_link:
                print(f"Warning: No slides link for title '{title}'")
                continue

            slug = create_slug(presentation_date, title)
            video_id = re.sub(r'https?:\/\/(?:www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)', '', video_id_or_maybe_url[0])
            video_data = {
                'title': title,
                'presenter': presenter_name,
                'event': event,
                'date': presentation_date,
                'publish_on': publish_on,
                'description': description,
                'image': {
                    'path': image_url,
                    'alt': alt_image if alt_image else None
                } if (image_url) else None,
                'keywords': keywords if keywords else None,
                'youtube_video_id': video_id,
                'links': [
                    {
                        'name': 'Public slides',
                        'value': slides_link
                    }
                ]
            }

            # Write to YAML file
            yaml_filename = f"{slug}.yml"

            with open(yaml_filename, 'w', encoding='utf-8') as yaml_file:
                yaml.dump(video_data, yaml_file, allow_unicode=True, default_flow_style=False, sort_keys=False)
            written_files.append(yaml_filename)

    # if written files contains duplicate names, print a warning
    if len(written_files) != len(set(written_files)):
        print("Warning: Some files were written with duplicate names. Please check the following files:")
        duplicates = set([f for f in written_files if written_files.count(f) > 1])
        for dup in duplicates:
            print(dup)
    
    return written_files

def convert_yml_to_md(yml_files, delete=False):
    for yml_file in yml_files:
        data = None
        with open(yml_file, 'r', encoding='utf-8') as file:
            data = file.read()
        data = "---\n" + data.strip() + "\n---\n"

        md_filename = re.sub(r'\.yml$', '.md', yml_file)
        with open(md_filename, 'w', encoding='utf-8') as md_file:
            md_file.write(data)

        print(f"Converted {yml_file} to {md_filename}")
    
    if delete:
        for yml_file in yml_files:
            try:
                os.remove(yml_file)
                print(f"Deleted {yml_file}")
            except OSError as e:
                print(f"Error deleting {yml_file}: {e}")

if __name__ == "__main__":
    converted = convert_csv_to_yml('Video Spreadsheet  - Sheet1.csv')
    convert_yml_to_md(converted, delete=True)
    print("Conversion completed.")