# Study Room hosting and publishing

**Live website:** [omnimaster-study-room.cabo-solutions-za.workers.dev](https://omnimaster-study-room.cabo-solutions-za.workers.dev/)  
**Canonical editable HTML source:** [index.html](index.html)  
**Static checks:** [test_study_room.py](test_study_room.py)

## Why this website exists

GitHub's regular `blob/main/docs/interactive/index.html` page shows **HTML source**. It does not run a custom interactive application in the repository file viewer.

The OmniMaster Study Room therefore has a **separate, public Cloudflare Worker deployment**. The profile's main action now targets the website. The source link remains available but is labelled accordingly.

This is a small, public learning experience with no user accounts, external script dependencies, API requests or production data. The course and UX chapter links on the hosted page redirect to the corresponding public GitHub Markdown files.

## Current deployment architecture

| Component | Where it lives | Notes |
|---|---|---|
| Canonical HTML/CSS/JS | `docs/interactive/index.html` on GitHub | Single-page, self-contained, framework-free and testable offline |
| Hosted copy | Cloudflare Worker `omnimaster-study-room` | An embedded HTML snapshot served at the public workers.dev address |
| Cloudflare account subdomain | `cabo-solutions-za.workers.dev` | Worker route enabled |
| Study material | Public GitHub Markdown chapters | The Worker provides redirects for known local lesson paths |
| Optional progress | Browser `localStorage` | No backend sync; browser/device-specific; can be cleared |
| CI | `engineering-labs-ci.yml` | Static structure and link tests; **not** a live browser or deployment check |

## Publishing a new study-room version

**Important: GitHub changes to the HTML do not automatically deploy to the Worker.** The hosted Worker contains a snapshot, so a maintainer must update that copy intentionally and verify the live page.

The deployment sequence is:

1. Merge tested HTML changes to the canonical repository, or prepare a clearly scoped candidate.
2. Run `cd docs/interactive && python -m unittest discover -v`, the full library link validator and relevant accessibility checks.
3. Upload a new version of the static HTML embedded in the `omnimaster-study-room` Worker using an authorised Cloudflare deployment workflow. Preserve the `GET /index.html` and `GET /` page response, known internal-document redirects and the no-network privacy model.
4. Verify the Worker version, 100% deployment routing and enabled workers.dev subdomain in Cloudflare.
5. **Open the actual URL in a browser** and test question selection, answer feedback, keyboard focus, mobile width, source/lesson destinations and optional progress/reset.
6. Record the matching Git commit and Worker deployment. Do not claim a completed browser smoke test unless it actually ran.

Do not put API tokens in the repository or browser source. The canonical HTML remains runnable offline, independently of hosting.

## UX acceptance criteria

A visitor clicking **Launch the live Study Room** must open an interactive page, not a GitHub source viewer. A visitor clicking **Inspect the HTML source** should open the source viewer intentionally.

The live page must display meaningful loading and feedback states, have keyboard-visible controls, reflow on narrow devices, avoid third-party scripts/trackers and keep the learning exercises functional without creating an account.

## Verification boundaries

Cloudflare's API can confirm a Worker script and its deployment status. It cannot by itself prove that every external browser can access the page, that all lesson redirects behave correctly, or that a participant can complete a task.

The repository's Python HTML tests check static structure and no-network design decisions, not real-user task completion or formal accessibility conformance.

[Read the UI/UX fieldbook](../OMNIMASTER_HUMAN_INTERFACE.md) · [Open the live Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/)
