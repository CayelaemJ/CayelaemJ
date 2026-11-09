# Reading access and technical source review

**Public learning website:** [OmniMaster Study Room](https://omnimaster-study-room-share.onrender.com/)

The course lessons, interactive questions, frontend/backend textbook and PDF edition are intended for anyone who wants to learn. They are served directly on the website, so visitors do **not** need to browse a GitHub repository to use them.

## The security distinction

**Website access and GitHub repository access are different things.** Making the education website independent of GitHub navigation reduces unnecessary exposure to development materials, but does not change repository permissions.

**Current state (9 November 2026):** the GitHub profile repository `CayelaemJ/CayelaemJ` is public. Anyone with its URL can view the committed files. Removing its links from the Study Room does **not** make it private or restrict its readers.

GitHub does not automatically establish that an anonymous visitor is a legitimate recruiter or technology professional. A self-described role, checkbox or unverified email domain is not access control.

## Recommended separation

| Material | Audience | Correct control |
|---|---|---|
| Public study lessons, tutorials and PDF | Everyone | Standalone read-only website with no secrets |
| Selected professional achievements and case studies | Everyone | Public portfolio, sanitised and based on genuine evidence |
| Detailed engineering interviews, architecture samples, code review | Approved recruiters and technical reviewers | **Private GitHub repository**, individually granted access after manual identity and role verification |
| Proprietary employer/client data, credentials, internal source | Nobody without underlying organisation authorisation | Do not publish or share outside the authorised project |

**Important:** turning the special profile repository private will remove its README from the public GitHub profile and break existing links. Before any visibility change, preserve a small public profile and migrate sensitive source into a separate private repository. Existing public project repositories also need their **own** visibility reviews. Previously published content may remain in forks, clones, caches or Git history even after a change.

## What to do for vetted code review

For a real recruiter or technical reviewer, verify their identity and affiliation through a trusted channel, confirm what source they need, and grant access only to the necessary private material. **A private repository owned by a personal GitHub account grants collaborators write access rather than read-only access.** For a read-only technical review, prefer a private GitHub **organisation** repository where an appropriate read role can be assigned, or an identity-protected read-only document/code-review experience. Review access periodically and revoke it when no longer needed.

Where access requirements need corporate SSO, expiry policies or institutional controls, use an appropriate managed identity/access service. Cloudflare Access can protect a **website** using identity rules; it cannot retroactively make a **public GitHub repository** private.

## What this implementation does

The Study Room now hosts the lessons in its own read-only Cloudflare Worker bundle, including links between chapters and a generated PDF. External GitHub project URLs in article source text are rendered as non-clickable references in public learning mode. The website does not collect user accounts or personal data.

**What it does not do:** change GitHub repository visibility, verify recruiter identity, create a private repository, or revoke public repository access. Those actions require an explicit repository migration and permission change.

[Back to the Study Room](https://omnimaster-study-room-share.onrender.com/) · [Read the frontend/backend book](https://omnimaster-study-room-share.onrender.com/OMNIMASTER_FULLSTACK_PLAYBOOK.html)
