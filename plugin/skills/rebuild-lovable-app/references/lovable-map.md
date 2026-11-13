# Lovable discovery and replacement map

Research checked 13 November 2026. Inspect the actual project; not every Lovable solution uses these components.

| Source concern | Evidence to inspect | Target decision |
|---|---|---|
| UI/routes | Components, routes, screenshots, validation | Recreate in a fresh target UI |
| Client/server split | Dependencies, server functions, SSR routes | Move behavior to supported SPA/services architecture |
| Database | SQL/Drizzle schema and migrations, real exports | SharePoint lists/library model and separately reconciled import |
| RLS/roles | SQL policies, auth claims, owner checks | Entra identity and equivalent backend-enforced rights |
| Files | Buckets, path conventions, permissions, actual file export | SharePoint library with verified file access |
| Functions/jobs | Function code, triggers, schedules, side effects | Supported governed operation or explicit capability decision |
| Auth | Providers, user IDs, owner foreign keys | Tenant identity mapping; credentials are not migrated to Entra |
| Runtime integrations | Lovable AI gateway, connectors, Supabase clients, secret names | Replace each required integration; verify remaining network calls |

Code export does not include database records or stored files. Private secrets and service connections also require separate supported setup. Distinguish a blank schema migration from a business-data migration.

Official references:

- [GitHub export and sync](https://docs.lovable.dev/integrations/github)
- [Hosting and ownership](https://docs.lovable.dev/tips-tricks/deployment-hosting-ownership)
- [External deployment and component inventory](https://docs.lovable.dev/tips-tricks/external-deployment-hosting)
- [Built-in backend](https://docs.lovable.dev/features/cloud)
- [Supabase integration](https://docs.lovable.dev/integrations/supabase)
- [TanStack upgrade and server behavior](https://docs.lovable.dev/features/upgrade-to-tanstack-start)

These sources explain what may exist and how to retrieve evidence. This plugin intentionally creates a replacement in Copilot Code instead of using their rehosting instructions.
