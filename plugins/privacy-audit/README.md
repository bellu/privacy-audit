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

### Audit from URLs (no codebase needed)

No source code? Provide document URLs + app description:

```
/privacy-audit:audit
Privacy Policy URL: https://example.com/privacy
App description: Newsletter SaaS — collects emails, tracks opens via Mailchimp, payments via Stripe
```

Multiple documents:

```
/privacy-audit:audit
Privacy Policy URL: https://example.com/privacy
Terms of Service URL: https://example.com/terms
Cookie Policy URL: https://example.com/cookies
App description: Newsletter SaaS — collects emails, tracks opens via Mailchimp, payments via Stripe
```

Claude fetches the documents automatically and runs the full audit.

### Changing jurisdiction

By default the audit runs against GDPR (EU). To target a different jurisdiction, add it to your prompt:

```
/privacy-audit:audit
Target jurisdictions: CCPA
```

Multiple jurisdictions at once:

```
/privacy-audit:audit
Target jurisdictions: GDPR, CCPA, LGPD
```

Supported: GDPR, CCPA, LGPD, UK GDPR, PIPL, Australian Privacy Act.

See [commands/audit.md](./commands/audit.md) for all options and flags.

## What it checks

- Privacy Policy, Terms of Service, Cookie Policy, DPA
- GDPR (38-point checklist)
- CCPA, LGPD, UK GDPR, Australian Privacy Act
- Automatic code analysis: detects third-party SDKs, PII in DB schema, tracking in frontend

## Disclaimer

This plugin provides automated analysis for informational purposes only. It is not legal advice.
