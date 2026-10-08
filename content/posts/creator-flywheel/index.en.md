---
title: "The Creator Flywheel: Notes on the Creation Problem"
date: 2026-08-25
summary: "Turning viewers into creators, then growing creators into top creators: one flywheel, two engines, and three levers for thinking about where modeling fits in the creation problem on a short-video platform."
label: "Notes"
tags: ["Creator Ecosystem", "Creation", "Recommender Systems"]
math: false
mermaid: true
translationKey: "creator-flywheel"
ai_assisted: true
ai_note: "The ideas here are my own, from a hand-drawn sketch; the write-up was AI-assisted."
---

> In one line: **the distribution system powers the "distribution loop"; content/topic modeling and inspiration modeling power "creator growth". They are the flywheel's two engines.**

## 1. The flywheel

```mermaid
flowchart LR
    C["Viewer"] -->|"break the ice"| F["First-time creator"]
    F -->|"grow"| T["Top creator"]
    T -->|"produce"| H["Top content / breakouts"]
    H -->|"distribute back"| C
    H -.->|"inspire"| F
    H -.->|"inspire"| T
```

**Four nodes, one closed loop:**

| Step | Conversion | Engine |
|---|---|---|
| Viewer → first-time creator | Break the ice, build a creation habit | **Creation-propensity modeling** (entry) |
| First-time creator → top creator | Settle on topics, a niche and a fan base; keep growing | **Content/topic modeling · inspiration modeling** (growth) |
| Top creator → top content / breakouts | Produce top content and breakouts | — |
| Top content → viewers | Good content is distributed back, closing the loop | **Distribution & search system** (consumption side) |

> The two dashed arrows are the inspire loop: top content and breakouts in turn **spark first-time and top creators to create more actively**. It is not part of the linear main loop; it is a "re-creation" feedback that runs through the whole flywheel.

## 2. The two engines

```mermaid
flowchart TB
    subgraph EA["Engine A · creator growth (creation side)"]
        direction TB
        A1["Content / topic modeling"] --> A2["Inspiration modeling"] --> A3["First-time creator → top creator"]
    end
    subgraph EB["Engine B · distribution loop (consumption side)"]
        direction TB
        B1["Distribution & search system"] --> B2["Top content / breakouts sent back to viewers"] --> B3["Loop closes: more viewing, more new creators"]
    end
```

- **Engine A (growth)**: helps first-time creators find topics, gives them inspiration, and pushes them toward the top. It decides **how fast** the flywheel spins.
- **Engine B (distribution)**: gets good content to viewers and pulls in new creators. It decides **whether the flywheel spins at all**.

## 3. Three levers for growing creators

This is Engine A in detail. For content/topic modeling and inspiration modeling to actually help creators, it comes down to the three things below, and much of it is delivered through the distribution and search system.

```mermaid
flowchart LR
    CR["Creator"] --> I["Inspiration"]
    CR --> Q["Quick feedback"]
    CR --> R["Role models"]
    I --> I1["Related topics"]
    I --> I2["Better content on the same topic"]
    I --> I3["New information"]
    Q --> Q1["Fast likes / comments / follows<br/>after cold-start exposure"]
    R --> R1["Find bigger top creators"]
    R --> R2["Learn from role models to build a profile"]
```

| Lever | What it means | Mainly delivered by |
|---|---|---|
| **Inspiration** | Related topics, better content on the same topic, new information | Distribution & search / inspiration modeling / content modeling |
| **Quick feedback** | Getting likes, comments and follows quickly during cold start | Cold-start distribution |
| **Role models** | Finding bigger top creators and learning from them to build a profile | Creator discovery |

## 4. Where each modeling task sits in the flywheel

| Task | Step | In one line |
|---|---|---|
| **Creation-propensity modeling** (will this viewer try creating; will they remix or imitate what they are watching) | Viewer → first-time creator | Turn a viewer into a first-time creator (entry conversion) |
| **Inspiration modeling** | First-time creator → top creator | Give inspiration, drive growth, help creators move up |
| **Distribution & search system** | Top content → viewers, plus the three levers | Distribution loop + cold-start feedback + inspiration and role-model discovery |
