# Human Interface 01 | My UI/UX development journey

[← Volume VI](../OMNIMASTER_HUMAN_INTERFACE.md) · [Next: Designing for people →](02_HUMAN_CENTRED_DESIGN.md)

## How I arrived here

I didn't start my engineering journey by memorising interface patterns. I started with **Statistics and Data Science**, worked with enterprise dashboards and operational data, then grew into building the applications and workflows that deliver those insights to people.

That progression changed my thinking about the interface.

A dashboard can return the correct number and still confuse its intended audience. An API can successfully process an upload while the page makes somebody click Submit three times. A carefully secured workflow can leave someone uncertain about what permission is missing or how to recover.

UI/UX development is where those engineering outcomes become **human experiences**.

## A timeline of the questions

| Experience | The interface question it taught me |
|---|---|
| **Banking and commercial BI** | Do users understand the metric, filter context, comparison period and limitations? |
| **Manufacturing and logistics analytics** | Can operational users find exceptions quickly without interpreting fifteen unrelated charts? |
| **FMCG and research reporting** | Does visual hierarchy help people make sense of high-volume data rather than hide the assumptions? |
| **Cross-stack platforms** | How do loading, validation, failed writes, permissions and feedback affect a person's confidence? |
| **Learning and assessment products** | Does the interface serve learners, educators and guardians with different needs and responsibilities? |
| **Mobile, responsive and dark-mode testing** | Does the experience survive smaller screens, touch input, changed contrast and platform conventions? |
| **Portfolio and learning experiences** | Can someone discover the right page and actually use it without reading a repository instruction first? |

These are engineering lessons and product contexts from my work, not invented quantified usability studies.

## From UI development to UX reasoning

**UI work** includes building layouts, interactions, reusable components, charts, forms and responsive states.

**UX work** asks whether those elements support a real task: find an account, submit valid data, understand a result, complete an assessment, recover from failure or make a decision.

I want both to connect.

~~~mermaid
flowchart LR
    GOAL["User goal"] --> FLOW["Task flow"]
    FLOW --> UI["Visual and interaction design"]
    UI --> CODE["Component / API behaviour"]
    CODE --> STATE["Correct system state"]
    STATE --> FEEDBACK["Understandable result"]
    FEEDBACK --> LEARN["Usability observations"]
    LEARN --> FLOW
~~~

An elegant UI built on inconsistent backend state is misleading. Correct backend state hidden behind ambiguous controls is equally frustrating. Good interfaces bridge the two.

## What I now notice almost automatically

When I open an interface I ask: **What is the primary task? What action stands out? What happens after the click? What would confuse a first-time visitor? What if the person is on a phone? What if the request fails?**

I care about the details because they determine whether somebody can actually use the product.

My tendency toward broad systems thinking is helpful, but there's a danger: designing an elaborate system before observing real behaviour. The correction is to test assumptions early with people and to prefer a clear, familiar workflow when it solves the problem.

## Why the GitHub study-room problem matters

The first version of my Study Room had a link that opened an HTML file **inside GitHub's code viewer**. The application existed, but the route didn't deliver the experience the visitor expected. That is an information-architecture and task-success failure.

The repair is not more decorative text explaining how HTML works. It is a link to an actual hosted experience, with source code kept as a separate option.

The lesson: **the path to the interface is part of the interface.**

## What I want to learn next

I want to deepen direct usability research, formal experiment design, advanced accessibility verification, accessible data visualisation and consistent native/mobile behaviour. I will not call a design “user-validated” just because automated checks pass.

I enjoy full-stack development partly because it gives me context for making UI/UX decisions that respect source truth, transactions, performance and privacy.

### Try this exercise

Choose a page you have built. Write its single primary user goal in one sentence. Ask someone unfamiliar with the page to complete the goal without help. Observe where they hesitate, what they expected, and what actually happened. Change the interface based on that evidence.

[← Volume VI](../OMNIMASTER_HUMAN_INTERFACE.md) · [Next: Human-centred design →](02_HUMAN_CENTRED_DESIGN.md)
