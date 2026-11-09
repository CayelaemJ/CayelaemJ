# THE OMNIMASTER HUMAN INTERFACE
### Volume VI | UI/UX engineering: designing for people, not merely for screens

**Cayelaem Jantjies · A practical account of how I build interfaces, learn from users and connect experience design to data and software engineering.**

[← GitHub profile](../README.md) · [My engineering story](OMNIMASTER_HANDBOOK.md) · [Engineering Academy](OMNIMASTER_ACADEMY.md) · [Interactive Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/)

---

> My work doesn't end when the data is correct. The person on the other end must be able to find it, understand it, trust it and act on it. That is why UI/UX development matters to me.

I have built dashboards, interfaces and application workflows across analytics and independent software projects. Working across SQL, APIs, React, reporting, mobile UI and authentication taught me that **usability is a system property**, not a layer of decoration added to finished code.

This volume explains how my thinking evolved from “make the information visible” to **“make the right action understandable, accessible and recoverable.”** I am involved in UI and UX development as part of my cross-stack work. I do not use that fact to invent a dedicated job title or claim that every usability hypothesis has already been validated with external research participants.

## Read by interest

| You want to know… | Start |
|---|---|
| How I became interested in interfaces beyond analytics | [01 · My UI/UX engineering journey](human-interface/01_MY_UX_JOURNEY.md) |
| What actually matters when people use software | [02 · Designing for real humans](human-interface/02_HUMAN_CENTRED_DESIGN.md) |
| How the ideas connect to products I build | [03 · Case studies and design reasoning](human-interface/03_UX_CASE_STUDIES.md) |
| How I build consistent, inclusive experiences | [04 · Design systems and accessibility](human-interface/04_DESIGN_SYSTEMS_AND_ACCESSIBILITY.md) |
| How I test whether an interface works | [05 · Usability research and measurement](human-interface/05_MEASURE_USABILITY.md) |
| How to practise and follow the same path | [06 · UI/UX workbook](human-interface/06_UX_WORKBOOK.md) |

## What changed my understanding of interface design

A technically correct dashboard can still make someone choose the wrong option. A successful API request can still leave a user wondering whether their change saved. An authentication screen can be secure but impossible to recover from. A visually impressive product can fail on narrow screens or with keyboard navigation.

I started paying attention to the entire journey, not simply the component.

~~~mermaid
flowchart LR
    NEED["Person's goal"] --> UNDERSTAND["Understand their context"]
    UNDERSTAND --> TASK["Design the task flow"]
    TASK --> INTERFACE["Build a usable interface"]
    INTERFACE --> TEST["Observe, test and measure"]
    TEST --> IMPROVE["Repair the friction"]
    IMPROVE --> TASK
~~~

## The seven questions I ask about an interface

1. **Purpose:** what job does the person want done, and how urgent is it?
2. **Clarity:** can they tell what the system is showing and what to do next?
3. **Feedback:** what confirms success, saving, loading, failure or an irreversible action?
4. **Control:** can they undo, retry, correct or safely abandon the operation?
5. **Access:** does it work for different devices, abilities and technology constraints?
6. **Trust:** are data freshness, permissions, AI uncertainty and consequences explained?
7. **Evidence:** did we observe task success, or did we merely like the mock-up?

A UX designer learns the user's mental model. A UI developer makes the design behave predictably. A data engineer makes the state behind it correct. I enjoy the connections between all three.

## My project contexts

- **Enterprise dashboards:** metric labels, filter logic, chart clarity, performance and decision-making.
- **The Fixer:** ingestion setup, source previews, validation errors, role-aware workflows and administrative tools.
- **CABO Learning Hub:** distinct learner, parent and educator journeys, privacy, age-aware patterns and assessment feedback.
- **Mobile and responsive work:** narrow-width controls, readable charts, dark-mode behaviour, focus and platform differences.
- **OmniMaster portfolio and study room:** navigation, discoverability, interactive learning and a directly observable UX mistake: an HTML source link does not launch the experience.

Some of these are active product design or test workstreams, not proof of launched features or formal end-user study results. The chapters distinguish design intent, implementation and verified behaviour.

## The purpose of this volume

I want readers to be able to critique their own apps, not simply copy my colours. Each chapter includes a decision framework, examples and exercises. The workbook asks you to design a task, test it with people where possible, and improve it based on real observations.

**An interface should help a person succeed, not make them admire how hard the developer worked.**

[Start with my UI/UX journey →](human-interface/01_MY_UX_JOURNEY.md)
