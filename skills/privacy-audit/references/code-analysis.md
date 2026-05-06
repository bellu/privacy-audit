# Code Analysis Reference

Patterns for extracting privacy-relevant data practices from source code, by tech stack and file type.

---

## Strategy: What to Fetch First

When given a GitHub repo URL, fetch files in this priority order:

1. `package.json` (Node/JS) or `requirements.txt` / `pyproject.toml` (Python) or `Gemfile` (Ruby) — reveals all third-party services
2. `.env.example` or `config/` — reveals integrations and infrastructure
3. Database schema: `prisma/schema.prisma`, `schema.sql`, `db/migrate/`, `models/`, `drizzle/`
4. Auth files: `lib/auth.ts`, `app/api/auth/`, `middleware.ts`, `config/passport.js`
5. API routes: `app/api/`, `pages/api/`, `routes/`, `controllers/`
6. Frontend tracking: `lib/analytics.ts`, `components/Analytics`, `_app.tsx`, `layout.tsx`
7. Storage: any file referencing S3, Cloudinary, Supabase Storage, GCS

Construct raw GitHub URLs like:
`https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{filepath}`

---

## Dependency Analysis (package.json / requirements.txt)

### Analytics & Tracking
| Package | Service | Data implication |
|---|---|---|
| `@segment/analytics-next`, `analytics` | Segment | Behavioral tracking, event data |
| `mixpanel-browser`, `mixpanel` | Mixpanel | User behavior, funnels |
| `@amplitude/analytics-browser` | Amplitude | Product analytics |
| `react-ga4`, `gtag` | Google Analytics 4 | Pageviews, events, IP address |
| `posthog-js`, `posthog-node` | PostHog | Full session data, feature flags |
| `@vercel/analytics` | Vercel Analytics | Pageviews, Web Vitals |
| `hotjar` | Hotjar | Session recordings, heatmaps — HIGH privacy impact |
| `fullstory` | FullStory | Full session replay — HIGH privacy impact |
| `clarity-js` | Microsoft Clarity | Session recordings |

### Authentication
| Package | Service | Data implication |
|---|---|---|
| `next-auth`, `@auth/core` | NextAuth / Auth.js | Sessions, OAuth tokens, user accounts |
| `@clerk/nextjs`, `@clerk/clerk-sdk-node` | Clerk | User identity, MFA, sessions |
| `@supabase/auth-helpers-*` | Supabase Auth | User accounts, sessions |
| `passport` | Passport.js | Custom auth — check strategies |
| `firebase` | Firebase Auth | Google-managed identity |
| `auth0` | Auth0 | User identity, enterprise SSO |
| `lucia` | Lucia Auth | Sessions, custom user tables |

### Databases & Storage
| Package | Service | Data implication |
|---|---|---|
| `@supabase/supabase-js` | Supabase (PostgreSQL) | Check schema for PII |
| `prisma`, `@prisma/client` | Prisma ORM | Check `schema.prisma` for data model |
| `mongoose` | MongoDB | Check models/ for PII fields |
| `drizzle-orm` | Drizzle ORM | Check schema files |
| `@planetscale/database` | PlanetScale (MySQL) | Check schema |
| `@aws-sdk/client-s3`, `aws-sdk` | Amazon S3 | File storage — what types of files? |
| `cloudinary` | Cloudinary | Image/video storage |
| `uploadthing` | UploadThing | File uploads via S3 |

### Email & Communications
| Package | Service | Data implication |
|---|---|---|
| `@sendgrid/mail`, `sendgrid` | SendGrid | Email addresses, send logs |
| `resend` | Resend | Email addresses |
| `nodemailer` | SMTP (custom) | Email addresses |
| `@mailchimp/mailchimp_marketing` | Mailchimp | Email lists, marketing data |
| `postmark` | Postmark | Transactional email |
| `twilio` | Twilio | Phone numbers, SMS |

### Payments
| Package | Service | Data implication |
|---|---|---|
| `stripe`, `@stripe/stripe-js` | Stripe | Payment data, billing info, customer ID |
| `@paddle/paddle-js` | Paddle | Payment data, VAT/tax info |
| `lemonsqueezy` | LemonSqueezy | Payment data |

