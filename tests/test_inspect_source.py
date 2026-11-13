import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT/'plugin/skills/migrate-to-copilot-code/scripts/inspect_source.py'
spec = importlib.util.spec_from_file_location('inspect_source', MODULE)
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


class SourceInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_script_boundaries_ignore_html_strings_in_vendor_code(self):
        source = '''<!doctype html><html><head>
<script>/* SheetJS vendor */ const fake="<body><script>";</script>
<style>.card { color: black; }</style></head><body>
<button onclick="save()">Save</button>
<script type="module">const app = () => localStorage.getItem('p');</script>
</body></html>'''
        doc = inventory.HTMLInventory(source).report()
        self.assertEqual(doc['body_start_lines'], [3])
        self.assertEqual([s['tag'] for s in doc['script_style_elements']], ['script','style','script'])
        self.assertTrue(doc['script_style_elements'][0]['vendor_hint'])
        self.assertEqual(doc['inline_event_attribute_count'], 1)
        last = doc['script_style_elements'][-1]
        self.assertEqual(source[last['content_start_offset']:last['content_end_offset']], "const app = () => localStorage.getItem('p');")
        self.assertEqual(last['script_kind'], 'module')

    def test_no_source_execution_and_no_credential_contents(self):
        project = self.root/'project'; project.mkdir()
        package = project/'package.json'
        marker = self.root/'executed'
        package.write_text(json.dumps({'dependencies':{'@tanstack/react-start':'1'},
            'scripts':{'postinstall':f'touch {marker}'}}))
        (project/'.env').write_text('TOKEN=DO_NOT_EMIT_THIS_VALUE')
        (project/'app.ts').write_text('const secret="ALSO_DO_NOT_EMIT"; fetch(secret);')
        before = hashlib.sha256(package.read_bytes()).hexdigest()
        result = inventory.inspect(project)
        encoded = json.dumps(result)
        self.assertNotIn('DO_NOT_EMIT_THIS_VALUE', encoded)
        self.assertNotIn('ALSO_DO_NOT_EMIT', encoded)
        self.assertFalse(marker.exists())
        self.assertEqual(hashlib.sha256(package.read_bytes()).hexdigest(), before)
        pkg = next(f['package'] for f in result['files'] if f['path']=='package.json')
        self.assertEqual(pkg['stack_hints'], ['tanstack-start'])
        self.assertTrue(pkg['has_lifecycle_hooks'])

    def test_zip_traversal_symlink_and_duplicates_are_not_extracted(self):
        archive = self.root/'source.zip'
        link = zipfile.ZipInfo('reference-link')
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        with zipfile.ZipFile(archive,'w') as z:
            z.writestr('../outside.txt', 'bad')
            z.writestr('/absolute.txt', 'bad')
            z.writestr('C:/windows.txt', 'bad')
            z.writestr('a\\b.txt', 'bad')
            z.writestr(link, '../outside.txt')
            z.writestr('project/app.ts', 'localStorage.setItem("x", "y")')
        result = inventory.inspect(archive)
        self.assertEqual([f['path'] for f in result['files']], ['project/app.ts'])
        self.assertEqual(len(result['skipped']), 5)
        self.assertTrue(result['incomplete'])
        self.assertFalse((self.root/'outside.txt').exists())
        self.assertFalse((self.root/'project').exists())

    def test_symlinked_files_and_directories_are_not_followed(self):
        project = self.root/'project';project.mkdir()
        outside = self.root/'outside';outside.mkdir()
        (outside/'private.txt').write_text('PRIVATE')
        (project/'link').symlink_to(outside, target_is_directory=True)
        (project/'file.txt').symlink_to(outside/'private.txt')
        result = inventory.inspect(project)
        self.assertEqual(result['files'], [])
        self.assertEqual(len(result['skipped']), 2)
        with self.assertRaisesRegex(ValueError, 'symbolic link'):
            inventory.inspect(project/'link')

    def test_large_file_marks_analysis_incomplete_without_partial_hash(self):
        source = self.root/'large.html';source.write_text('x'*100)
        with patch.object(inventory,'MAX_FILE_BYTES',20):
            result=inventory.inspect(source)
        self.assertTrue(result['incomplete'])
        self.assertEqual(result['files'],[])
        self.assertEqual(result['skipped'][0]['reason'],'file-byte-limit')

    def test_total_limit_bounds_zip_decompression(self):
        archive=self.root/'compressed.zip'
        with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr('a.txt','a'*100)
            z.writestr('b.txt','b'*100)
        with patch.object(inventory,'MAX_TOTAL_BYTES',150):
            result=inventory.inspect(archive)
        self.assertEqual(result['summary']['bytes_read'],100)
        self.assertTrue(result['incomplete'])

    def test_file_limit_marks_incomplete(self):
        for name in ['a.ts','b.ts']:(self.root/name).write_text('x')
        with patch.object(inventory,'MAX_FILES',1):
            result=inventory.inspect(self.root)
        self.assertEqual(len(result['files']),1)
        self.assertTrue(result['incomplete'])

    def test_malformed_package_and_non_utf8_do_not_abort_inventory(self):
        (self.root/'package.json').write_text('not-json')
        (self.root/'legacy.html').write_bytes(b'\xff\xfe\x80')
        result=inventory.inspect(self.root)
        package=next(f for f in result['files'] if f['path']=='package.json')
        legacy=next(f for f in result['files'] if f['path']=='legacy.html')
        self.assertIn('package_error',package)
        self.assertIn('not-utf8',legacy['analysis'])

    def test_unclosed_script_is_reported(self):
        doc=inventory.HTMLInventory('<body><script>const x=1;').report()
        self.assertFalse(doc['script_style_elements'][0]['closed'])

    def test_external_attribute_values_are_not_emitted(self):
        doc=inventory.HTMLInventory('<script src="https://x.test/?token=PRIVATE"></script>').report()
        self.assertNotIn('PRIVATE',json.dumps(doc))
        self.assertTrue(doc['script_style_elements'][0]['external'])

    def test_cli_refuses_source_overwrite_and_existing_output(self):
        source=self.root/'app.html';source.write_text('<body>Original</body>')
        evidence=self.root/'inventory.json';evidence.write_text('keep')
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(inventory.main([str(source),'--output',str(source)]),2)
            self.assertEqual(inventory.main([str(source),'--output',str(evidence)]),2)
        self.assertEqual(source.read_text(),'<body>Original</body>')
        self.assertEqual(evidence.read_text(),'keep')

    def test_cli_writes_json_only_when_requested(self):
        source=self.root/'app.html';source.write_text('<body><script>const x=1;</script></body>')
        output=self.root/'evidence'/'inventory.json'
        self.assertEqual(inventory.main([str(source),'--output',str(output)]),0)
        result=json.loads(output.read_text())
        self.assertTrue(result['read_only'])
        self.assertEqual(result['summary']['files_read'],1)

    def test_duplicate_zip_path_is_not_silently_replaced(self):
        archive=self.root/'duplicate.zip'
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',UserWarning)
            with zipfile.ZipFile(archive,'w') as z:
                z.writestr('app.ts','const first=1;')
                z.writestr('app.ts','const second=2;')
        result=inventory.inspect(archive)
        self.assertEqual(len(result['files']),1)
        self.assertEqual(result['files'][0]['sha256'],hashlib.sha256(b'const first=1;').hexdigest())
        self.assertTrue(result['incomplete'])
        self.assertEqual(result['skipped'][0]['reason'],'duplicate-path')

    def test_invalid_zip_reports_a_clear_error(self):
        source=self.root/'broken.zip';source.write_bytes(b'not an archive')
        with self.assertRaisesRegex(ValueError,'not a valid ZIP'):
            inventory.inspect(source)


if __name__=='__main__':
    unittest.main()
