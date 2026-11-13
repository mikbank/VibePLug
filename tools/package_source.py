#!/usr/bin/env python3
"""Bundle editable plugin source, research and local validation evidence."""
import argparse
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'dist'/'niras-app-migration-source-1.0.0.zip')
    args=parser.parse_args()
    paths=[]
    for folder in ('plugin','schemas','tools','tests','evaluations'):
        paths.extend(p for p in (ROOT/folder).rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and p.suffix!='.pyc')
    paths.extend(p for p in ROOT.iterdir() if p.is_file() and p.suffix in ('.md','.txt','.json'))
    paths.append(ROOT/'dist'/'niras-app-migration-1.0.0.zip')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for p in sorted(set(paths)):
            entry=zipfile.ZipInfo(p.relative_to(ROOT).as_posix(),date_time=(2026,11,13,0,0,0))
            entry.compress_type=zipfile.ZIP_DEFLATED
            entry.external_attr=0o100644 << 16
            archive.writestr(entry,p.read_bytes())
    print(f'Packaged {len(set(paths))} source/evidence files: {args.output}')

if __name__=='__main__':main()
