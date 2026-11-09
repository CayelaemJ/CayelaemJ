# OmniMaster Offline Study Room

This is a **static, self-contained HTML experience** for readers of [Volume V: Build a System With Me](../OMNIMASTER_BUILD_WITH_ME.md).

## Run it

1. Clone or download the [CayelaemJ profile repository](https://github.com/CayelaemJ/CayelaemJ).
2. Double-click **`docs/interactive/index.html`** or open it in your browser.
3. Browse seven lessons, answer five engineering scenarios and tick off the 30 daily study missions.

GitHub's normal file preview displays HTML as source and **does not execute it**. I have not claimed or configured GitHub Pages hosting for this page.

## What it includes

- An offline, browser-readable guide to the Academy and Volume V.
- Five fictional engineering decision scenarios with explanations.
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
