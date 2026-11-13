# Live probe checklist

Use dedicated identifiable test data and log evidence without secrets. Follow the current migration authorization and host consent model; do not repeatedly seek approval for already authorized reversible tests.

1. Record the exact site, list/library, generated service version, operation, runtime identity and time. A historical site URL is not a target selection.
2. Read through the target app connection. Confirm response shape and fields. Do not infer a file read/write from a list metadata read.
3. Generate a stable test record/project ID and operation ID. Create once without overwrite. Confirm authoritative acknowledgement and resulting revision.
4. Reload in the app, refresh the page, and open a fresh authorized session. Check the complete model and identifiers, including hidden/legacy properties.
5. Test two sessions reading the same revision. Save in A; attempt a conflicting save in B using the stale revision. Require backend rejection and unchanged A data. A mock 412 or client preflight check does not establish this.
6. Check a user/role lacking rights: direct read and write must be denied by the backend, with a helpful UI state. Avoid changing real users' rights merely to test; use the authorized test identities or mark the test blocked.
7. Exercise a populated multi-page query through all continuation tokens. Simulate a later-page failure separately and confirm already loaded rows remain visible.
8. Where using a snapshot/index design, simulate an index failure after save and verify precise user state and idempotent repair. Use a live controlled case when feasible and label evidence accurately.
9. Exercise timeout reconciliation with the same retained identities. Prefer controlled fault injection; do not manufacture ambiguous writes against business data. Track any unresolved real write as unknown.
10. Clean up only the identified verification records if included in test scope. Keep evidence and pending operations. Do not delete unrelated abandoned lists mentioned in source documents.

Report each result as live passed, live failed, simulated passed, blocked, not-run or not-applicable. State exactly which route and operations were tested. If required persistence, access control or concurrency fails, continue fixing or report an incomplete migration; publishing does not turn it into a passed check.
