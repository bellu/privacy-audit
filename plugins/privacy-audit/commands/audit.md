# /privacy-audit:audit

Run a full privacy & legal compliance audit on your project.

## Usage

```
/privacy-audit:audit
/privacy-audit:audit --url https://yourapp.com/privacy
/privacy-audit:audit --jurisdiction ccpa
```

## What this command does

1. **Scans your codebase** to automatically extract your app's actual data practices:
   - Reads `package.json` / `requirements.txt` to identify third-party services (analytics, auth, payments, email, AI APIs, etc.)
   - Reads your database schema (Prisma, SQL migrations, Mongoose models) to find PII fields
   - Reads API routes and frontend code to identify data collection points

2. **Reads your legal documents** — either from files in the repo (`/public/privacy-policy.md`, etc.) or from a URL you provide

3. **Runs the audit** comparing app reality vs. legal claims:
   - 🔴 Critical gaps (legal risk)
   - 🟡 Important gaps (compliance risk)
   - 🟢 Minor issues (best practice)
   - ✅ GDPR checklist (38 requirements)

4. **Produces two outputs**:
   - A downloadable markdown report
   - An interactive artifact for sharing

## Options

| Flag | Description |
|---|---|
| `--url <url>` | Fetch privacy policy from a URL instead of looking in the repo |
| `--jurisdiction <name>` | Add jurisdiction-specific checks: `gdpr` (default), `ccpa`, `lgpd`, `uk-gdpr`, `all` |
| `--docs-only` | Skip code analysis, audit documents against each other only |
| `--skip-artifact` | Skip interactive artifact, produce markdown report only |

## Examples

```
# Full audit — reads code + looks for legal docs in /public
/privacy-audit:audit

# Audit with remote privacy policy
/privacy-audit:audit --url https://myapp.com/privacy-policy

# Multi-jurisdiction audit
/privacy-audit:audit --jurisdiction all

# Quick doc-only audit (no code scanning)
/privacy-audit:audit --docs-only --url https://myapp.com/privacy
```
