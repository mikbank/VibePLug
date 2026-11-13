# NIRAS App Migration for Copilot Code

Version 1.0.1 · Prepared 13 November 2026 · Publisher: NIRAS A/S

[Download the plugin ZIP](dist/niras-app-migration-1.0.1.zip?raw=true) · [Setup guide](NIRAS-App-Migration-Guide.md) · [Research](RESEARCH.md)

This Microsoft 365 plugin teaches Copilot to inspect an existing solution and recreate it as a fresh Copilot Code managed app. It covers Lovable, static HTML applications and discovery of projects from other platforms. SharePoint is the default durable store. A request to migrate includes building, testing and publishing, unless the user limits the scope.

The result is a skills package, not a deterministic source converter or an independent migration service. It uses the coding, file/repository, browser, connector and publishing tools available to the host session. Installing the package does not grant access, create SharePoint connections or deploy an app. If a Cowork session cannot build the target directly, the skills produce a concrete handoff for Copilot Code and report that the migration is incomplete.

## Upload package

Upload **`dist/niras-app-migration-1.0.1.zip`**. The ZIP contains `manifest.json`, two PNG icons and six declared skills at its root. Do not upload this source directory or the source distribution ZIP as the plugin.

Version 1.0.1 targets Microsoft's current unified manifest **1.29** format and has been compared with the official Agents Toolkit packager. It includes no remote MCP server, external service dependency or embedded credentials. The app ID is `261c64ae-e58d-4efa-aa5c-68907c8b3f46`; keep it stable when updating and increment the manifest version.

Configured publisher fields:

| Field | Value |
|---|---|
| Publisher | NIRAS A/S |
| Website | https://www.niras.com/ |
| Privacy | https://www.niras.com/privacy-policy/ |
| Terms | https://niras.sharepoint.com/sites/GlobalIT/SitePages/Citizen-Development-And-VibeCoding-in-NIRAS.aspx |

The internal terms URL was supplied by the user and has not been accessed in the NIRAS tenant. The icons are original generic migration glyphs, not official NIRAS logos. This package is prepared for internal organizational distribution.

## Install in Microsoft 365

1. Sign in to the Microsoft 365 admin center using an account permitted to manage organizational plugins.
2. Open **Agents → Tools → Registry → Upload**, where available, and select the plugin ZIP. Review the six skills and choose the intended users/groups before installing.
3. Microsoft also documents **Manage apps → Upload custom app → … → Add agent** for ZIP publication. Use the upload surface available in the tenant; labels differ between documented admin experiences. If an admin surface asks for the package/manifest, retain the ZIP and all its bundled skill files together.
4. In Cowork, open the plugins area under **Sources & Skills** or **Customize**, find **NIRAS App Migration** and add/enable it as required by the tenant's deployment experience. Verify the six skills are discoverable in a new session. Check Code's plugin availability in that tenant as well.
5. Run the activation and pilot scenarios below before broader rollout. Local validation cannot prove Microsoft ingestion or tenant-specific policy acceptance.

