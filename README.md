# perfload-site

Marketing site for [PerfLoad](https://perfload.io) — a self-hosted, no-script HTTP load testing tool. Plain static HTML, no build step, deployed with GitHub Pages.

## Structure

- `index.html` — homepage (what PerfLoad is, installation, Workbench/Dashboard, AI skills, Chrome extension, Cloud teaser)
- `cloud.html` — PerfLoad Cloud (coming soon) page, includes an embedded Google Form signup
- `extension.html` — Chrome extension (PerfLoad Workspace Launcher) landing page
- `privacy.html` — privacy policy for the Chrome extension
- `curl-load-test/`, `api-load-testing/`, `curl-to-k6/`, `k6-alternative/`, `ci-cd-load-testing/`, `github-actions-load-testing/`, `self-hosted-load-testing/`, `http-load-test/`, `load-testing-tool/`, `website-load-test/`, `rest-api-load-test/` — SEO landing pages, one `index.html` per directory (served at `/<name>/`). They share `assets/landing.css` and `assets/landing.js`, and each carries its own title, description, canonical, Open Graph tags, and JSON-LD. The CI/CD and GitHub Actions examples mirror the runner's documented API (see the CI/CD section of the `perfload` repo's README). Keep all seven listed in `sitemap.xml` and linked from the homepage's Guides section
- `assets/screenshots/` — product screenshots used across the pages
- `CNAME` — custom domain for GitHub Pages (currently `perfload.io`)
- `robots.txt`, `sitemap.xml` — SEO basics

## Local preview

No build tooling needed — just serve the directory and open it:

```
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deployment

This repo is served directly by **GitHub Pages** from the `main` branch. The `CNAME` file pins the custom domain (`perfload.io`); DNS for that domain is managed on **Namecheap** (Advanced DNS tab):

- Apex (`@`) — 4 A records to GitHub Pages' IPs (`185.199.108.153` / `.109.153` / `.110.153` / `.111.153`)
- `www` — CNAME to `stepince.github.io.`

`perfload.net` is set up as a redirect to `perfload.io` via a Namecheap URL Redirect Record (Advanced DNS on the `perfload.net` domain, not this repo).

Pushing to `main` deploys automatically — no CI step.

## Updating the "Get notified" Google Form (cloud.html)

The signup form on `cloud.html` is a Google Form embedded via iframe:

```html
<iframe src="https://docs.google.com/forms/d/1PCUszsEsFrAmjnXOmTLEDTvICTmMXAAixcNfMwS7t3s/viewform?embedded=true">
```

To edit the form itself (title, questions, branding text):

1. Go to the edit URL — swap `/viewform` for `/edit` in the link above (or open [forms.google.com](https://forms.google.com) and find it in your form list).
2. Make your changes — Google Forms autosaves, no republish step needed.
3. Only touch this repo if the form's **ID** changes (e.g. you create a brand new form) — then update the `src` in `cloud.html` to the new form's `/viewform?embedded=true` URL.

## Naming conventions

The product was renamed from "curl-load" to "PerfLoad" (domain: `perfload.io`, not `.com`). Brand-name references in prose/headers/titles use **PerfLoad**; code-facing identifiers stay lowercase `perfload` — the domain, the Docker image/volume names (`perfload/perfload-runner`, `perfload-runs`), the Chrome Web Store URL slug, and literal in-app UI strings quoted in copy (e.g. the Chrome tab group label `"perfload"`, the `"perfload dashboard →"` link text) since those describe actual lowercase text shown in the product's screenshots.
