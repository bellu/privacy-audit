# 🔍 Privacy Audit — Claude Plugin

A Claude Code plugin (and Claude.ai skill) that audits whether your app's legal documents — Privacy Policy, Terms of Service, Cookie Policy, and DPA — actually reflect what your app does.

Built for indie developers, SaaS founders, and freelancers who want to ship compliant products without a lawyer on retainer.

---

## Installation

### Option A — Claude Code (recommended)

```bash
# Add this repo as a marketplace (one-time setup)
claude plugin marketplace add https://github.com/bellu/privacy-audit

# Install the plugin
claude plugin install privacy-audit
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

---

## Usage

**Claude Code:**
```bash
/privacy-audit:audit
/privacy-audit:audit --url https://yourapp.com/privacy
/privacy-audit:audit --jurisdiction ccpa
/privacy-audit:audit --jurisdiction all
```

**Claude.ai** — just talk naturally:
> *"Audit my privacy policy against my codebase"*
> *"Check my privacy policy for GDPR compliance — here's the URL: https://..."*
> *"Does my ToS reflect what my app actually does?"*

---

## What it checks

- Privacy Policy, ToS, Cookie Policy, DPA
- 🔴 Critical gaps — legal risk (undisclosed data collection, missing legal basis, etc.)
- 🟡 Important gaps — compliance risk (vague language, missing cookie disclosure, etc.)
- 🟢 Minor issues — best practice (outdated contact info, missing document version, etc.)
- ✅ 38-point GDPR checklist (Art. 6, 12–22, 28, 32, ePrivacy, cross-border transfers)

## Supported jurisdictions

🇪🇺 GDPR · 🇺🇸 CCPA/CPRA · 🇧🇷 LGPD · 🇨🇳 PIPL · 🇬🇧 UK GDPR · 🇦🇺 Australian Privacy Act

---

## Structure

```
privacy-audit/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── skills/
│   └── privacy-audit/
│       ├── SKILL.md           # Main skill instructions
│       └── references/
│           ├── gdpr-checklist.md
│           ├── jurisdictions.md
│           ├── code-analysis.md
│           └── artifact-template.md
├── commands/
│   └── audit.md              # /privacy-audit:audit command
├── privacy-audit.skill        # Prebuilt file for Claude.ai
└── package.py                 # Build script
```

---

## Disclaimer

Automated analysis only — not legal advice. Always consult a qualified privacy lawyer for compliance-critical decisions.

---

## License

MIT
