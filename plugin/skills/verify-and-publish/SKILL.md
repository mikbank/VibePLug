---
name: verify-and-publish
description: "Verify and publish a recreated Copilot Code managed app after migration. Use for feature parity, original-versus-new fixtures, live SharePoint evidence, real-host visual and interaction checks, deployment status, player links and migration handoff. Publishing is included when the user requests a migration unless they limit the scope."
---

# Verify the new app and publish it

Use this skill at the first end-to-end slice and again after final changes. Read `references/release-evidence.md`. Work autonomously through checks and fixes already authorized by the migration. A request to migrate includes publishing by default; respect preview-only or other explicit limits. Microsoft platform consent and existing tenant policy still apply.

## Verify behavior at the right layer

Compare original and target with identical representative fixtures and user-confirmed rules. Cover normal flows, edge cases, validation, relevant roles, state transitions and error recovery. Use source code, recorded examples and actual behavior as evidence. Do not create expected values by copying the new implementation's results.

For financial, scheduling or other nontrivial logic, use deterministic tests for rounding, calendars, units and boundary inputs. For data and files, verify unknown/legacy fields, stable IDs and JSON/XML or other round trips with representative fixtures. Include an intentional-difference log when exact parity is not feasible or the user chose a change.

Run build, type and lint checks appropriate to the target scaffold. Inspect generated dependency/configuration alignment and remove accidental source runtime URLs, source bootstraps, copied secrets and Lovable/Supabase runtime dependencies outside explicitly agreed integrations. Do not hand-edit generated services to make a type check pass.

## Verify the real connection and host

Apply `sharepoint-persistence` for live runtime read/write, reload/new-session, actual denied permissions and stale-revision rejection where collaboration is required. Simulated fault tests are useful but cannot verify server enforcement or connection readiness. Do not mark a backend gate passed from mocks.

Open the actual managed preview/player in a browser when tools allow. Check light, dark and relevant accessibility modes; root and portal colors; navigation, dialogs and main actions; and relevant scroll/resize/keyboard/file/print behavior. Include CSP/resource failures and browser console errors. DOM-only checks cannot establish geometry, real file pickers or native print behavior.

Treat missing business data exports, unimplemented server functions or failed security as substantive gaps even if the UI looks complete. Do not publish a broken replacement as a completed migration. Keep the target preview and continue independent fixes when a critical dependency is blocked.

## Publish within scope

1. Read the app's current ID, environment, deployment state and existing audience. Use that target; do not accidentally create a second app on retry.
2. Confirm core acceptance criteria with current evidence. A new app without durable data requirements can mark persistence not-applicable with a reason. Noncritical unverified behavior must be explicit; essential business and security gaps block the completed release.
3. Use the current host publish operation or supported CLI deployment flow, inspecting help/schema first. Record the source commit/version and returned deployment identifier. Do not substitute a successful local build, source save or Git push for confirmed deployment.
4. Observe the actual deployment until terminal success or failure. Do not repeat a still-running publish. Diagnose failure using its error and preserve the same app identity.
5. Retrieve the actual published player URL from the platform; never construct or guess it. Open that exact URL with the intended identity when browser access permits. If the platform confirms deployment but browser verification is unavailable, state both facts separately.
6. Preserve the audience already specified. When none is defined, publish within the maker's existing restricted scope and report it. Sharing more broadly, replacing the original app's traffic, disabling its services or deleting source data requires that scope to have been requested; do not infer it from the act of publishing.

An early end-to-end version can be published within the same restricted target scope while development continues. Label its incomplete coverage and do not call the migration finished. Publish the final verified changes to the same app before handing over the final link.

## Handoff

Lead with the outcome and link, then give concise evidence and limitations. Provide a business-readable feature summary, the actual SharePoint location, important user decisions, any change in workflow, and explicit unresolved criteria. Keep technical details in the migration record and evidence matrix.

If publication or a critical check is blocked, deliver the concrete target implementation, parity matrix, fixtures, connection/setup instructions and the precise remaining step. Label preview/source artifacts correctly, state that migration is incomplete and do not claim the plugin granted the missing capability. Never reuse historical test counts from attached notes.
