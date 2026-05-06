---
name: privacy-audit
description: >
  Audit whether an app's legal documents (Privacy Policy, ToS, Cookie Policy, DPA) accurately
  reflect its actual data practices. Use when the user wants to: audit their privacy policy or
  terms of service, verify GDPR compliance, find gaps in legal docs, or asks "does my privacy
  policy cover X", "is my ToS accurate", "audit my privacy policy", "are my legal docs compliant".
  Trigger when the user shares legal documents with either an app description OR source code /
  GitHub repo URL — Claude will extract app reality from code automatically when available,
  without requiring a manual description. Always use for legal document vs. app reality gap analysis.
---

# Privacy & Legal Docs Audit Skill

This skill audits whether an app's legal documents (Privacy Policy, ToS, Cookie Policy, DPA)
accurately and completely reflect its actual data practices. It produces:
1. A **structured markdown report** (downloadable)
2. An **interactive artifact** (Claude API-powered, for live in-browser auditing)

---

## Input Modes

There are two ways to provide app reality. Use whichever the user provides — **never ask for a manual description if code is available**.

### Mode A — Manual Description
The user describes the app themselves.

| Input | Required | Notes |
|---|---|---|
| App description / data flow | ✅ | What the app does, what data it collects, how it stores/processes it, third-party integrations |
| Privacy Policy text | ✅ (at least one doc) | Full text or URL |
| Terms of Service text | ⬜ Optional | Full text or URL |
| Cookie Policy text | ⬜ Optional | Full text or URL |
| DPA (Data Processing Agreement) | ⬜ Optional | Full text or URL |
| Target jurisdictions | ⬜ Optional | Default: GDPR (EU) + general best practices |

### Mode B — Code Analysis (preferred when code is available)
The user provides source code files or a GitHub repo URL. Claude extracts the app reality directly from the code — no manual description needed.

| Input | Required | Notes |
|---|---|---|
| Source code files or GitHub URL | ✅ | Full repo, or key files (see below) |
| Privacy Policy text | ✅ (at least one doc) | Full text or URL |
| Terms of Service text | ⬜ Optional | Full text or URL |
| Cookie Policy text | ⬜ Optional | Full text or URL |
| DPA (Data Processing Agreement) | ⬜ Optional | Full text or URL |
| Target jurisdictions | ⬜ Optional | Default: GDPR (EU) + general best practices |

If a GitHub URL is provided, use `web_fetch` to retrieve key files. Prioritize:
- `package.json` / `requirements.txt` / `Gemfile` — to identify third-party dependencies
- Environment/config files (`.env.example`, `config/`, `settings.py`) — for integrations
- Database schema files — for understanding what data is persisted
- API route files — for understanding what data is received and processed
- Authentication files — for understanding user identity data
- Any existing legal docs in the repo (`/public`, `/legal`, `/docs`)

See `references/code-analysis.md` for detailed extraction patterns per tech stack.

---

## Audit Methodology

### Step 1 — Extract App Reality

**If Mode A (manual description):** extract from the user's description.

**If Mode B (code):** analyze the codebase to extract the same inventory automatically. See `references/code-analysis.md` for stack-specific patterns. Key things to look for:

- **`package.json` / dependency files**: identify analytics SDKs (Mixpanel, Segment, Amplitude, GA), auth providers (Auth0, Clerk, NextAuth), payment processors (Stripe), email services (SendGrid, Resend), error tracking (Sentry), cloud storage (S3, Cloudinary), databases (Supabase, PlanetScale, Mongo Atlas), AI APIs (OpenAI, Anthropic), and any other third-party service
- **Database schema / migrations**: every table/model = a category of data collected and persisted; flag tables with PII (users, profiles, sessions, payments, logs)
- **API routes / controllers**: what data comes in via POST/PUT bodies? what gets logged? what gets forwarded to third parties?
- **Auth implementation**: what identity data is stored? OAuth scopes requested? session storage method?
- **Frontend / client-side code**: cookies set, localStorage usage, tracking pixels, analytics calls, form fields collecting PII
- **Environment variables**: any `.env.example` reveals integrations even if keys are hidden
- **Storage calls**: S3 uploads, Cloudinary, Supabase Storage — what file types are stored and from whom?

After code analysis, produce the same structured inventory as Mode A:

