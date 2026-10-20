---
title: "The Facility Is the Context: Building an MCP Platform for Scientific Computing"
presenter: "Giordon Holtsberg Stark"
event: "European HTCondor Workshop 2026"
date: '2026-10-01'
publish_on: []
description: |
  Large language model agents are becoming useful for software development and scientific analysis, but making them useful on shared computing infrastructure requires more than the model itself. Agents need reliable access to the software, data, workflows, and identities that researchers already use.

  This talk introduces the Model Context Protocol (MCP) as a practical interface between AI agents and scientific software. I will briefly discuss how MCP can expose existing Python libraries, databases, experiment services, Jupyter environments, and batch systems, and then show how these pieces come together in an MCP platform developed for the UChicago Analysis Facility.

  The platform provides a common gateway for MCP services while handling authentication, authorization, and credential brokering separately from the individual services. This allows agents to work with resources such as Rucio, Jupyter, filesystems, and HTCondor without directly handling users' long-lived credentials.

  Using examples from the ATLAS Analysis Facility and work extending this approach across experiments, I will discuss what works today, the infrastructure challenges that remain, and what an MCP-based approach could mean for making agentic computing portable across scientific facilities.
image: null
keywords:
  - AI
  - HTCondor
youtube_video_id: null
links:
  - name: "Demo Prompt"
    value: https://gist.github.com/kratsg/6956cf796e269c5d13cb2835e72ee664
  - name: "Slides (reveal.js)"
    value: https://kratsg.github.io/2026-10-01-htcondor-eu/#/title
  - name: "Indico Agenda"
    value: https://indico.cern.ch/event/1659396/contributions/7273024/
---
