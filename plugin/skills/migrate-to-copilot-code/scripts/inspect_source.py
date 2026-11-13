#!/usr/bin/env python3
"""Bounded, read-only source inventory. No source execution or network access."""

from __future__ import annotations

import argparse
import bisect
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile


MAX_FILES = 10000
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_TOTAL_BYTES = 100 * 1024 * 1024
EXCLUDED_DIRS = {'.git', '.svn', 'node_modules', 'dist', 'build', '.next',
                 '.output', 'coverage', '__pycache__', '.venv', 'vendor'}
TEXT_SUFFIXES = {'.html', '.htm', '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs',
                 '.css', '.scss', '.json', '.sql', '.md', '.txt', '.yaml', '.yml',
                 '.xml', '.vue', '.svelte', '.py', '.cs', '.sh', '.toml'}
SECRET_SUFFIXES = {'.pem', '.key', '.p12', '.pfx', '.keystore'}
HINTS = {
    'browser-storage': r'\b(?:localStorage|sessionStorage|indexedDB)\b',
    'supabase-client': r'\b(?:supabase|createClient)\b',
    'sql-policy': r'\b(?:create\s+policy|row\s+level\s+security)\b',
    'sql-table': r'\bcreate\s+table\b',
    'sql-function-trigger': r'\bcreate\s+(?:or\s+replace\s+)?(?:function|trigger)\b',
    'server-code': r'\b(?:createServerFn|createServerFileRoute|Deno\.serve|use server)\b',
    'network-call': r'\b(?:fetch\s*\(|axios\b|XMLHttpRequest\b|WebSocket\b)',
    'auth-permission': r'\b(?:signIn|signOut|auth\.uid|role|permission|isAdmin)\b',
    'file-import-export': r'\b(?:FileReader|showOpenFilePicker|xlsx|SheetJS|jsPDF|Blob)\b',
    'host-interaction': r'\b(?:window\.print|window\.confirm|Worker\s*\(|OffscreenCanvas)\b',
    'date-calculation': r'\b(?:Date\.UTC|setMonth|getTimezoneOffset|daysPerMonth)\b',
    'lovable-dependency': r'\b(?:lovable|gptengineer)\b',
}
PATTERNS = {key: re.compile(value, re.I) for key, value in HINTS.items()}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_parts(name: str) -> tuple[str, ...] | None:
    if '\\' in name or '\x00' in name or name.startswith('/'):
        return None
    parts = PurePosixPath(name).parts
    if not parts or any(p in ('..', '.') or ':' in p for p in parts):
        return None
    return parts


def excluded(name: str) -> str | None:
    parts = PurePosixPath(name).parts
    if any(p in EXCLUDED_DIRS for p in parts[:-1]):
        return 'generated-or-vendor-directory'
    base = parts[-1].lower()
    if (base.startswith('.env') or base in {'.npmrc', '.pypirc', 'credentials',
            'credentials.json', 'secrets.json', 'id_rsa', 'id_ed25519'}
            or Path(base).suffix in SECRET_SUFFIXES):
        return 'credential-file'
    return None


