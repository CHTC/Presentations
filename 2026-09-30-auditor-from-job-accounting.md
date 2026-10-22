---
title: "AUDITOR: From Job Accounting to Sustainable Computing in HTC"
presenter: "Dirk Sammel"
event: "European HTCondor Workshop 2026"
date: '2026-09-30'
publish_on: []
description: |
  In the realm of High Throughput Computing (HTC), managing and processing large volumes of accounting data across diverse environments and use cases presents significant challenges. AUDITOR addresses this issue by providing a flexible framework for building accounting pipelines that can adapt to a wide range of needs. AUDITOR is a modular framework for collecting, storing, and processing accounting data from heterogeneous computing resources. It provides centralized storage for accounting records and enables data exchange through a REST interface. Collectors retrieve accounting data from various sources and submit it to AUDITOR, while plugins access the stored data for subsequent processing. Its modular architecture allows collectors and plugins to be adapted to specific use cases and environments, providing a flexible and extensible approach to accounting data management. For HTC, the HTCondor collector retrieves job ClassAds from HTCondor and converts them into the standardized AUDITOR record structure. This presentation outlines the architecture of the AUDITOR accounting ecosystem and demonstrates its existing accounting pipelines. Furthermore, it describes how the AUDITOR ecosystem is currently being expanded to include new metrics such as the power consumption and carbon footprint per job, allowing for the quantification of environmentally sustainable computing.
image:
  path: https://raw.githubusercontent.com/CHTC/presentations/main/images/European-Condor-Week-2026-Images/EuropeanCondorWeek2026-Sammel.png
keywords:
  - Admin Tools
  - HTCondor
youtube_video_id: null
links:
  - name: "Presentation Slides (PDF)"
    value: https://indico.cern.ch/event/1659396/contributions/7273021/attachments/3353342/6013092/htcondor_2026_dirksammel.pdf
  - name: "Indico Agenda"
    value: https://indico.cern.ch/event/1659396/contributions/7273021/
---
