# Migration record template

Copy to the target workspace and update after each phase. Do not store credentials, tokens or unnecessary personal data here.

- Status: discovery / building / awaiting-business-rule / blocked / verification / deployed
- User objective and exclusions:
- Source platform, immutable commit/version and hashes:
- Available source, runtime and data access; missing evidence:
- Target app ID, project/repository, environment and host:
- Tools/SDK/CLI versions checked; source URLs and date:
- Publishing scope: migration includes publishing unless user limited it
- Intended audience and existing sharing scope:
- Persistence: exact SharePoint site, list/library IDs, authoritative store:
- Connection identity and read/write operations verified:
- Feature/rule matrix location and fixtures:
- New target architecture and source-to-target map:
- Data migration scope, source counts, target counts, rejected rows and identity map:
- Last completed action and next independent action:
- Preview URL (label preview):
- Deployment ID/status, commit/version and confirmed player URL:

| Rule ID | Rule or question | Evidence path/lines or observation | Status/confidence | Impact if wrong | User answer/default | Dependent work |
|---|---|---|---|---|---|---|

| Operation ID | Stable record/project ID | Target path | Expected revision | Outcome: confirmed/failed/unknown | Reconciliation evidence | Next action |
|---|---|---|---|---|---|---|

Keep pending writes across retries and session handoffs. A timeout stays unknown until authoritative evidence reconciles it. Never create a new ID just because the response was lost.

| Change from source behavior | Reason | User decision or reversible assumption | Validation |
|---|---|---|---|

Resume by reading this record and checking current source, target, deployment and pending-write state. Do not rerun unknown writes, bulk imports or deployments merely because a previous session ended.
