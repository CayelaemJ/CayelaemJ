# Study Room hosting and publishing

**Live website:** [omnimaster-study-room.cabo-solutions-za.workers.dev](https://omnimaster-study-room.cabo-solutions-za.workers.dev/)  
**Canonical editable HTML source:** [index.html](index.html)  
**Static checks:** [test_study_room.py](test_study_room.py)

## Why this website exists

GitHub's regular `blob/main/docs/interactive/index.html` page shows **HTML source**. It does not run a custom interactive application in the repository file viewer.

The OmniMaster Study Room therefore has a **separate, public Cloudflare Worker deployment**. The profile's main action now targets the website. The source link remains available but is labelled accordingly.

This is a small, public learning experience with no user accounts, external script dependencies, API requests or production data. The website now serves approved educational Markdown as **readable HTML directly from the Worker**, without redirecting visitors to GitHub. External source-code references from those articles are intentionally not clickable in public learning mode.

## Current deployment architecture

| Component | Where it lives | Notes |
|---|---|---|
| Canonical HTML/CSS/JS | `docs/interactive/index.html` on GitHub | Single-page, self-contained, framework-free and testable offline |
| Hosted copy | Cloudflare Worker `omnimaster-study-room` | Embedded HTML plus 54 public teaching pages, with read-only lesson routes |
| Cloudflare account subdomain | `cabo-solutions-za.workers.dev` | Worker route enabled |
| Study material | Approved educational Markdown chapters | Bundled into the Worker when deployed, served on-site as HTML rather than GitHub redirects |
| Downloadable textbook | `/downloads/omnimaster-fullstack.pdf` | Actual PDF response generated from the public full-stack playbook at deployment build |
| Optional progress | Browser `localStorage` | No backend sync; browser/device-specific; can be cleared |
| CI | `engineering-labs-ci.yml` | Static structure and link tests; **not** a live browser or deployment check |

## Publishing a new study-room version

**Important: GitHub changes to the HTML do not automatically deploy to the Worker.** The hosted Worker contains a snapshot, so a maintainer must update that copy intentionally and verify the live page.

The deployment sequence is:

1. Merge tested HTML changes to the canonical repository, or prepare a clearly scoped candidate.
2. Run `cd docs/interactive && python -m unittest discover -v`, the full library link validator and relevant accessibility checks.
3. Run `node docs/interactive/build_worker.mjs` to create the generated read-only Worker containing the approved chapters and the Study Room HTML. Run `node docs/interactive/test_library_worker.mjs` and check that lesson routes and the PDF response are valid. Deploy that **exact generated Worker** to `omnimaster-study-room` using an authorised Cloudflare deployment workflow. Preserve `GET /`, the on-site lesson routes and the no-tracking privacy model.
4. Verify the Worker version, 100% deployment routing and enabled workers.dev subdomain in Cloudflare.
5. **Open the actual URL in a browser** and test question selection, answer feedback, keyboard focus, mobile width, the frontend/backend book, lesson navigation, real PDF download and optional progress/reset. A successful deployment API response alone is not browser validation.
6. Record the matching Git commit and Worker deployment. Do not claim a completed browser smoke test unless it actually ran.

Do not put API tokens in the repository or browser source. The canonical HTML remains runnable offline, independently of hosting.

## UX acceptance criteria

A visitor clicking **Launch the live Study Room** must open an interactive page, not a GitHub source viewer. A visitor clicking **Inspect the HTML source** should open the source viewer intentionally.

The live page must display meaningful loading and feedback states, have keyboard-visible controls, reflow on narrow devices, avoid third-party scripts/trackers and keep the learning exercises functional without creating an account. Public lesson pages must not direct visitors to the GitHub source viewer.

## Verification boundaries

Cloudflare's API can confirm a Worker script and its deployment status. It cannot by itself prove that every external browser can access the page, that all lesson redirects behave correctly, or that a participant can complete a task.

The repository's Python HTML tests check static structure and no-network design decisions, not real-user task completion or formal accessibility conformance.

[Read the UI/UX fieldbook](../OMNIMASTER_HUMAN_INTERFACE.md) · [Open the live Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/)