class HTMLInventory(HTMLParser):
    """Use HTML raw-text rules; never execute or regex-extract the document."""

    def __init__(self, source: str):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.starts = [0] + [m.end() for m in re.finditer('\n', source)]
        self.elements: list[dict] = []
        self.open_element: dict | None = None
        self.body_lines: list[int] = []
        self.inline_handler_count = 0

    def source_offset(self) -> int:
        line, col = self.getpos()
        return self.starts[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.body_lines.append(self.getpos()[0])
        self.inline_handler_count += sum(1 for k, _ in attrs if k.lower().startswith('on'))
        if tag not in ('script', 'style'):
            return
        attributes = dict(attrs)
        kind = attributes.get('type') or ''
        kind = 'module' if kind == 'module' else 'data' if 'json' in kind else 'classic'
        self.open_element = {
            'tag': tag, 'line': self.getpos()[0], 'start_offset': self.source_offset(),
            'content_start_offset': self.source_offset() + len(self.get_starttag_text() or ''),
            'external': 'src' in attributes, 'script_kind': kind,
        }

    def handle_endtag(self, tag):
        if self.open_element and tag == self.open_element['tag']:
            self.finish(self.source_offset(), closed=True)

    def finish(self, end: int, *, closed: bool):
        entry = self.open_element
        if not entry:
            return
        content = self.source[entry['content_start_offset']:end]
        entry.update({
            'content_end_offset': end,
            'end_line': bisect.bisect_right(self.starts, end),
            'content_characters': len(content), 'content_sha256': sha(content.encode()),
            'closed': closed,
            'vendor_hint': bool(re.search(r'SheetJS|jsPDF|@license|copyright|webpackBootstrap', content[:4096], re.I)),
        })
        self.elements.append(entry)
        self.open_element = None

    def report(self):
        self.feed(self.source)
        self.close()
        if self.open_element:
            self.finish(len(self.source), closed=False)
        return {
            'script_style_elements': self.elements,
            'body_start_lines': self.body_lines,
            'inline_event_attribute_count': self.inline_handler_count,
            'parser_note': 'HTMLParser raw-text boundaries are hints; verify malformed HTML manually. No code or attribute values are emitted.',
        }


def summarize_text(name: str, data: bytes) -> dict:
    try:
        source = data.decode('utf-8-sig')
    except UnicodeDecodeError:
        return {'analysis': 'not-utf8; inspect with appropriate decoder'}
    newlines = [m.start() for m in re.finditer('\n', source)]
    hints = {}
    for key, pattern in PATTERNS.items():
        count, lines = 0, []
        for match in pattern.finditer(source):
            count += 1
            if len(lines) < 8:
                line = bisect.bisect_left(newlines, match.start()) + 1
                if line not in lines:
                    lines.append(line)
        if count:
            hints[key] = {'count': count, 'first_lines': lines}
    result = {'line_count': source.count('\n') + 1, 'hints': hints}
    if PurePosixPath(name).name == 'package.json':
        try:
            package = json.loads(source)
            deps = set()
            for key in ('dependencies', 'devDependencies', 'peerDependencies'):
                if isinstance(package.get(key), dict):
                    deps.update(str(k) for k in package[key])
            result['package'] = {
                'dependency_names': sorted(deps)[:500],
                'dependencies_truncated': len(deps) > 500,
                'has_lifecycle_hooks': any(k in package.get('scripts', {}) for k in ('preinstall', 'install', 'postinstall', 'prepare')),
                'stack_hints': [s for s, p in [('tanstack-start', '@tanstack/react-start'),
                    ('react', 'react'), ('vite', 'vite'), ('next', 'next'), ('supabase', '@supabase/supabase-js')]
                    if p in deps],
            }
        except (ValueError, AttributeError, TypeError):
            result['package_error'] = 'Invalid or unexpected package JSON shape'
    if Path(name).suffix.lower() in ('.html', '.htm'):
        result['html'] = HTMLInventory(source).report()
    return result


def inspect(source: Path) -> dict:
    if source.is_symlink():
        raise ValueError('Source must not be a symbolic link')
    if not source.exists():
        raise ValueError('Source does not exist')
    result = {
        'inventory_version': 1,
        'source_label': source.name,
        'read_only': True,
        'source_content_is_untrusted': True,
        'limits': {'max_files': MAX_FILES, 'max_file_bytes': MAX_FILE_BYTES,
                   'max_total_bytes': MAX_TOTAL_BYTES},
        'limitations': [
            'Heuristic inventory only; does not recover complete business logic or permissions.',
            'No source execution, dependency installation, ZIP extraction or network access.',
            'Generated/vendor directories, recognized credential files and symlinks are excluded.',
            'Hashes cover complete files only when within the byte limits.',
            'Embedded secrets in ordinary code are not scanned or certified absent; content snippets are never emitted.',
        ],
        'files': [], 'skipped': [], 'issues': [], 'incomplete': False,
    }
    total = 0
    seen = set()

    def skip(path, reason, incomplete=False):
        if len(result['skipped']) < 1000:
            result['skipped'].append({'path': path, 'reason': reason})
        result['incomplete'] |= incomplete

    def add(name, size, reader):
        nonlocal total
        if len(result['files']) >= MAX_FILES:
            skip(name, 'file-count-limit', True)
            return False
        if name in seen:
            skip(name, 'duplicate-path', True)
            return True
        seen.add(name)
        reason = excluded(name)
        if reason:
            skip(name, reason)
            return True
        if size > MAX_FILE_BYTES:
            skip(name, 'file-byte-limit', True)
            return True
        if total + size > MAX_TOTAL_BYTES:
            skip(name, 'total-byte-limit', True)
            return False
        try:
            data = reader()
        except (OSError, RuntimeError, ValueError, zipfile.BadZipFile):
            skip(name, 'read-error', True)
            return True
        if len(data) > MAX_FILE_BYTES or total + len(data) > MAX_TOTAL_BYTES:
            skip(name, 'observed-byte-limit', True)
            return False
        total += len(data)
        entry = {'path': name, 'bytes': len(data), 'sha256': sha(data)}
        if Path(name).suffix.lower() in TEXT_SUFFIXES:
            entry.update(summarize_text(name, data))
        else:
            entry['analysis'] = 'hash-only; no text analysis for this file type'
        result['files'].append(entry)
        return True

    def file_reader(path):
        # Refuse a link swapped in between discovery and opening where supported.
        flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
        fd = os.open(path, flags)
        with os.fdopen(fd, 'rb') as handle:
            if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
                raise ValueError('Non-regular file')
            return handle.read(MAX_FILE_BYTES + 1)

    if source.is_dir():
        stopped = False
        def walk_error(_):
            result['issues'].append('Directory access error; inventory is incomplete')
            result['incomplete'] = True
        for base, dirs, files in os.walk(source, followlinks=False, onerror=walk_error):
            kept = []
            for name in sorted(dirs):
                path = Path(base) / name
                if path.is_symlink() or name in EXCLUDED_DIRS:
                    skip(path.relative_to(source).as_posix(), 'symlink-or-excluded-directory')
                else:
                    kept.append(name)
            dirs[:] = kept
            for name in sorted(files):
                path = Path(base) / name
                relative = path.relative_to(source).as_posix()
                try:
                    info = path.lstat()
                except OSError:
                    skip(relative, 'stat-error', True)
                    continue
                if not stat.S_ISREG(info.st_mode):
                    skip(relative, 'symlink-or-nonregular-file')
                    continue
                if not add(relative, info.st_size, lambda p=path: file_reader(p)):
                    stopped = True
                    break
            if stopped:
                break
    elif zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as archive:
            entries = archive.infolist()
            if len(entries) > MAX_FILES * 2:
                raise ValueError('Archive has too many entries for this bounded inventory')
            for info in sorted(entries, key=lambda x: x.filename):
                if info.is_dir():
                    continue
                if safe_parts(info.filename) is None:
                    skip('[unsafe archive entry]', 'unsafe-archive-path', True)
                    continue
                if stat.S_ISLNK(info.external_attr >> 16) or info.flag_bits & 1:
                    skip(info.filename, 'archive-symlink-or-encrypted-entry', True)
                    continue
                def read_entry(entry=info):
                    with archive.open(entry) as handle:
                        return handle.read(MAX_FILE_BYTES + 1)
                if not add(info.filename, info.file_size, read_entry):
                    break
    elif source.suffix.lower() == '.zip':
        raise ValueError('Source has a ZIP extension but is not a valid ZIP archive')
    elif source.is_file():
        add(source.name, source.stat().st_size, lambda: file_reader(source))
    else:
        raise ValueError('Expected a directory, ZIP archive or regular file')
    result['summary'] = {'files_read': len(result['files']), 'bytes_read': total,
                         'skipped_paths_reported': len(result['skipped'])}
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Local directory, code ZIP or HTML file')
    parser.add_argument('--output', type=Path, help='Write JSON here instead of stdout')
    args = parser.parse_args(argv)
    try:
        if args.output and args.output.resolve() == args.source.resolve():
            raise ValueError('Output must not overwrite source')
        report = inspect(args.source)
        encoded = json.dumps(report, indent=2, ensure_ascii=True) + '\n'
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            # Do not overwrite any existing source, evidence or unresolved run record.
            with args.output.open('x', encoding='utf-8') as handle:
                handle.write(encoded)
        else:
            print(encoded, end='')
        return 0
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f'Inventory failed: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
