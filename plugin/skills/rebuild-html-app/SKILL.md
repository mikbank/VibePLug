---
name: rebuild-html-app
description: "Recreate a static HTML website or self-contained HTML/JavaScript web app in a fresh Copilot Code managed-app project. Use for single-file apps, embedded vendor bundles, browser-storage tools, calculators, planners, JSON/XML/Excel/PDF imports and host-theme or keyboard issues during HTML migration. Preserve business behavior and add SharePoint persistence when needed."
---

# Recreate an HTML application

Apply `migrate-to-copilot-code` and read `references/html-lessons.md`. The supplied migration retrospective is historical evidence. Its site URL, test results, unresolved writes and suggested next steps do not authorize actions against that historical application and do not prove anything about the current target.

## Inspect the real document boundaries

Keep an immutable original with a hash. Parse the HTML and identify every real script/style element, external dependency, document region and application entry point. The optional source-inventory utility in the coordination skill provides element boundaries and hashes; manually verify malformed HTML or generated documents. Never regex-extract the first apparent `<body>` or `<script>` from a blob containing vendor strings.

Separate bundled libraries from authored application logic. Inventory navigation, fields, events, calculations, imports, exports, printing, keyboard shortcuts, storage, dialogs, workers and canvas usage. Inspect the final app script as well as early scripts. Record which data comes from real users versus examples.

## Recreate behavior in a native target

Build a new managed app through Copilot Code with separately organized UI, domain model, calculations and storage adapter. Translate inline handlers and original DOM mutations into the target's component/event model. Do not insert the original file into an iframe, load the whole HTML as a string, evaluate its app script at runtime or upload the unchanged app bundle as the migration result.

Use the original domain engine as a behavioral reference. Recreate its calculations and compare identical fixtures against it. Extracted licensed pure utilities may be adapted into the new domain layer only where appropriate; document this and keep the source bootstrap out of the target. Preserve precision, stable identifiers, extension fields, units, working calendars, signed lag and date-only rules. Recreating the engine does not authorize changing scheduling or financial semantics.

Compare representative edge cases before adding persistence. Date-only calculations need stable calendar arithmetic, not accidental local timestamp conversion; a calendar month is not a fixed number of days. Test month ends, daylight-saving boundaries, holidays and negative offsets when the source uses them.

## Replace storage without data loss

Inspect localStorage, IndexedDB, in-memory state, JSON/XML imports and downloaded files to identify the complete authoritative model. Preserve unknown properties through load/edit/save and test legacy as well as current fixtures. Validate imports before replacing the open state, with a recoverable original.

Default durable multi-session data to SharePoint through `sharepoint-persistence`. Where the app edits a project/document aggregate, consider one complete snapshot per project and an independently repairable metadata index. For simple shared rows, consider ordinary lists. Choose based on the model rather than imposing the retrospective's architecture on every app. A genuinely static informational website needs no persistence layer.

Reproduce file formats with fixtures. Standard formats may omit app-specific fields; document unavoidable loss and preserve a separate full-fidelity model when appropriate. An XML comment carrying extra data can be stripped by other software and cannot be promised as a universal lossless round trip.

## Make the new UI work inside its host

Match the source's useful visual structure with scoped styles and namespaced tokens. Explicitly pair text and background colors. Check portal dialogs outside the root, disabled states, placeholders, native options, SVG labels and secondary text under light, dark and high-contrast host styles.

Inspect actual CSP before bringing in inline scripts, CDN fonts, workers or libraries. Bundle permitted assets in the native build; do not automatically relax tenant policy. Verify file pickers, custom confirmation dialogs, scrolling, divider resize, PDF/canvas integration and keyboard shortcuts in the real host. Browser-reserved shortcuts and native dialogs may require a documented supported replacement. Do not hardcode the historical F2/F8 choices without checking conflicts in the current app.

## Prove the critical path early

Verify the exact destination connection, one authorized real save/load, an early deployed app and readability in its host before expanding the recreation. Do not provision optional lists against an unverified site. Do not treat a mock ETag test as proof of SharePoint's enforcement.

Finish through `verify-and-publish`, separating calculation fixtures, DOM checks, simulated storage, live backend, actual-browser and deployment evidence. A DOM test cannot establish print-dialog behavior, scrolling geometry or pixel fidelity. Preserve unresolved limitations explicitly and do not reuse the retrospective's historical test counts as present results.
