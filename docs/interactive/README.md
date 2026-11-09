# OmniMaster Offline Study Room

This is a **static, self-contained HTML experience** for readers of [Volume V: Build a System With Me](../OMNIMASTER_BUILD_WITH_ME.md).

## Launch the hosted experience

**[Open the live OmniMaster Study Room](https://omnimaster-study-room.cabo-solutions-za.workers.dev/).** The public, static page is served from a separate Cloudflare Worker. There is no GitHub Pages deployment involved. [Source HTML](index.html) is available for inspection.

## Run locally

1. Clone or download the [CayelaemJ profile repository](https://github.com/CayelaemJ/CayelaemJ).
2. Double-click **`docs/interactive/index.html`** or open it in your browser.
3. Browse seven foundational lessons plus additional specialist volumes, answer seven engineering scenarios and tick off the 30 daily study missions.

GitHub's normal file preview displays HTML as source and **does not execute it**. Use the live Cloudflare URL above to interact without cloning, or open the HTML file locally. See [hosting and maintenance notes](HOSTING.md).

## Browse the complete online library

The hosted site has a [searchable catalogue of all 54 lessons](https://omnimaster-study-room.cabo-solutions-za.workers.dev/library), filterable by subject. Every hosted article includes reading estimates, a contents panel where applicable, previous/next links within its subject and optional **Mark as read** progress stored in the visitor's own browser only. This does not create an account, send analytics events or sync between devices.

The `/library` and book routes only exist on the hosted Worker, not when opening the standalone HTML file from disk.

## What it includes

- An offline, browser-readable guide to the Academy and Volume V.
- Seven fictional engineering decision scenarios with explanations.
- An optional 30-day checklist, with a progress bar and a clear-progress button.
- Dark OmniMaster styling, responsive layouts, visible keyboard focus, semantic sections and accessible announcements.

## Privacy and security

No CDN, tracker, external API, third-party script, cookie or account is used. There are no requests to my website or GitHub. Progress is stored in the **current browser's localStorage** when available. In privacy-restricted environments or some file:// browser contexts, storage can fail; the page still works without persistent progress. Clearing local progress removes only this study-room checklist.

The browser HTML contains no live database access and does not reproduce an authenticated product. The choice of fictional questions is explanatory, not a universal architecture answer key.

## Tests

The accompanying Python standard-library static tests check link paths, page structure, scenario/mission counts, presence of the content security policy and absence of external network code.

~~~bash
cd docs/interactive
python -m unittest discover -v
~~~

These tests are *not* browser-based cross-device or security penetration testing. They only confirm the documented properties of this small source file.
