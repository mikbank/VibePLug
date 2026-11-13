# Per-session capability record

| Capability | Evidence needed | State and evidence |
|---|---|---|
| Source inspection | Local source/export or authorized repository read; version captured | |
| New target authoring | Actual managed-app builder or compatible scaffold; separate app/project ID | |
| Tooling | Version and compatible scaffold, current help/API definitions | |
| SharePoint read | Bound exact site/list/library and successful runtime call | |
| SharePoint write | Authorized stable test record saved and reloaded | |
| Permissions | Actual runtime user and denied-access test | |
| Concurrency | Conditional operation available and stale revision rejected live | |
| Server behaviors | Supported integration for every privileged/background action | |
| Browser/host | Exact preview/player, theme, CSP and interactions checked | |
| Deployment | Real publish tool, successful terminal status, app/version and launch URL | |
| Audience | Explicit existing/intended users, app rights and separate data rights | |

States: verified / documented-only / unavailable / blocked / not-applicable. Avoid treating an API name found in documentation as a working session capability.

If a capability is missing, record what was attempted, the actual error, what independent work remains possible and the smallest user/admin action needed. Do not invent tool invocations, bypass policy with raw fetch, or automatically recommend a new external service.
