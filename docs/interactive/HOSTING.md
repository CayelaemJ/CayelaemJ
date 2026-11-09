# Study Room hosting and publishing

**Primary sharing website:** [https://omnimaster-study-room-share.onrender.com/](https://omnimaster-study-room-share.onrender.com/)  
**Original Cloudflare Worker:** [https://omnimaster-study-room.cabo-solutions-za.workers.dev/](https://omnimaster-study-room.cabo-solutions-za.workers.dev/)  
**Canonical editable HTML source:** [index.html](index.html)  
**Static checks:** [test_study_room.py](test_study_room.py)

## Why this website exists

GitHub's regular `blob/main/docs/interactive/index.html` page shows **HTML source**. It does not run a custom interactive application in the repository file viewer.

The OmniMaster Study Room therefore has a **separate, public Cloudflare Worker deployment**. The profile's main action now targets the website. The source link remains available but is labelled accordingly.

This is a small, public learning experience with no user accounts, external script dependencies, API requests or production data. The website now serves approved educational Markdown as **readable HTML directly from the Worker**, without redirecting visitors to GitHub. External source-code references from those articles are intentionally not clickable in public learning mode.

## Public sharing fallback and manual Render update

LinkedIn Post Inspector reported that it could not connect to the original `workers.dev` address. Cloudflare's managed Browser Integrity Check applies to `workers.dev` and cannot be disabled for that hostname. To avoid disrupting the working Worker, a **separate Render static site** was created at https://omnimaster-study-room-share.onrender.com/.

- Render service: `omnimaster-study-room-share`, static hosting (not the private OmniMaster portfolio).
- Public GitHub source: `CayelaemJ/CayelaemJ`, branch `main`.
- Build: `node docs/interactive/export_static.mjs`.
- Publish folder: `docs/interactive/.static-publish`.
- `OMNIMASTER_PUBLIC_ORIGIN`: `https://omnimaster-study-room-share.onrender.com`.
- **Auto-deploy is disabled**. After changes to course content, rebuild and manually deploy this Render static site; the Cloudflare Worker has its own independent publishing process.
- The export writes 56 HTML files including 54 lessons, plus the PDF, original 1200 × 630 PNG, `robots.txt` and sitemap. Lesson links point to actual `.html` pages, not Markdown source.
- Automated export testing checks all 1,003 internal hyperlinks, site-specific Open Graph URLs, image and PDF. A live browser independently verified the new site's homepage and social metadata; the user's LinkedIn Post Inspector outcome has not yet been confirmed.
- Static site hosting is free on Render but consumes account-level bandwidth and build minutes, and usage beyond included allowances may be billable depending on account settings.

Keep the original Worker URL online as a fallback. Do not change Cloudflare's Worker Open Graph canonical host to Render: each host must refer to its own address.

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

## Social sharing / link previews

The Worker injects canonical and Open Graph metadata **server-side**, including `og:title`, `og:description`, `og:url`, `og:image`, `og:image:width`, `og:image:height`, and a `twitter:card=summary_large_image` tag.

- `GET /og/omnimaster-study-room.png` returns a locally generated **1200 × 630 image/png**, built using standard Node.js code and embedded in the Worker. No external image hosting or cookies.
- Metadata is on `/`, `/library`, the frontend/backend textbook and the other public lesson routes, with page-specific titles.
- The original `docs/interactive/social-preview-image.mjs` builds the card; `docs/interactive/social-metadata.mjs` creates the link-preview tags.
- `node docs/interactive/test_library_worker.mjs` validates PNG dimensions, size, MIME, public access, and initial-HTML tags without relying on a JavaScript-rendering crawler.
- After deployment, test the raw live HTML and publicly served image. Use LinkedIn Post Inspector to refresh any previously cached preview. A successful deployment does not guarantee LinkedIn will generate a card until the platform re-fetches it.

## Reader and catalogue routes

- `GET /library`: a searchable, category-filtered 54-page catalogue, rendered directly by the Worker, with filtering handled only in the reader's browser.
- `GET /academy/*.md`, `/human-interface/*.md`, `/reliability/*.md`, and other approved routes: HTML article reader with an on-page contents panel, reading estimates and next/previous navigation where applicable.
- `GET /downloads/omnimaster-fullstack.pdf`: the existing generated PDF book.
- Optional article-read state is stored under `omnimaster.reader.completed.v1` in browser `localStorage`; the 30-day expedition uses a separate local key. Neither is sent to the server.

The source-based integration test exercises these routes, while live browser rendering should verify visual layout, category filtering, accessible keyboard access and article progression.

## UX acceptance criteria

A visitor clicking **Launch the live Study Room** must open an interactive page, not a GitHub source viewer. A visitor clicking **Inspect the HTML source** should open the source viewer intentionally.

The live page must display meaningful loading and feedback states, have keyboard-visible controls, reflow on narrow devices, avoid third-party scripts/trackers and keep the learning exercises functional without creating an account. Public lesson pages must not direct visitors to the GitHub source viewer.

## Verification boundaries

Cloudflare's API can confirm a Worker script and its deployment status. It cannot by itself prove that every external browser can access the page, that all lesson redirects behave correctly, or that a participant can complete a task.

The repository's Python HTML tests check static structure and no-network design decisions, not real-user task completion or formal accessibility conformance.

[Read the UI/UX fieldbook](../OMNIMASTER_HUMAN_INTERFACE.md) · [Open the live Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/)