### Error Tracking & Monitoring
| Package | Service | Data implication |
|---|---|---|
| `@sentry/nextjs`, `@sentry/node` | Sentry | Error logs, stack traces, may capture PII |
| `@bugsnag/js` | Bugsnag | Error data |
| `newrelic` | New Relic | Performance + error data |
| `datadog-lambda-js`, `dd-trace` | Datadog | Logs, traces, metrics |
| `logtail`, `@logtail/node` | Logtail/BetterStack | Logs — may contain PII |

### AI & ML
| Package | Service | Data implication |
|---|---|---|
| `openai` | OpenAI API | User inputs sent to OpenAI — HIGH privacy impact |
| `@anthropic-ai/sdk` | Anthropic API | User inputs sent to Anthropic |
| `@google-cloud/aiplatform`, `@google/generative-ai` | Google AI | User inputs sent to Google |
| `replicate` | Replicate | User inputs/images sent externally |
| `langchain`, `@langchain/core` | LangChain | Check what data flows through chains |

### Feature Flags & A/B Testing
| Package | Service | Data implication |
|---|---|---|
| `launchdarkly-js-client-sdk` | LaunchDarkly | User context, feature flag data |
| `@growthbook/growthbook` | GrowthBook | A/B test exposure |
| `statsig-js` | Statsig | User exposure, event data |

---

## Schema Analysis (Prisma / SQL / Mongoose)

Look for models/tables containing:

**Direct PII:**
- `email`, `phone`, `name`, `firstName`, `lastName`
- `address`, `city`, `country`, `postalCode`
- `birthDate`, `dateOfBirth`, `age`
- `avatar`, `profileImage`, `photo`
- `ipAddress`, `userAgent`

**Indirect / Behavioral PII:**
- `session`, `token`, `refreshToken`, `accessToken`
- `deviceId`, `fingerprintId`
- `clicks`, `pageviews`, `events`
- `searchQuery`, `searchHistory`

**Sensitive categories:**
- `healthData`, `medicalRecord`, `condition`
- `paymentMethod`, `cardLast4`, `stripeCustomerId`
- `location`, `latitude`, `longitude`, `geoPoint`
- `salary`, `income`, `creditScore`

**For each PII table/model, note:**
- Is there a `deletedAt` / soft delete? → data retention practice
- Is there a `createdAt`? → data retention auditable
- Are there cascade deletes? → right to erasure implementation

---

## API Route Analysis

For each POST/PUT route, check:
- What fields are accepted in the body? → data collected
- Is the request body logged? → logging of PII
- Is any data forwarded to a third-party SDK? → subprocessor disclosure needed
- Is there IP address capture (`req.ip`, `x-forwarded-for`)? → network data collection

---

## Frontend / Client-Side Analysis

Look for:
- `document.cookie` or `js-cookie` or `cookies-next` → cookie usage
- `localStorage.setItem` / `sessionStorage` → client-side storage
- Analytics `track()` / `identify()` calls → what events and user properties are tracked
- Form fields: `<input type="email">`, `<input name="phone">` etc. → PII collection points
- `navigator.geolocation` → location access
- `getUserMedia` → camera/mic access
- Script tags loading external resources → third-party trackers

---

## Infrastructure Signals

From env vars / config:
- `DATABASE_URL` containing `supabase.co`, `planetscale.aws`, `mongo.net` → cloud DB provider + region
- `AWS_REGION`, `GOOGLE_CLOUD_REGION` → data residency
- `NEXT_PUBLIC_*` vars → anything prefixed NEXT_PUBLIC is exposed client-side

From `vercel.json`, `netlify.toml`, `fly.toml`, `railway.json`:
- Deployment region → where data is processed
- Edge functions → data processed at edge (potentially many countries)

---

## Common Stack Profiles

### Next.js + Supabase + Stripe (typical SaaS)
Priority files: `package.json`, `prisma/schema.prisma` or Supabase migrations, `app/api/`, `lib/supabase.ts`, `lib/stripe.ts`, `middleware.ts`

### Next.js + Clerk + PlanetScale
Priority files: `package.json`, `middleware.ts`, `app/api/`, DB schema

### Rails + Devise + Heroku
Priority files: `Gemfile`, `db/schema.rb`, `config/routes.rb`, `app/controllers/`, `config/initializers/`

### Django + PostgreSQL
Priority files: `requirements.txt`, `models.py` (all apps), `settings.py`, `urls.py`, `views.py`

### React + Firebase
Priority files: `package.json`, `firestore.rules`, `firebase.json`, any `firebase.initializeApp()` call
