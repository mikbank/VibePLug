#!/usr/bin/env python3
"""Create a deterministic Microsoft 365 admin ZIP; never provisions a tenant."""
import argparse
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]

def default_output():
    version=json.loads((ROOT/'plugin'/'manifest.json').read_text(encoding='utf-8'))['version']
    return ROOT/'dist'/f'niras-app-migration-{version}.zip'

def package(source, destination):
    files=sorted(p for p in source.rglob('*') if p.is_file())
    if any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('Symlinks cannot be packaged')
    destination.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in files:
            relative=path.relative_to(source).as_posix()
            if any(part.startswith('.') or part=='__pycache__' for part in path.relative_to(source).parts):
                raise ValueError('Hidden/generated file in plugin: '+relative)
            if path.suffix=='.pyc':raise ValueError('Compiled Python file in plugin')
            entry=zipfile.ZipInfo(relative,date_time=(2026,11,13,0,0,0))
            entry.compress_type=zipfile.ZIP_DEFLATED
            entry.external_attr=0o100644 << 16
            archive.writestr(entry,path.read_bytes())
    return len(files)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=default_output())
    args=parser.parse_args()
    count=package(ROOT/'plugin',args.output)
    print(f'Packaged {count} files: {args.output}')
