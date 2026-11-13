---
name: copilot-managed-app-capabilities
description: "Assess what Microsoft Copilot Code and Copilot Managed Runtime can support before building or migrating an app from any platform. Use for managed-app architecture, connectors, runtime limitations, Entra identity, SharePoint storage, source access, host behavior, tooling or publishing capability questions."
---

# Establish actual platform capabilities

Use this skill before committing to a migration architecture and when the user asks what managed apps can do. Read `references/platform-facts.md` for the researched baseline and `references/capability-check.md` for a per-session checklist. The platform is evolving; verify a dated statement against current official documentation and actual tool/connector signatures before making implementation decisions.

## Distinguish the surfaces

Copilot Code is the Microsoft Code experience used to author the new app. Cowork can use the migration skills to inspect and coordinate work. Copilot Managed Runtime hosts the resulting app. The admin-uploaded plugin is a separate Microsoft 365 skills package; uploading it does not deploy an app or provision a SharePoint connection. GitHub Copilot and the local `ms` CLI are development routes, not interchangeable names for Copilot Code.

A skills-only plugin relies on the host's authorized tools. Discover whether this session can read source, edit/build a new app, inspect it in a browser, bind SharePoint and publish to Managed Runtime. Code and Cowork conversation state does not automatically move between tabs. If direct target building is unavailable, generate a handoff and explicitly identify the step that must continue in Code. Never pretend a ZIP of skills creates APIs or access rights.

## Verify before choosing an architecture

1. Identify the tenant/environment, existing target app and user's requested scope. Check actual availability of Code, app builder, approved connectors, end-user licensing and permissions. Do not ask the user for secrets in chat; use the platform's supported sign-in/connection flow.
2. Inspect a current fresh scaffold and its package manifest. As researched on 13 November 2026, Microsoft's active repository is `microsoft/Copilot-Managed-Runtime`; it lists `@microsoft/cmr-cli`, `@microsoft/cmr-apps` and `@microsoft/cmr-apps-vite-plugin`. Older Learn pages and examples still name `@microsoft/managed-apps*`. Do not mix generations or mass-rewrite an existing supported target. Check the installed versions, repository README and current Microsoft docs, then use one compatible scaffold.
3. Use current host tools where available. For a CLI workflow, inspect `ms --version`, `ms --help` and the relevant subcommand help before mutating anything. Create a separate target with the supported create/init flow. Do not initialize or deploy the Lovable source repository as the migration result.
4. Prefer generated connector models/services. Discover permitted SharePoint tables/actions; bind through the builder or CLI and inspect generated definitions and actual response shapes. Do not fabricate services, copy old sample signatures, hand-edit generated code or manually patch platform-owned configuration.
5. Check required server behavior against the SPA target: privileged operations, webhooks, schedulers, secret use, server functions, transactions, realtime and external APIs each need a supported governed route. Do not put secrets or privileged authorization in browser code. If an essential requirement has no suitable route, explain the gap and ask about scope or an approved backend option.
6. Verify host policies and behavior before promising compatibility: external fonts/scripts, inline JavaScript, workers, frames, file APIs, print, popups, browser shortcuts and theme tokens. Bundle allowed dependencies and move inline handlers into compiled code. Never loosen tenant policies as an incidental migration fix.

## Useful discovery commands

These documented examples are prompts for discovery, not permission to invoke unknown versions or change an environment. Check local help first:

```text
ms --version
ms connector list --search sharepoint
ms connector list-actions --connector shared_sharepointonline
ms app add data-source --help
ms app refresh data-source --help
ms app dev --help
ms app deploy --help
```

Register connections through platform tooling; generated `generated/` services and `ms.config.json` are owned by that tooling. A connector visible to Cowork's authoring session is not proof the deployed app can call it. Test the exact site, operation and runtime identity.

## Answer capability questions precisely

Classify each required feature as verified in this session, documented but unverified here, requires an approved integration, or unresolved. Include the evidence and next probe for unresolved requirements. SharePoint is the default for persistence, not a relational database substitute in every case. Preserve SQL policy intent and state transitions; do not assume Entra sign-in alone provides application authorization.

Building, previewing, saving source, deployment and sharing are separate states. A final run link requires successful deployment, and source sharing does not grant access to underlying data. Keep app audience and data permissions explicit. Reuse existing authorizations; allow Microsoft to enforce its own consent and admin controls.
