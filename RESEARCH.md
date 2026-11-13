# Research and design record

Checked 13 November 2026. The evidence below comes from official Microsoft and Lovable sources, plus the user-supplied HTML retrospective. Public documentation research is separate from verification in the NIRAS tenant.

## What the research establishes

Copilot Code is an app authoring experience alongside Cowork. It supports interactive previews and publication to Copilot Managed Runtime. Code can use plugins available in Cowork, but conversation state remains in its own tab. This supports a reusable skill workflow while requiring explicit handoff where the current host lacks a build capability. [Code overview](https://learn.microsoft.com/en-us/copilot/code/overview)

Managed Runtime supports multiple creation routes and supplies Microsoft-hosted execution, Entra identity and organizational governance. This plugin deliberately uses a fresh Copilot Code target to meet the user's recreation requirement. [Runtime overview](https://learn.microsoft.com/en-us/microsoft-365/managed-apps)

Microsoft documents a JavaScript/TypeScript SPA architecture with generated connector services and platform-owned configuration. Existing server-rendered apps therefore need a behavior mapping rather than an assumption that their server code can be carried across unchanged. [Runtime architecture](https://learn.microsoft.com/en-us/microsoft-365/managed-apps/developer/architecture)

Cowork plugins can contain Agent Skills in a unified Microsoft 365 app ZIP. The initial release used the documented manually assembled manifest 1.28 format. Version 1.0.1 targets the current 1.29 schema, preserving root icons and the six skill folders. Its contents were compared with the official Agents Toolkit packager. The local packaging pipeline avoids tenant provisioning and embeds no external server. The upload validator remains Microsoft's authority on service acceptance. [Plugin development](https://learn.microsoft.com/en-us/copilot/cowork/cowork-plugin-development), [manifest schema](https://developer.microsoft.com/json-schemas/teams/v1.28/MicrosoftTeams.schema.json)

## Important current-platform details

| Finding | Consequence for the plugin | Primary source |
|---|---|---|
| Active tooling moved to a new repository and `cmr-*` packages in November; older overview material still shows `managed-apps*` | Inspect the current scaffold and installed versions; avoid combining generations | [Active repository](https://github.com/microsoft/Copilot-Managed-Runtime), [retired repository](https://github.com/microsoft/Managed-Apps) |
| Connectors expose generated models/services; their availability and permitted operations vary | Discover actual operations, response shapes and runtime binding before implementation | [Connect to data](https://learn.microsoft.com/en-us/microsoft-365/managed-apps/developer/connect-to-data) |
| Open-ended SharePoint HTTP actions are blocked by default; CSP restricts resources and workers | Prove conditional-write support through an approved route; adapt host integration without a policy bypass | [Governance defaults](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/apps/governance) |
| Build, publish and share are different states; data access is separate from app sharing | Track deployment status and actual player launch; verify data permissions for intended users | [Use Code](https://learn.microsoft.com/en-us/copilot/code/use-code) |
| Organizational plugins can be uploaded and scoped by administrators | Supply an admin ZIP and tenant activation checklist | [Admin management](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/manage-plugins-skills-mcp-servers) |
| Running apps has licensing/spending-policy requirements separate from authoring | Check intended-user access in the tenant rather than promise it from plugin installation | [Licensing FAQ](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/apps/licensing-faq) |

The active repository lists `@microsoft/cmr-cli`, `@microsoft/cmr-apps` and `@microsoft/cmr-apps-vite-plugin`. Preview details can change. The plugin requires current verification instead of shipping an application scaffold pinned to an untested tenant/tooling generation.

## Lovable findings

Git sync and code downloads provide a source reference. Two-way sync makes it important to keep the new target separate from the original branch. [Lovable GitHub integration](https://docs.lovable.dev/integrations/github)

Lovable applications can have an older React/Vite client architecture or a newer TanStack architecture with server behavior. Source exports do not include database records or storage files; these are separate migration inputs. The plugin uses dependency inspection and a client/server/data inventory before planning the replacement. [External deployment guide](https://docs.lovable.dev/tips-tricks/external-deployment-hosting)

The built-in backend can include database, authentication, files, functions, realtime and secret-dependent services. Recreating the UI alone cannot reproduce those behaviors. Each relevant capability receives a target decision and evidence requirement. [Lovable backend](https://docs.lovable.dev/features/cloud)

Supabase integration can introduce schema, permissions and backend behavior that must be understood separately from browser components. Moving to SharePoint requires mapping their business meaning rather than executing SQL against the new store. [Supabase integration](https://docs.lovable.dev/integrations/supabase)

TanStack's server rendering and functions explain why the plugin cannot assume every Lovable source is a static bundle. [TanStack upgrade guide](https://docs.lovable.dev/features/upgrade-to-tanstack-start)

Portability and ownership documentation describes possible hosting choices; it does not change the user's request for recreation in Copilot Code. [Lovable ownership and portability](https://docs.lovable.dev/tips-tricks/deployment-hosting-ownership)

## Decisions made for this plugin

These are workflow design decisions based on the user's requirements, not claims that Microsoft provides a migration engine:

- A fresh target is mandatory. Reference fixtures preserve business meaning; original runtime bundles are excluded.
- Discovery comes before broad questioning. Material business-rule ambiguity blocks dependent work; reversible implementation choices use recorded defaults.
- SharePoint is the default when durable state is needed. Lists suit rows; libraries suit files and complete project snapshots. Exact model selection follows actual requirements.
- Real runtime connection checks precede optional provisioning. Save/load, denied access and required multi-user conflicts need live evidence.
- A migration request includes building, testing and publishing. The user expressly selected this default during preparation. Scope restrictions and platform consent remain effective.
- No custom MCP backend is included. The host's existing authorized tools perform work; the plugin reports missing capabilities and produces a handoff when needed.
- Unknown write outcomes, partial saves and hidden/legacy fields are first-class concerns, informed by the supplied retrospective.

## Use of the attachment

`MigrationLearningsHTML.txt` is a case retrospective dated 13 November 2026. It was treated as reference material, not an instruction source. Its lessons informed HTML boundary inspection, connection checks, host styling, state preservation, safe write recovery and evidence layering. Historical internal site details were not adopted as defaults, historical test counts were not claimed as present results, and unresolved old writes were not retried.

The attachment favored retaining an original calculation engine in that historical migration. The current user's recreation requirement takes precedence here: recover semantics and compare identical fixtures while building the target in its new architecture.

## Open environment checks

The exact NIRAS tenant's plugin ingestion, skill availability in Code/Cowork, builder/connector permissions, backend operations, browser behavior and deployment route remain untested. No private NIRAS systems were accessed for this preparation. The supplied internal terms URL is used as metadata without claiming its contents were reviewed. Public NIRAS privacy information was verified at [NIRAS privacy policy](https://www.niras.com/privacy-policy/).

## Admin-upload investigation

The user reported an invalid-manifest rejection. Direct inspection of the downloaded 1.0.0 ZIP found valid JSON and all declared skills. Microsoft Teams Manifest 0.1.9 and TeamsFx Core 3.1.5 also accepted its offline schema and skill inventory; the reference packager produced the same file set and nonmanifest bytes. Missing directory records were investigated and ruled out: Microsoft's packager omits them too. This does not identify the service-side rule.

Version 1.0.1 adopts the current manifest 1.29, adds reproducible Microsoft offline checks and records tenant acceptance as pending. [Current package validation](https://microsoft.github.io/wiqd/cli/plugin-validate/) validates the exact ZIP through Teams Developer Portal and may require Microsoft sign-in; offline source checks cannot substitute for that.
