---
title: "Evolving the CMS Submission Infrastructure"
presenter: "Marco Mascheroni"
event: "European HTCondor Workshop 2026"
date: '2026-10-01'
publish_on: []
description: |
  The CMS Submission Infrastructure (SI), based on HTCondor and GlideinWMS, operates a federated pool of resources, integrated from WLCG, HPC and cloud providers, supporting CMS offline computing needs. As CMS prepares for the High-Luminosity LHC (HL-LHC) phase, the infrastructure must continue evolving to support increasing resource scale and heterogeinity, while maintaining the stability, flexibility, and efficiency required for large-scale distributed computing.

  This contribution presents recent developments in the CMS SI, focused on improving resource utilization and scheduling efficiency. In particular, we discuss the deployment of high-IO auxiliary slots to reduce slot fragmentation caused by bursts of short single-core workloads, and the introduction of controlled pilot overloading techniques aimed at recovering otherwise unused CPU cycles from inefficient or I/O-bound payloads. These strategies have shown systematic improvements in overall CPU efficiency while preserving stable SI operations..

  The talk will also cover the continued evolution of CMS resource integration strategies for heterogeneous computing environments, including GPUs, ARM processors, and HPC facilities, together with broader CMS plans for the next-generation Workflow Management system designed for HL-LHC-scale workflows and increasingly dynamic computing resources. Together, these developments represent important steps toward a more scalable, sustainable, and efficient CMS computing infrastructure, as required by the HL-LHC program.
image:
  path: https://raw.githubusercontent.com/CHTC/presentations/main/images/European-Condor-Week-2026-Images/EuropeanCondorWeek2026-Mascheroni.png
keywords:
  - HTCondor
youtube_video_id: null
links:
  - name: "Presentation Slides (PDF)"
    value: https://indico.cern.ch/event/1659396/contributions/7296979/attachments/3353798/6014110/20261001%20CMS%20SI%20meets%20the%20DiracX%20TS.pdf
  - name: "Indico Agenda"
    value: https://indico.cern.ch/event/1659396/contributions/7296979/
---
