# Researched baseline — 13 November 2026

This is documentation evidence, not a claim that the NIRAS tenant has been tested. Official sources are listed below. Recheck preview details and actual environment capabilities at migration time.

| Topic | Baseline | Source |
|---|---|---|
| Code | Authors apps locally or in cloud, accepts project context, offers preview and can publish apps; Code is a separate tab from Cowork | [Code overview](https://learn.microsoft.com/en-us/copilot/code/overview) |
| Runtime | Microsoft hosts apps created through several authoring routes; Entra and tenant controls apply | [Managed Runtime](https://learn.microsoft.com/en-us/microsoft-365/managed-apps) |
| Target architecture | JavaScript/TypeScript SPA with a platform SDK and generated connector services; platform owns configuration | [Architecture](https://learn.microsoft.com/en-us/microsoft-365/managed-apps/developer/architecture) |
| Tooling freshness | Active repository uses `cmr-*`; the former `managed-apps` repository is archived | [Current repository](https://github.com/microsoft/Copilot-Managed-Runtime), [archived repository](https://github.com/microsoft/Managed-Apps) |
| Data | Connector discovery, binding and regeneration through platform tooling; calls use generated services | [Connect to data](https://learn.microsoft.com/en-us/microsoft-365/managed-apps/developer/connect-to-data) |
| Policy | Allowed connectors do not imply every operation is allowed. Open-ended SharePoint HTTP actions are blocked by default; CSP constrains scripts, workers and resources | [Governance](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/apps/governance) |
| Publishing | A build is not publication; sharing an app does not share underlying data | [Use Code](https://learn.microsoft.com/en-us/copilot/code/use-code) |
| Plugin | Skills can be packaged in the Microsoft 365 unified manifest, with PNG icons, and registered for organizational use | [Build plugins](https://learn.microsoft.com/en-us/copilot/cowork/cowork-plugin-development), [admin registry](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/manage-plugins-skills-mcp-servers) |
| Licensing | Authoring and running apps have distinct requirements; confirm current license/spending-policy coverage for intended users | [Licensing FAQ](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/apps/licensing-faq) |

The platform can host a Lovable app through other workflows, but this plugin's requested result is recreation in Copilot Code. Hosting portability documentation does not override that objective.

Preview APIs, package names and admin navigation can change. Prefer observed tool/schema results and the newest authoritative page relevant to the target; record conflicts rather than silently combining old and new examples. In particular, the general runtime landing page still contains old SDK names while the active repository and architecture page use the renamed packages.
