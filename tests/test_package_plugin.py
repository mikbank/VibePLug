import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT/'tools'/filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

packager = load('package_plugin', 'package_plugin.py')
checker = load('validate_plugin', 'validate_plugin.py')

class PluginPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.archive = self.dir/'candidate.zip'
        packager.package(ROOT/'plugin', self.archive)
        self.manifest = json.loads((ROOT/'plugin/manifest.json').read_text())
        self.schema = ROOT/'schemas'/f"MicrosoftTeams-v{self.manifest['manifestVersion']}.schema.json"

    def rewrite(self, update):
        with zipfile.ZipFile(self.archive) as z:
            files = {name: z.read(name) for name in z.namelist()}
        update(files)
        with zipfile.ZipFile(self.archive, 'w') as z:
            for name, data in files.items():
                z.writestr(name, data)

    def test_current_package_and_all_declared_skills_validate(self):
        result = checker.validate(self.archive, self.schema)
        self.assertEqual(result['result'], 'passed')
        self.assertEqual(result['manifest_version'], self.manifest['manifestVersion'])
        self.assertEqual(len(result['skills']), 6)

    def test_default_artifact_filename_tracks_manifest_version(self):
        self.assertEqual(packager.default_output().name, f"niras-app-migration-{self.manifest['version']}.zip")

    def test_same_sources_produce_identical_archive(self):
        other = self.dir/'second.zip'
        packager.package(ROOT/'plugin', other)
        self.assertEqual(self.archive.read_bytes(), other.read_bytes())

    def test_nonbreaking_spaces_in_json_indentation_are_rejected(self):
        def modify(files):
            files['manifest.json'] = files['manifest.json'].replace(b'\n  "', '\n\u00a0 "'.encode('utf-8'), 1)
        self.rewrite(modify)
        with self.assertRaises(json.JSONDecodeError):
            checker.validate(self.archive, self.schema)

    def test_declared_skill_folder_must_exist_in_the_zip(self):
        def modify(files):
            manifest = json.loads(files['manifest.json'])
            manifest['agentSkills'][0]['folder'] = './skills/vibe-solution-migration'
            files['manifest.json'] = json.dumps(manifest).encode()
        self.rewrite(modify)
        with self.assertRaisesRegex(ValueError, 'Declared SKILL.md exists'):
            checker.validate(self.archive, self.schema)

    def test_schema_and_manifest_versions_must_agree(self):
        def modify(files):
            manifest = json.loads(files['manifest.json'])
            manifest['manifestVersion'] = '1.28'
            files['manifest.json'] = json.dumps(manifest).encode()
        self.rewrite(modify)
        with self.assertRaisesRegex(ValueError, 'Microsoft manifest schema'):
            checker.validate(self.archive, self.schema)

    def test_cli_selects_the_schema_declared_by_the_package(self):
        run = subprocess.run([sys.executable, str(ROOT/'tools/validate_plugin.py'), str(self.archive)],
            capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['manifest_version'], self.manifest['manifestVersion'])

if __name__ == '__main__':
    unittest.main()
