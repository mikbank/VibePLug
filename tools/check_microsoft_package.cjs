#!/usr/bin/env node
// Verify the exact portable ZIP using Microsoft's published offline libraries.
// Does not sign in, upload, provision, register skills or change tenant state.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const { createRequire } = require('node:module');

const root = path.resolve(__dirname, '..');
function argument(flag, fallback) {
  const index = process.argv.indexOf(flag);
  if (index < 0) return fallback;
  if (!process.argv[index + 1] || process.argv[index + 1].startsWith('--')) {
    throw new Error(`Missing value for ${flag}`);
  }
  return process.argv[index + 1];
}
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'plugin/manifest.json'), 'utf8'));
const archivePath = path.resolve(argument('--package', path.join(root, 'dist', `niras-app-migration-${manifest.version}.zip`)));
const toolingRoot = path.resolve(argument('--tooling-root', root));
const requireTool = createRequire(path.join(toolingRoot, 'package.json'));
const { ManifestUtil } = requireTool('@microsoft/teams-manifest');
const coreRoot = path.dirname(requireTool.resolve('@microsoft/teamsfx-core/package.json'));
const { readSkillPackage, validateSkillTransportPackage } = require(path.join(coreRoot, 'build/component/m365/skills/skillPackage.js'));
const { CreateAppPackageDriver } = require(path.join(coreRoot, 'build/component/driver/teamsApp/createAppPackage.js'));
const requireCore = createRequire(path.join(coreRoot, 'package.json'));
const AdmZip = requireCore('adm-zip');
const hash = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');

async function main() {
  const bytes = fs.readFileSync(archivePath);
  const archive = new AdmZip(bytes);
  const manifestBytes = archive.getEntry('manifest.json').getData();
  assert(!manifestBytes.subarray(0, 3).equals(Buffer.from([0xef, 0xbb, 0xbf])), 'Manifest must be UTF-8 without BOM');
  const packagedManifest = JSON.parse(manifestBytes.toString('utf8'));
  assert.equal(packagedManifest.$schema, `https://developer.microsoft.com/json-schemas/teams/v${packagedManifest.manifestVersion}/MicrosoftTeams.schema.json`, 'Schema URL must match manifestVersion');
  assert.deepEqual(packagedManifest, manifest, 'Packaged manifest must match source');
  assert.equal(path.basename(archivePath), `niras-app-migration-${manifest.version}.zip`, 'Release filename must match manifest.version');
  const schema = JSON.parse(fs.readFileSync(path.join(root, 'schemas', `MicrosoftTeams-v${manifest.manifestVersion}.schema.json`), 'utf8'));
  const errors = await ManifestUtil.validateManifestAgainstSchema(packagedManifest, schema);
  assert.deepEqual(errors, [], 'Microsoft manifest schema errors: ' + JSON.stringify(errors));
  const inventory = readSkillPackage(bytes);
  assert(inventory.isOk(), inventory.isErr() ? inventory.error.message : 'Skill package cannot be parsed');
  const transport = validateSkillTransportPackage(inventory.value);
  assert(transport.isOk(), transport.isErr() ? transport.error.message : 'Skill transport preflight failed');

  const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'niras-ms-package-'));
  try {
    const referencePath = path.join(scratch, 'microsoft-reference.zip');
    const quiet = { info() {}, debug() {}, verbose() {}, warning() {}, error() {} };
    const result = await new CreateAppPackageDriver().build({
      manifestPath: path.join(root, 'plugin/manifest.json'),
      outputZipPath: referencePath,
      outputJsonPath: path.join(scratch, 'manifest.json'),
    }, { projectPath: root, logProvider: quiet, addTelemetryProperties() {}, addSummary() {} });
    assert(result.isOk(), result.isErr() ? result.error.message : 'Microsoft packaging failed');
    const reference = new AdmZip(referencePath);
    const names = archive.getEntries().filter(e => !e.isDirectory).map(e => e.entryName).sort();
    const referenceNames = reference.getEntries().filter(e => !e.isDirectory).map(e => e.entryName).sort();
    assert.deepEqual(names, referenceNames, 'Archive entries differ from Microsoft packager');
    for (const name of names) {
      if (name === 'manifest.json') {
        assert.deepEqual(packagedManifest, JSON.parse(reference.getEntry(name).getData().toString('utf8')));
      } else {
        assert(archive.getEntry(name).getData().equals(reference.getEntry(name).getData()), 'File differs from Microsoft packager: ' + name);
      }
    }
    const report = {
      result: 'passed',
      tools: {
        '@microsoft/teams-manifest': requireTool('@microsoft/teams-manifest/package.json').version,
        '@microsoft/teamsfx-core': requireTool('@microsoft/teamsfx-core/package.json').version,
      },
      archive_sha256: hash(bytes),
      version: packagedManifest.version,
      manifest_version: packagedManifest.manifestVersion,
      app_id: packagedManifest.id,
      strict_json: 'passed',
      microsoft_schema_errors: errors,
      microsoft_skill_inventory: inventory.value.skills.map(s => ({ name: s.name, folder: s.folder, files: s.files.length })),
      microsoft_skill_transport_preflight: 'passed',
      microsoft_packager_comparison: { result: 'passed', files: names.length, manifest: 'semantic equality', other_files: 'byte equality' },
      service_side_validation: 'not_run; requires Microsoft sign-in',
      tenant_installation: 'not_retested',
    };
    const encoded = JSON.stringify(report, null, 2) + '\n';
    const reportPath = argument('--report', null);
    if (reportPath) fs.writeFileSync(path.resolve(reportPath), encoded);
    process.stdout.write(encoded);
  } finally {
    fs.rmSync(scratch, { recursive: true, force: true });
  }
}
main().catch(error => { process.stderr.write('Microsoft offline package checks failed: ' + error.message + '\n'); process.exitCode = 1; });
