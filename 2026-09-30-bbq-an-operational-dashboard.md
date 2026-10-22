---
title: "BBQ: an Operational Dashboard for HTCondor and Slurm Clusters"
presenter: "Guillaume Cochard"
event: "European HTCondor Workshop 2026"
date: '2026-09-30'
publish_on: []
description: |
  Monitoring a computing cluster requires more than infrastructure metrics and alerting. While tools such as Nagios, Prometheus and Grafana provide valuable information about system health and resource usage, they often lack the application-level view required for day-to-day cluster administration. Understanding what jobs are running, how resources are being used, or quickly correlating worker state with scheduler information typically requires querying multiple systems.

  To address this need, we developed BBQ (Beautiful Batch Query), an internal web application designed to provide a unified operational view of our HTCondor and Slurm clusters. BBQ continuously collects information from HTCondor through its Python bindings and enriches it with data from various infrastructure services such as our CMDB and PuppetDB. The resulting database contains up-to-date information about running and completed jobs, workers, and cluster configuration.

  The web interface allows administrators to explore job and worker details, visualize usage statistics, and correlate information that would otherwise be scattered across multiple tools or command-lines results. While some dashboards overlap with traditional monitoring solutions, BBQ focuses on operational workflows and scheduler-specific information rather than infrastructure metrics alone. The same interface also exposes our Slurm cluster, for which additional information and management features are available.

  This presentation will introduce the architecture of BBQ, discuss the design choices behind the data collection pipeline, and demonstrate how the tool simplifies daily administration of production clusters comprising several hundred compute nodes. We will also present ongoing work toward integrating administrative actions directly into the interface, such as draining nodes or temporarily blocking users.
image:
  path: https://raw.githubusercontent.com/CHTC/presentations/main/images/European-Condor-Week-2026-Images/EuropeanCondorWeek2026-Cochard.png
keywords:
  - Admin Tools
  - HTCondor
youtube_video_id: null
links:
  - name: "Presentation Slides (PDF)"
    value: https://indico.cern.ch/event/1659396/contributions/7264629/attachments/3353336/6013080/bbq.pdf
  - name: "Indico Agenda"
    value: https://indico.cern.ch/event/1659396/contributions/7264629/
---
