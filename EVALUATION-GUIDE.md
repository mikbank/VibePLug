# Tenant evaluation guide

The JSON scenarios are specifications for exercising the plugin in the real host. They have not been run. They are distinct from the 14 executed Python tests, which verify the optional inventory utility only.

## Activation check

Upload the plugin ZIP to a restricted pilot audience. Start a new session, confirm the plugin and all six skill names appear, then ask it to explain the migration workflow. Confirm it retrieves companion references when relevant. If the inventory utility cannot execute in that host, it should continue with manual inspection rather than inventing an execution result.

## Run the scenarios

For each entry in `evaluations/scenarios.json`, create the stated small synthetic fixture and run the prompt in a new conversation with the plugin enabled. Record the manifest version, host surface, model/version if shown, available tools, scenario input, observed actions, answers given and evidence artifacts. Test both Cowork coordination and Code authoring where available.

Start with scenarios 01, 03, 04, 06, 07, 10, 13, 14 and 18, then complete the remainder. Follow-up answers should allow the plugin to resume dependent work without repeating resolved questions.

Use isolated test destinations and synthetic records. Do not change production permissions to manufacture a scenario. Controlled simulated faults should stay labeled simulated; use live checks for server-enforced permissions and conditional writes.

## Record results

| Scenario | Host/version | Observed behavior | Evidence | Passed/failed/blocked/not-run |
|---|---|---|---|---|

Pass only if the expected behaviors occur and no failure condition occurs. An unavailable required host capability means blocked, not passed. A good explanation of missing capability can pass a scenario explicitly testing graceful handoff, while the attempted migration itself remains incomplete.

The release should not be advertised as end-to-end verified until at least one Lovable recreation and one HTML recreation have completed their critical live checks and launched from an actual confirmed published URL. Keep the new app in its existing restricted test scope unless a broader audience was specified.

## Update safely

Keep the manifest app ID stable and increment its version. Rebuild and locally validate the exact ZIP intended for upload. Re-run affected behavioral scenarios when modifying skill instructions, references or activation descriptions, and verify a new tenant session picks up the update. A source-only edit is not evidence that the installed plugin changed.
