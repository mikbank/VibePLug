# Parity and acceptance template

| Feature/rule ID | Source evidence | Expected scenario/result | Target location | Test layer | Actual result | Evidence artifact/time | Status |
|---|---|---|---|---|---|---|---|

Status values: passed, failed, blocked, not-run, not-applicable. An inference is not a passed test. Link user decisions for intentional differences.

Separate these layers: deterministic domain/fixture, DOM interaction, simulated storage contract, live SharePoint/backend, real browser in actual host, and deployment/player launch. Report meaningful coverage and limitations for each, rather than one combined green count.

Minimum release criteria, tailored to the actual app:

- Core workflow and calculations match reference fixtures; material rule questions resolved.
- Target is a fresh native implementation; no unchanged source bootstrap or Lovable runtime dependency unless an explicitly agreed external integration requires one.
- Required data survives save, refresh and a fresh browser session on the exact destination.
- Permissions prevent unauthorized reads and writes at the backend, including direct record access.
- Multi-user updates have live, server-enforced conflict evidence, or an explicit user-agreed restricted usage model that fits the business need. Never claim client-only conflict detection is safe collaboration.
- Relevant populated pagination, partial writes, write timeouts, legacy data and file round trips checked.
- Actual host is readable and core interactions work, including relevant dialogs, scrolling, keyboard, imports and print.
- Build/type/lint checks supported by the scaffold pass; remaining warnings are described.
- Final deployment succeeded and the exact player URL launches with the intended identity.

For a stateless page, mark persistence and concurrency not-applicable with the reason. Do not hide a failed core criterion in a handoff footnote. Continue fixing it or identify the precise blocker and withhold the completed-migration claim.
