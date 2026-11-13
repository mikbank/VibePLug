# Release evidence template

- Target app ID and environment:
- Source commit/version and target commit/version:
- Publishing authorized by: migration request / explicit publish / scope limited
- Intended/current audience:
- SharePoint target and tested runtime identity:
- Material questions resolved; any intentional differences:

| Layer | Scenarios covered | Result | Artifact/time | What this does not prove |
|---|---|---|---|---|
| Domain fixtures | Original-versus-new rules and boundary cases | | | Live backend or browser behavior |
| DOM | Navigation and form events | | | Actual scrolling, native dialogs or pixels |
| Simulated persistence | Conflicts, timeouts and partial writes | | | Real SharePoint enforcement |
| Live backend | Exact connection, create/save/load, permissions, concurrency | | | Untested identities or operations |
| Actual host browser | Readability, core interactions and relevant file/print checks | | | Unexecuted devices or flows |
| Deployment | Terminal success and exact player launch | | | Untested feature parity |

- Final deployment ID/status:
- Actual published URL:
- Launch identity, browser and result:
- Outstanding criteria with impact and next action:
- Pending/unknown write operations and reconciliation plan:
- Data import totals, errors and rollback/source preservation:

A successful end-to-end path does not prove all features. Describe coverage in terms of scenarios and roles. Distinguish failed, blocked and not-run instead of treating them all as warnings under a green total.
