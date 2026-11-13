# Local verification record

13 November 2026. These results apply to the prepared plugin and optional source inventory utility, not a migrated customer application.

- 14 standard-library unit tests passed for the inventory helper: real HTML script boundaries, no source execution, credential content exclusion, unsafe ZIP paths, symlinks, file/total/count limits, malformed JSON/encoding, unclosed script detection, source/output preservation, duplicate ZIP entries and invalid ZIP handling.
- The upload ZIP passed 90 local manifest/package checks against Microsoft's unchanged saved v1.29 schema and documented constraints. See `validation.json` for the archive and schema hashes.
- 7 additional package tests passed: current declared skills, version-derived artifact names, deterministic rebuilding, invalid JSON whitespace rejection, missing skill rejection, schema/version agreement and CLI schema selection. Total: 21 tests.
- Microsoft Teams Manifest 0.1.9 and TeamsFx Core 3.1.5 passed schema validation, six-skill parsing, portable transport preflight and a comparison with the official packaging driver. See `microsoft-validation.json`.
- Python sources parsed successfully.
- Rebuilding the plugin ZIP from the packaged source content produced byte-identical output.
- 18 behavioral evaluation scenarios were prepared and remain not-run.

Not executed for the 1.0.1 candidate: Microsoft tenant upload, actual skill activation, host-model behavior evaluation, end-to-end Lovable/HTML recreation, live SharePoint operations, target app publishing or player launch. No private NIRAS systems were accessed from this environment.

The original 1.0.0 package was reported rejected by admin upload. The exact rejecting service-side rule remains unknown. Version 1.0.1 uses manifest 1.29, and tenant acceptance is not yet retested.
