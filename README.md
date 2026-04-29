# 🔍 Privacy Audit Skill for Claude

A custom Claude skill that audits whether your app's legal documents — Privacy Policy, Terms of Service, Cookie Policy, and DPA — actually reflect what your app does.

Built for indie developers, SaaS founders, and freelancers who want to ship compliant products without a lawyer on retainer.

---

## What it does

You provide:
- A description of your app (what data it collects, how it stores it, third-party integrations)
- Your legal documents (Privacy Policy, ToS, Cookie Policy, DPA — any combination)

The skill produces:
- A **structured audit report** with findings grouped by severity
- An **interactive artifact** (Claude API-powered) for live in-browser auditing
- A **GDPR checklist** with 38 requirements, each marked ✅ / ⚠️ / ❌
- **Jurisdiction-specific checks** for GDPR, CCPA (California), LGPD (Brazil), UK GDPR, and more

### Severity levels

| Level | Meaning |
|---|---|
| 🔴 Critical | Legal risk — undisclosed data collection, missing legal basis, etc. |
| 🟡 Important | Compliance risk — vague language, missing cookie disclosure, etc. |
| 🟢 Minor | Best practice — outdated contact info, missing document version, etc. |

---

## Installation

### Option A — Claude Code (recommended)

If you use [Claude Code](https://docs.anthropic.com/en/docs/claude-code) in your terminal:

```bash
# Add this repo as a marketplace (one-time setup)
claude plugin marketplace add https://github.com/bellu/privacy-audit

# Install the plugin
claude plugin install privacy-audit@privacy-audit
```

Then run from inside any project:

```bash
/privacy-audit:audit
```

Claude will scan your codebase automatically — no manual description needed.

### Option B — Claude.ai web/app

1. Download [`privacy-audit.skill`](./privacy-audit.skill) from this repo
2. Go to [claude.ai](https://claude.ai) → **Settings** → **Skills**
3. Upload the `.skill` file
4. Done — Claude activates this skill automatically when you ask for a privacy or legal audit

### Option C — Build from source

```bash
git clone https://github.com/bellu/privacy-audit
cd privacy-audit

# Requires Python 3.8+
python package.py
```

This produces `privacy-audit.skill` in the current directory, ready to install via Option B.

---

## Usage

Once installed, just talk to Claude naturally:

> *"Audit my privacy policy — here's what my app does: [description]. And here's the policy: [text]"*

> *"Does my Terms of Service reflect what my SaaS actually does?"*

> *"Check my privacy policy for GDPR compliance"*

> *"I have a JS widget that collects user feedback and stores it in Supabase — what should my privacy policy say?"*

### Audit from URLs (no codebase needed)

If you don't have source code available, provide the URL of your legal documents and a description of your app:

> *"Audit this privacy policy for GDPR compliance: https://example.com/privacy — it's a SaaS that collects email, usage analytics via Mixpanel, and stores data on AWS S3."*

Or with multiple documents:

> *"Audit my legal docs:
> - Privacy Policy: https://example.com/privacy
> - Terms of Service: https://example.com/terms
> - Cookie Policy: https://example.com/cookies
>
> App: a newsletter platform that collects emails via Mailchimp, tracks opens/clicks, and uses Stripe for payments."*

Or with Claude Code:

```
/privacy-audit:audit
Privacy Policy URL: https://example.com/privacy
App description: Newsletter SaaS — collects emails, tracks opens via Mailchimp, payments via Stripe
```

Claude fetches the documents automatically and runs the full audit.

Claude will automatically use the skill and produce a full audit report.

### Changing jurisdiction

Default is GDPR (EU). To target a different jurisdiction, specify it in your prompt:

> *"Audit my privacy policy for CCPA compliance — here's the policy: [text]"*

Or when using Claude Code:

```
/privacy-audit:audit
Target jurisdictions: CCPA
```

Multiple jurisdictions at once:

```
/privacy-audit:audit
Target jurisdictions: GDPR, CCPA, LGPD
```

---

## What's inside

```
privacy-audit/
├── SKILL.md                          # Main skill instructions
└── references/
    ├── gdpr-checklist.md             # 38-point GDPR checklist (Art. 6, 12–22, 28, 32...)
    ├── jurisdictions.md              # GDPR, CCPA, LGPD, PIPL, UK GDPR, Australian Privacy Act
    └── artifact-template.md         # React scaffold for interactive audit UI
```

---

## Supported jurisdictions

- 🇪🇺 **GDPR** (EU) — full 38-point checklist
- 🇺🇸 **CCPA / CPRA** (California)
- 🇧🇷 **LGPD** (Brazil)
- 🇨🇳 **PIPL** (China)
- 🇬🇧 **UK GDPR**
- 🇦🇺 **Australian Privacy Act**
- 🌍 **General best practices** (jurisdiction-neutral)

---

## Disclaimer

This skill provides automated analysis for informational purposes only. It is **not legal advice** and does not substitute for a qualified privacy lawyer. Always consult a legal professional for compliance-critical decisions.

---

## Contributing

PRs welcome. Useful contributions:
- New jurisdiction checklists (PIPEDA, PDPA, etc.)
- Additional audit dimensions (accessibility, security headers, etc.)
- Improved GDPR checklist items
- Better artifact UI

---

## License

MIT
