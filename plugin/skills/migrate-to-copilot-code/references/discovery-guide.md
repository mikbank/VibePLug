# Source discovery

Start with the source tree, package/configuration files and routes. Distinguish authored code from vendors, build output, generated files and sample data. Trace at least one create/edit/save/read and one permission-sensitive flow through every layer. Keep originals immutable and record provenance.

| Area | Inspect | Capture |
|---|---|---|
| Purpose | Landing screen, navigation, usage docs, sample records | Business outcome, personas, main tasks |
| UI | Routes, forms, dialogs, grids, empty/error/loading states | Workflow steps and validation |
| Rules | Services, reducers, calculations, conditions, constants, tests | Inputs, outputs, units, rounding, exceptions |
| State | Browser storage, DB schema, API calls, saved files | Authoritative data, IDs, hidden/legacy fields |
| Security | Auth, API middleware, SQL policies, ownership | Read/create/edit/delete rights per role |
| Services | Server functions, jobs, webhooks, payments, AI | Triggers, side effects, secrets needed by name only |
| Files | Imports, exports, attachments, third-party libraries | Formats, lossiness, representative fixtures |
| Host | Keyboard, print, dialogs, workers, external resources | Embedded-host and CSP dependencies |
| Delivery | Current deployment, intended users, build setup | New target scope and launch verification |

For an unfamiliar platform, identify its stack from the actual dependencies and entry points, not the platform's marketing. Inspect both client and server directories. Search for data mutations, permission checks, calculations and import/export code. Read dependency manifests before executing anything; do not run package lifecycle hooks just to list files. Any source execution uses the host's isolated development path after reviewing scripts.

Create 3-8 representative reference fixtures per important workflow, scaled to risk: normal, boundary, error and role-restricted cases. Ask for examples if source or tests cannot establish expected outcomes. Do not ask the user to enumerate every feature before exploring.

Preserve UI-visible fields and extension/legacy fields. Imported data that the current UI does not expose can still be part of the contract. Preserve identity mappings, exact decimal/money requirements, timezone versus date-only meaning, locale, null versus empty and enum distinctions.

When only a rendered URL is available, inspect permitted pages and interactions without destructive actions. Record inaccessible screens and unknown backend behavior. Request the source export and data/permission information needed to close the gaps; a screenshot resemblance is not full parity.
