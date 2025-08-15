---
title: Tighter HTCondor and Kubernetes interplay for better glideins
presenter: Igor Sfiligoi and Jamie Frey
event: HTC25
date: '2025-06-05'
publish_on:
- path
- osg
- htcondor
description: HTCondor is the leading system for building a dynamic overlay batch scheduling
  system on resources managed by any scheduling system, by means of glideins. One
  fundamental property of these setups is the use of late binding of containerized
  user workloads. From a resource provider point of view, a compute resource is thus
  claimed before the user container image is selected. Kubernetes allows for both
  multi-container requests and dynamic updates to the container image being used.
  In this talk we show how HTCondor can exploit these features to both increase the
  effectiveness and the security of gildeins running on top of Kubernetes-managed
  resources.
image: null
keywords:
- Admin Tools
- HTCondor
youtube_video_id: ZfNdeV6LwAA
links:
- name: Public slides
  value: https://agenda.hep.wisc.edu/event/2297/contributions/33819/
---
