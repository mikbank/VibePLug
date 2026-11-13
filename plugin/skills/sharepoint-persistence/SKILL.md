---
name: sharepoint-persistence
description: "Design and verify SharePoint as the default persistence layer for a recreated Copilot Code app. Use for list/library mapping, project snapshots, metadata indexes, generated connector services, runtime identity, data migration, pagination, conditional writes, conflicts, partial saves and unknown write outcomes. Establish real connection evidence before claiming persistence works."
---

# Make SharePoint persistence reliable

SharePoint is the default durable store for this migration plugin. Choose a model that fits the business data and verify the exact connector route. Read `references/storage-contract.md` and `references/live-probes.md` before implementing writes.

## Establish the destination and connection

Identify the intended site, list and library from the current task and authorized tools. Ask for the destination if unknown; never adopt a historical attachment's site as a tenant-wide default. Check three separate layers: authoring-session access, target app connection/binding, and deployed app read/write using its actual runtime identity. A successful metadata read proves that operation only.

Discover the current generated services, supported actions, response shapes, path conventions and policy status. Normal app data calls go through Microsoft-generated connector services. Open-ended SharePoint HTTP actions can be blocked by default even when the connector is allowed. Do not bypass this with direct browser fetch, embedded tokens, an ad hoc proxy or policy changes.

Confirm a minimal real connection before provisioning optional structures. If discovering an existing list/library is possible, probe it with a read. If the required target does not yet exist, create only the minimal dedicated structure necessary for the authorized proof; defer optional indexes. Site inspection or list creation through an authoring tool does not prove runtime binding support.

Use delegated end-user access by default where supported; inspect the actual connection mode. A shared/service connection requires explicit understanding of whose rights the operation uses and equivalent backend enforcement of app-specific rules. Never claim users inherit per-user SharePoint rights when every request actually runs as a more privileged owner.

## Choose and explain a model

- Ordinary business records: SharePoint lists with indexed query fields and stable IDs; files in a document library. Preserve field types and reference IDs.
- Document/project aggregates: one complete JSON snapshot per stable project ID in a library, optionally with a list containing searchable metadata. The snapshot is authoritative and the index is rebuildable. Do not store every user's project in one shared JSON file.
- Read-only informational content: no persistence unless a feature requires it. Explain that SharePoint remains the default when durable data is added.

Define required fields, uniqueness, validation, identity/ownership, relationships, size/volume, access boundaries and expected write concurrency. SharePoint is not a general SQL transaction engine. Complex transactions, security rules, high write contention, realtime presence or scale can require a different approved design. Identify the exact mismatch, ask the business owner a focused question and proceed with independent work. Do not silently select Supabase, Dataverse or localStorage instead.

## Implement an app-owned persistence adapter

Define load, create, save, list and reconciliation operations against the generated services. Preserve full state including unknown fields; map metadata without making it authoritative accidentally. Generate and retain stable project and operation identities before writes. Preserve operation state through timeout recovery and session handoff.

For existing records use the loaded server revision with a genuinely conditional update when available. For new records require a supported atomic create/no-overwrite or unique-key mechanism. Do not use an overwrite by default. Merely comparing a revision in the browser has a race and does not enforce concurrency. An ETag obtained separately from content must refer to that same revision; use a verified atomic read or a revision check around retrieval.

If the permitted connector cannot express conditional writes or safe uniqueness, surface the limitation early. Ask about a supported operation, approved service design or a business-acceptable restricted usage model. Do not present a client-side lock as a guarantee. A permission restriction must be enforced, not just announced. Withhold a completed multi-user migration until its essential collaboration model is supported and verified.

## Handle outcomes accurately

Report distinct states: unsaved, saving, confirmed saved, failed, editing conflict, snapshot saved/index pending, and outcome unknown. Confirmed saved means the authoritative backend acknowledged the write. A local cache or a queued request is not saved.

File and index writes are separate operations. Write the authoritative snapshot first when using that design; if metadata fails, preserve the saved snapshot and queue an idempotent index repair. Do not tell the user the snapshot failed or retry it unnecessarily.

A timed-out write has an unknown outcome. Reconcile using its retained stable ID, operation ID, target path and expected revision before retrying. A missing item from a filtered or delayed listing alone may not settle the question. Never generate a new ID on retry, blindly repeat a create, or overwrite after an ambiguous response. Read retries may use bounded backoff; write retries must respect idempotency and reconciliation.

Treat pagination tokens as opaque and follow actual returned tokens. Preserve existing rows if a later page fails; show incomplete results rather than an empty successful list. Never claim an empty-page test validates populated pagination. Respect throttling and observed retry instructions.

## Prove with live data

Run the relevant probes in `references/live-probes.md` on clearly identified verification records under the migration's authorization. Prove save/load after refresh and in a fresh session, permissions and server conflict rejection. Keep fixtures and mocks for fault cases but label them simulated. Record unresolved writes for reconciliation and avoid deleting unrelated data. Cleanup only known verification records within the authorized test scope.