- **Data collected**: personal data, behavioral data, device/technical data, user-generated content
- **Data subjects**: end users, clients, third parties, minors (if any)
- **Processing purposes**: core functionality, analytics, marketing, AI/ML training, etc.
- **Storage & infrastructure**: where data lives (country/cloud provider), retention periods
- **Third-party sharing**: integrations, SDKs, APIs, subprocessors (with specific service names found in code)
- **User rights mechanisms**: deletion, export, opt-out, consent flows
- **Special categories**: health data, financial data, location, biometrics

### Step 2 — Extract Legal Doc Claims

For each provided document, extract what is claimed about the same categories above.

### Step 3 — Gap Analysis

Compare reality vs. claims across these audit dimensions:

#### 🔴 Critical Gaps (must fix — legal risk)
Items present in app reality but **absent or contradicted** in legal docs:
- Undisclosed data collection
- Undisclosed third-party sharing or subprocessors
- Missing legal basis for processing (GDPR Art. 6)
- Missing data subject rights procedures
- Incorrect or missing data retention periods
- Cross-border transfer not disclosed (GDPR Ch. V)

#### 🟡 Important Gaps (should fix — compliance risk)
- Vague or non-specific language where specificity is required
- Cookie/tracking not covered by cookie policy
- Missing or weak DPA clauses if processing third-party personal data
- No mention of data breach procedures (GDPR Art. 33/34)
- Missing processor vs. controller distinction

#### 🟢 Minor Issues (nice to fix — best practice)
- Outdated contact info / DPO details
- No plain-language summary
- Missing version/date on documents
- ToS doesn't reflect current feature set

### Step 4 — GDPR Checklist

Run a GDPR-specific checklist (see `references/gdpr-checklist.md`). Flag each item as ✅ / ⚠️ / ❌.

### Step 5 — Recommendations

For each gap, provide:
- **What's missing**: specific clause or statement
- **Why it matters**: legal risk or regulatory exposure
- **Suggested fix**: draft language or concrete action

---

## Output Formats

### Format A — Markdown Report

Generate a downloadable `.md` file with this structure:

```
# Privacy & Legal Audit Report
## App: [name]
## Date: [date]
## Documents audited: [list]

---

## Executive Summary
[2–3 sentence overview of overall compliance posture]

## App Data Reality
[Structured inventory from Step 1]

## Critical Gaps 🔴
[Numbered list with: gap description, affected document, suggested fix]

## Important Gaps 🟡
[Same format]

## Minor Issues 🟢
[Same format]

## GDPR Checklist
[Table: requirement | status | notes]

## Recommended Next Steps
[Prioritized action list]
```

Save to `/mnt/user-data/outputs/privacy-audit-report.md` and present with `present_files`.

### Format B — Interactive Artifact

Build a React artifact (`.jsx`) with Claude API integration that allows the user to:
- Paste app description + legal docs into text areas
- Select which documents they're providing
- Select target jurisdiction(s)
- Click "Run Audit" to get a live AI-powered audit report rendered in the UI
- See findings grouped by severity with expandable detail cards
- Download the report as markdown

See `references/artifact-template.md` for the React component structure.

**Always produce both formats** unless the user explicitly asks for only one.

---

## Important Notes

- **Prefer code analysis over manual description** — if the user provides code or a GitHub URL, use Mode B. Never ask for a manual description when code is available.
- If the user provides a GitHub URL, use `web_fetch` to fetch `https://raw.githubusercontent.com/{owner}/{repo}/main/package.json` and other key files directly.
- If the user provides URLs for legal docs instead of text, use `web_fetch` to retrieve the content before auditing.
- If documents are PDFs, read the `pdf-reading` skill first.
- Never fabricate legal requirements. Stick to established GDPR text, ePrivacy Directive, and widely accepted best practices.
- If a jurisdiction other than EU is mentioned (e.g., California → CCPA, Brazil → LGPD), consult `references/jurisdictions.md`.
- Always caveat the report: this audit is not legal advice and does not substitute for a qualified lawyer.
- Be specific in gap descriptions — avoid generic statements like "improve your privacy policy". Name the exact missing clause.
- When identifying third-party processors from code, use the actual service name (e.g. "Supabase" not "a database provider").

---

## Reference Files

- `references/gdpr-checklist.md` — Full GDPR compliance checklist (Articles 12–22, 24–32)
- `references/jurisdictions.md` — Key requirements per jurisdiction (CCPA, LGPD, PIPL, etc.)
- `references/artifact-template.md` — React component scaffold for the interactive artifact
- `references/code-analysis.md` — Stack-specific patterns for extracting data practices from code
