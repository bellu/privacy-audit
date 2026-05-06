# Interactive Audit Artifact — React Component Template

Use this as the scaffold for the interactive `.jsx` artifact. Adapt as needed.

## Component Structure

```
AuditApp
├── InputPanel (left/top)
│   ├── AppDescriptionTextarea
│   ├── DocumentTabs (Privacy Policy | ToS | Cookie Policy | DPA)
│   │   └── DocumentTextarea per tab
│   ├── JurisdictionSelector (checkboxes: GDPR, CCPA, LGPD, General)
│   └── RunAuditButton
└── ResultsPanel (right/bottom)
    ├── LoadingState (spinner + "Analyzing...")
    ├── ExecutiveSummary (card)
    ├── SeverityTabs (Critical 🔴 | Important 🟡 | Minor 🟢 | GDPR Checklist)
    │   └── FindingCard[] per tab
    │       ├── FindingTitle
    │       ├── AffectedDocument badge
    │       ├── WhyItMatters
    │       └── SuggestedFix (expandable)
    └── DownloadReportButton
```

## Key Implementation Notes

### API Call

```javascript
const runAudit = async () => {
  setLoading(true);
  setResults(null);

  const systemPrompt = `You are a privacy law and compliance expert. 
Analyze the provided app description and legal documents.
Return ONLY a valid JSON object with this exact structure:
{
  "summary": "2-3 sentence overall assessment",
  "appReality": {
    "dataCollected": [],
    "thirdParties": [],
    "storage": "",
    "userRights": []
  },
  "criticalGaps": [
    {
      "title": "",
      "affectedDoc": "",
      "whyItMatters": "",
      "suggestedFix": ""
    }
  ],
  "importantGaps": [...same structure...],
  "minorIssues": [...same structure...],
  "gdprChecklist": [
    {
      "requirement": "",
      "status": "ok|partial|missing|na",
      "notes": ""
    }
  ],
  "nextSteps": []
}
No markdown, no backticks, no preamble. Pure JSON only.`;

  const userPrompt = buildUserPrompt(appDescription, documents, jurisdictions);

  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1000,
      system: systemPrompt,
      messages: [{ role: "user", content: userPrompt }]
    })
  });

  const data = await response.json();
  const text = data.content.map(i => i.text || "").join("");
  const parsed = JSON.parse(text);
  setResults(parsed);
  setLoading(false);
};
```

### buildUserPrompt

```javascript
const buildUserPrompt = (appDescription, documents, jurisdictions) => {
  let prompt = `APP DESCRIPTION:\n${appDescription}\n\n`;
  
  if (documents.privacyPolicy) 
    prompt += `PRIVACY POLICY:\n${documents.privacyPolicy}\n\n`;
  if (documents.tos) 
    prompt += `TERMS OF SERVICE:\n${documents.tos}\n\n`;
  if (documents.cookiePolicy) 
    prompt += `COOKIE POLICY:\n${documents.cookiePolicy}\n\n`;
  if (documents.dpa) 
    prompt += `DPA:\n${documents.dpa}\n\n`;
  
  prompt += `TARGET JURISDICTIONS: ${jurisdictions.join(", ")}\n\n`;
  prompt += `Perform a comprehensive audit and return the JSON report.`;
  
  return prompt;
};
```

### Download Report

```javascript
const downloadReport = () => {
  const md = generateMarkdownReport(results, appName);
  const blob = new Blob([md], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `privacy-audit-${Date.now()}.md`;
  a.click();
};
```

### generateMarkdownReport

Convert the parsed JSON back to the structured markdown format defined in SKILL.md Format A.

## Styling Notes

- Use Tailwind utility classes only (no custom CSS)
- Severity colors: red-500 (critical), yellow-500 (important), green-500 (minor)
- Status colors for GDPR checklist: green (ok), yellow (partial), red (missing), gray (na)
- Keep the layout clean and scannable — this is a professional tool
- On mobile: stack input/results vertically; on desktop: side-by-side or tabbed
