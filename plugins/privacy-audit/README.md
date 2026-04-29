# privacy-audit plugin

Audit your app's legal documents against its actual data practices.

## Install

```bash
# Add the marketplace
claude plugin marketplace add https://github.com/bellu/privacy-audit

# Install the plugin
claude plugin install privacy-audit@privacy-audit
```

## Usage

Once installed, run from inside your project:

```bash
/privacy-audit:audit
```

Claude will scan your codebase, read your legal documents, and produce a full compliance report.

See [commands/audit.md](./commands/audit.md) for all options and flags.

## What it checks

- Privacy Policy, Terms of Service, Cookie Policy, DPA
- GDPR (38-point checklist)
- CCPA, LGPD, UK GDPR, Australian Privacy Act
- Automatic code analysis: detects third-party SDKs, PII in DB schema, tracking in frontend

## Disclaimer

This plugin provides automated analysis for informational purposes only. It is not legal advice.
