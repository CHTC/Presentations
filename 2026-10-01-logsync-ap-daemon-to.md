---
title: "Logsync - AP daemon to offload user log writes"
presenter: "Panagiotis Gkonis"
event: "European HTCondor Workshop 2026"
date: '2026-10-01'
publish_on: []
description: |
  At CERN, we operate a few tens of HTCondor APs to server thousands of users doing remote job submission. The users' log files are written synchronously by the AP to their destinations of choice. This has often been a cause of degraded AP responsiveness, as they prefer to write the logs to shared file systems, whose performance is impacted by external factors, such as the jobs themselves.

  Over the past months we have been developing a daemon that is able to write these log files independently from the main schedd process, which instead stages them to a spool directory on the machine's much more stable local storage. In our presentation, we share the high level overview of the system, some interesting low-level details with regards to its durability, as well as its integration with HTCondor. We will also present operational anecdotes and metrics collected so far, during our gradual production deployment.
image:
  path: https://raw.githubusercontent.com/CHTC/presentations/main/images/European-Condor-Week-2026-Images/EuropeanCondorWeek2026-Gkonis.png
keywords:
  - Admin Tools
  - HTCondor
youtube_video_id: null
links:
  - name: "Logsync (mirrored) Repository"
    value: https://github.com/cernops/logsync
  - name: "Presentation Slides (PDF)"
    value: https://indico.cern.ch/event/1659396/contributions/7268092/attachments/3351629/6013235/logsync.pdf
  - name: "Indico Agenda"
    value: https://indico.cern.ch/event/1659396/contributions/7268092/
---