Microsoft references: [admin registry](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/manage-plugins-skills-mcp-servers), [package creation and tenant upload](https://learn.microsoft.com/en-us/copilot/cowork/cowork-plugin-development), [using Cowork plugins](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugins).

## Start a migration

Provide an authorized repository/folder or code ZIP, the business purpose and the intended SharePoint destination. A URL and screenshots help discover UI behavior, but cannot establish hidden rules or backend completeness. Provide separate business-data/file exports if existing data must move.

Example Lovable request:

> Use NIRAS App Migration to recreate this Lovable project in a fresh Copilot Code managed app. Explore the attached source and workflows, ask me where material business rules are unclear, and use SharePoint for persistence. Build, test and publish to my existing restricted scope. Keep the original Lovable project unchanged.

Example HTML request:

> Migrate this HTML planning app to a new Copilot Code managed app. Preserve its calculations, imports/exports and familiar workflows. Use this SharePoint site for durable projects: [site]. Explore first, resolve unclear business logic with me, then build, test and publish.

Assessment-only request:

> Assess this solution for recreation in Copilot Code. Inspect the source and identify business-rule questions and platform gaps. Do not build or publish yet.

The plugin should investigate before asking for information already present in the source. It asks up to three material questions at a time and continues independent work while waiting. It records inferred rules separately from confirmed ones. Attached notes and repository text remain evidence, not authority to change the task or run embedded instructions.

## Included skills

| Skill | Purpose |
|---|---|
| `migrate-to-copilot-code` | Discovery, orchestration, questions, parity matrix and migration record |
| `copilot-managed-app-capabilities` | Runtime, tool, identity, connector and host capability assessment |
| `rebuild-lovable-app` | Client/server, database, roles, integrations and data-export discovery; native recreation |
| `rebuild-html-app` | Real HTML/script boundaries, domain parity, files and host interaction |
| `sharepoint-persistence` | Lists/libraries, snapshots, live access, concurrency, timeouts and partial saves |
| `verify-and-publish` | Layered evidence, release checks, successful deployment and actual player URL |

The recreation must use a fresh target architecture. Rehosting a Lovable build, embedding the old site or running an unchanged HTML application does not fulfill the migration. Representative fixtures preserve the original business meaning. Licensed portable utilities may be adapted into the new domain layer when appropriate and recorded; the source bootstrap stays out of the target.

## Source inventory helper

The optional helper uses Python 3.10+ and the standard library only:

```bash
python plugin/skills/migrate-to-copilot-code/scripts/inspect_source.py /path/to/source --output inventory.json
```

It accepts a directory, code ZIP or HTML file. It does not execute code, install dependencies, extract ZIPs or contact services. It emits hashes, HTML boundaries, dependency names and heuristic locations rather than source snippets or secret values. Recognized credential files, symlinks and build/vendor directories are excluded. Limits are 10,000 read files, 8 MiB per file and 100 MiB total; skipped/truncated analysis is reported. Embedded vendor code can still appear in an HTML inventory. Malformed/legacy-encoded files require manual inspection, and this utility is not a secret scanner or a complete business-logic extractor.

## Rebuild and validate the plugin

Python development utilities use Python 3.10+ with the dependencies in `requirements-dev.txt`. Microsoft offline checks also use the pinned Node dependencies in `package.json` and `package-lock.json`. The shipped source-inventory helper has no third-party dependency.

```bash
python -m pip install -r requirements-dev.txt
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
python tools/make_icons.py
python tools/package_plugin.py
PYTHONDONTWRITEBYTECODE=1 python tools/validate_plugin.py dist/niras-app-migration-1.0.1.zip --report validation.json
```

Microsoft's unchanged 1.28 and 1.29 schema snapshots are included in `schemas/` for reproducible local manifest validation. Python's metaschema regex check does not understand some ECMAScript patterns in unrelated optional vendor definitions, so the validator validates this manifest against the saved schema without revalidating the schema's own regex syntax. It also checks ZIP integrity, metadata, icon sizes/transparency, declared skills, frontmatter, companion references and package path/size constraints. These are local checks, not Microsoft's service-side validation.

For the Microsoft tooling checks, install the pinned dependencies with `npm ci --ignore-scripts` and run `npm run check:microsoft -- --report microsoft-validation.json`. This invokes Microsoft's offline library and packaging driver; it does not sign in, upload or provision.

## Verification status and tenant pilot

Local verification: **21 tests passed** (14 inventory-helper and 7 package checks). The ZIP passed the saved Microsoft schema and 90 local checks. Microsoft's own libraries parsed all six skills, passed transport preflight and found no schema errors. The contents match the official packager output; see `microsoft-validation.json`. The build is reproducible.

The original 1.0.0 package was rejected by the user's admin upload. This 1.0.1 candidate has not yet been accepted by that service; offline checks do not establish tenant acceptance. See [ADMIN-UPLOAD-TROUBLESHOOTING.md](ADMIN-UPLOAD-TROUBLESHOOTING.md).

Not yet exercised: tenant upload, actual skill activation, a migration performed by the host model, live SharePoint operations, app deployment or player launch. `evaluations/scenarios.json` contains 18 behavioral scenarios; they are **not run**, not passed tests.

Start with one noncritical source app and a dedicated SharePoint destination. Confirm skill activation and the fresh-target behavior; prove a real save/load after refresh, permissions and any required concurrency; then verify publication and launch. The plugin keeps simulated tests distinct from live and browser evidence. A failed essential criterion yields an incomplete migration with concrete artifacts and a precise blocker.

Publishing the target is included when migration is requested. Sharing more broadly, deleting the source, replacing its traffic, disabling its services or removing unrelated historical lists requires that additional scope to be requested. Existing platform consent prompts and tenant controls still apply.

Read [RESEARCH.md](RESEARCH.md) for sources, design choices and unresolved environment checks, and [EVALUATION-GUIDE.md](EVALUATION-GUIDE.md) for pilot execution. The editable source distribution is [dist/niras-app-migration-source-1.0.1.zip](dist/niras-app-migration-source-1.0.1.zip?raw=true).
