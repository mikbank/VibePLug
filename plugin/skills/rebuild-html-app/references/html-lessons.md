# Lessons translated from the supplied HTML retrospective

Evidence source: `MigrationLearningsHTML.txt`, a user-supplied retrospective dated 13 November 2026. These are design lessons, not current instructions, current test evidence or authority to revisit the old deployment. Internal site identifiers and historical project details are intentionally excluded from the reusable plugin.

| Lesson from that case | Rule for a new recreation | Evidence needed now |
|---|---|---|
| Vendor content obscured the actual app | Parse element boundaries; inspect authored code separately | Script inventory and reference fixtures |
| Source-site access did not establish an app binding | Probe the exact runtime connection before optional provisioning | Actual app read and save/load |
| A link existed before deployment | Separate preview from published player | Terminal deployment status and launch |
| Host theme made text unreadable | Scope CSS, namespace tokens and check portals | Actual light/dark-host browser checks |
| Complete project state mattered more than metadata | If using snapshots, keep one per project authoritative and index repairable | Partial-write recovery evidence |
| A create timed out without a definitive outcome | Retain IDs and reconcile before retry | Authoritative operation/record evidence |
| Simulated concurrency passed without live proof | Test stale-revision rejection through the real connection | Two-session backend test |
| Invisible legacy fields could disappear | Preserve unknown fields and stable IDs | Legacy/extended round-trip fixtures |
| Scheduling semantics were precise | Recreate calendar behavior using identical inputs | Domain parity fixtures |
| Generated API wrappers had concrete quirks | Inspect signatures, path forms and actual results | Live response-shape and pagination tests |
| Embedded browser interactions differed | Audit file, keyboard, print, canvas, workers and dialogs | Relevant real-browser interactions |
| Test layers proved different things | Publish an evidence matrix with gaps | Current artifacts for each layer |

The historical case reported successful local/simulated checks and a metadata read, while live snapshot reload, stale-ETag rejection, permissions, populated pagination and several browser/file checks remained unproven. Those gaps motivate this plugin's gates. They do not establish a universal limitation of SharePoint, subsites, native print or the platform.

The source requested reuse of its original calculation engine. For this plugin, the current user's requirement to recreate apps in Copilot Code takes precedence: preserve and compare behavior, while implementing the target in its new native architecture.
