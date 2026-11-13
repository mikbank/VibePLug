# App-owned adapter contract

This is a conceptual contract for the new app, not a Microsoft SDK API. Bind it to generated operations only after inspecting their real signatures. No hardcoded SharePoint REST workaround is supplied.

```text
load(id) -> { completeModel, serverRevision }
create(id, completeModel, operationId) -> confirmed(newRevision) | conflict | failed | unknown
save(id, completeModel, expectedRevision, operationId)
  -> confirmed(newRevision) | conflict | failed | unknown
list(cursor?) -> { rows, nextCursor?, completeness }
reconcile(id, operationId, target, expectedRevision) -> outcome + authoritativeEvidence
repairIndex(id, confirmedSnapshotRevision) -> repaired | pending | failed
```

Each operation must preserve the identity, read/content revision pairing, unknown properties and backend permission semantics. A row/file's latest revision alone may not establish which timed-out operation wrote it; preserve an operation marker in the authoritative model when appropriate and verify the expected content/version.

| Outcome | User-visible state | Next action |
|---|---|---|
| Authoritative write acknowledged | Confirmed saved | Store returned revision; update repairable metadata |
| Index write fails after acknowledged snapshot | Saved; metadata update pending | Repair index without rewriting snapshot |
| Stale revision rejected | Editing conflict | Keep local work; offer latest reload, continue editing or save as separate project |
| Definite permission/validation rejection | Save failed | Preserve local state and show actionable cause |
| Timeout or lost acknowledgement | Outcome unknown | Retain IDs; reconcile against authoritative target |
| Later page fails | Partial listing | Keep fetched rows and offer continuation/retry |

Do not equate a transport timeout with a negative backend acknowledgement. Do not overwrite remote changes when retrying. Reloading after conflict requires preserving or explicitly discarding local work; saving a separate project creates a new intentional identity, unlike blindly retrying an uncertain create.

Snapshot metadata might include project ID, title, owner identity, schema version, modified date and snapshot locator/revision. Store the complete business model in the snapshot, not just UI-visible fields. For list-based records choose indexed query fields and follow server-side paging; a list view threshold is a query-design concern, not a universal maximum list size.
