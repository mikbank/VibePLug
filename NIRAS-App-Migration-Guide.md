# NIRAS App Migration for Copilot Code

Version 1.0.0 · NIRAS A/S · Prepared 13 November 2026

The plugin is designed to explore an existing solution, ask focused questions about unclear business rules, and recreate it as a fresh Copilot Code managed app. It covers Lovable, HTML applications and projects from other platforms. It defaults to SharePoint for durable data and carries a migration request through building, testing and publishing, unless the user limits the scope.

The plugin contains six Agent Skills. It uses the host's available coding, source access, connector, browser and publishing tools. Installing it does not create connections or grant permissions. It cannot independently supply a missing Copilot Code build capability.

## Files

- **[dist/niras-app-migration-1.0.0.zip](dist/niras-app-migration-1.0.0.zip?raw=true)** — the plugin package to upload to Microsoft 365.
- **[dist/niras-app-migration-source-1.0.0.zip](dist/niras-app-migration-source-1.0.0.zip?raw=true)** — editable skills, references, utility, tests, packaging tools, research and evaluation scenarios. Do not upload this ZIP as the plugin.
- **[RESEARCH.md](RESEARCH.md)** — findings and official sources.
- **[validation.json](validation.json)** — local package validation result and hash.

## Install

1. Sign in to the Microsoft 365 admin center with permission to manage plugins.
2. Use **Agents → Tools → Registry → Upload**, where available, and select `niras-app-migration-1.0.0.zip`. Review the six skills, scope the intended users/groups, and install. Microsoft also documents **Manage apps → Upload custom app → … → Add agent** for ZIP publication; use the surface exposed in the tenant.
3. In Cowork's plugins area under **Sources & Skills** or **Customize**, locate **NIRAS App Migration**. Enable/add it if required, then confirm its skills appear in a new session. Verify plugin availability in Code as well.
4. Run a restricted pilot before broader distribution. The source archive contains an evaluation guide and 18 scenario specifications.

The package uses Microsoft's documented unified manifest 1.28 format. Publisher metadata is NIRAS A/S, the NIRAS public website and privacy policy, and the internal Citizen Development and VibeCoding page supplied for terms of use. It includes no external MCP server or credentials.

Official references: [admin upload](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/manage-plugins-skills-mcp-servers), [plugin package format](https://learn.microsoft.com/en-us/copilot/cowork/cowork-plugin-development).

## First migration

Provide a source folder, authorized repository or code export, a short business purpose and the intended SharePoint site. Include separate data/file exports when existing business data must move. A URL or screenshot alone cannot reveal all backend rules.

> Use NIRAS App Migration to recreate this Lovable project as a fresh Copilot Code managed app. Explore the source and workflows, ask me where material business rules are unclear, and use this SharePoint site for persistence: [site]. Build, test and publish to my existing restricted scope. Keep the original project unchanged.

For HTML:

> Migrate this HTML application to a new Copilot Code managed app. Preserve its calculations, file formats and familiar workflows. Inspect it first, ask about unclear business logic, then build, test and publish with SharePoint persistence.

The plugin should recreate the application in the target architecture. Deploying the original Lovable bundle, embedding the old site or running an unchanged HTML file does not satisfy its workflow. It uses source-backed fixtures to preserve business meaning.

## Skills

| Skill | Role |
|---|---|
| Migration coordination | Explore, recover rules, resolve questions and track parity |
| Managed-app capabilities | Verify the current host, tooling, identity and connector capabilities |
| Lovable recreation | Inspect client/server code, database rules, auth, files and integrations |
| HTML recreation | Find real app code, preserve calculations/files and adapt host interactions |
| SharePoint persistence | Choose lists/libraries and verify real writes, conflicts and recovery |
| Verification and publishing | Separate test evidence, confirm deployment and verify the player URL |

The optional read-only inventory helper supports directories, ZIPs and HTML without executing source code or making network calls. If the host cannot run it, the skill proceeds with manual exploration.

## Verification boundary

The plugin ZIP passed local validation against Microsoft's saved manifest schema and documented packaging constraints. **Fourteen tests passed for the inventory helper.** The ZIP rebuild is reproducible.

Microsoft tenant ingestion, skill activation, actual model-led migrations, live SharePoint operations and managed-app deployment have **not** been tested. The 18 behavioral scenarios are specifications, not passed tests. A first pilot should prove a real save/load after refresh and in another session, backend permissions and required conflict protection, then successful publication and actual player launch.

The skills distinguish source assumptions, user-confirmed rules, simulated tests, live backend evidence and browser evidence. They report blocked essential behavior as an incomplete migration. Publishing is included when migration is requested; broader sharing, source deletion and traffic cutover must be within the requested scope.
