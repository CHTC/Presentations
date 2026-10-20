---
title: "INK: Interactive Analysis Workbench on HTCondor"
presenter: "Jingyan Shi"
event: "European HTCondor Workshop 2026"
date: '2026-09-29'
publish_on: []
description: |
  INK (Interactive aNalysis worKbench) is a web-based interactive computing platform developed at the IHEP Computing Center, giving physicists browser-accessible interactive sessions — Jupyter, VS Code, ROOT, VNC, and remote desktops — transparently backed by our production HTCondor and Slurm clusters. By abstracting job submission, resource allocation, connection management, and authentication behind a unified web interface, INK lets users launch and connect to interactive workloads with a single click, without writing submit files or handling HTCondor directly, while still benefiting from the scheduling and resource management of the batch system underneath.

  Key features of INK include a pluggable job-type framework that makes new interactive applications easy to add, a session-based reverse proxy for secure browser access to running jobs, and a portable, site-agnostic core with IHEP-specific logic isolated as plugins.

  Building on this platform, we have been exploring how AI — large language models in particular — can be delivered on HTCondor. This talk presents our integration of AI coding assistants (OpenCode, OpenChamber) as first-class interactive job types, along with the design choices for running LLM-based tools securely on shared clusters. We will share the architecture, our experience, and the practical challenges of bringing AI applications into a production HTCondor environment.
image: null
keywords:
  - HTCondor
youtube_video_id: null
links:
  - name: "Presentation Slides (PDF)"
    value: https://indico.cern.ch/event/1659396/contributions/7264627/attachments/3352355/6011138/INK-Lyon-HTCondor26-v3.pdf
  - name: "Presentation Slides (PPTX)"
    value: https://indico.cern.ch/event/1659396/contributions/7264627/attachments/3352355/6011137/INK-Lyon-HTCondor26-v3.pptx
  - name: "Indico Agenda"
    value: https://indico.cern.ch/event/1659396/contributions/7264627/
---
