---
title: "JobLens: Toward Job-Native Observability for HTCondor Clusters"
presenter: "Zhenyuan Wang"
event: "European HTCondor Workshop 2026"
date: '2026-09-30'
publish_on: []
description: |
  Modern HTCondor deployments predominantly rely on node-centric monitoring paradigms, whereas users and operators typically reason about performance anomalies, failures, and resource efficiency at the granularity of individual jobs. To bridge this semantic gap, we present JobLens, a lightweight, job-native observability framework that organizes runtime metrics and system events around scheduler-visible jobs rather than isolated machines. Its architecture integrates eBPF-based job discovery, rule-driven job capture, hot-pluggable collectors, and a streaming data pipeline to gather CPU, memory, I/O, network, and system-level signals with minimal overhead in production environments.

  We envision JobLens evolving from a passive monitoring tool into an observation-driven runtime intelligence layer for HTCondor clusters. By correlating scheduler decisions, hardware locality, and process–resource interactions, JobLens establishes a foundation for fine-grained job-level diagnosis, power attribution, workload characterization, and feedback-aware scheduling. This paradigm shifts cluster observability beyond post-hoc metric inspection toward a continuously updated digital representation of job execution dynamics—from matching and dispatching to runtime behavior.
image: null
keywords:
  - Admin Tools
  - HTCondor
youtube_video_id: null
links:
  - name: "JobLens_ CondorWorkshop_v4"
    value: https://indico.cern.ch/event/1659396/contributions/7264628/attachments/3353050/6012865/JobLens_%20CondorWorkshop_v4.pdf
  - name: "Indico Agenda"
    value: https://indico.cern.ch/event/1659396/contributions/7264628/
---
