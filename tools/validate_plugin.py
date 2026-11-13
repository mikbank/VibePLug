#!/usr/bin/env python3
"""Validate manifest against Microsoft's saved schema plus ZIP/skill constraints."""
import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import re
import sys
import uuid
import zipfile

from jsonschema import validators, FormatChecker
from PIL import Image
import yaml

ROOT=Path(__file__).resolve().parents[1]
SAFE=re.compile(r'^[A-Za-z0-9_. !-]+$')
KEBAB=re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
RESERVED={'CON','PRN','AUX','NUL'}|{f'{p}{n}' for p in ('COM','LPT') for n in range(1,10)}

def validate(archive_path,schema_path):
    checks=[]
    def require(test,label):
        if not test:raise ValueError(label)
        checks.append(label)
    with zipfile.ZipFile(archive_path) as archive:
        require(archive.testzip() is None,'ZIP CRC integrity')
        names=archive.namelist()
        require(len(names)==len(set(names)),'No duplicate ZIP entries')
        for name in names:
            path=PurePosixPath(name)
            require(not path.is_absolute() and '\\' not in name and '\x00' not in name
                and all(p not in ('..','.') and not p.startswith('.') and SAFE.fullmatch(p)
                        and p.split('.')[0].upper() not in RESERVED for p in path.parts),
                'Safe package path: '+name)
        require('manifest.json' in names,'Manifest at ZIP root')
        manifest=json.loads(archive.read('manifest.json'))
        expected_schema=f"https://developer.microsoft.com/json-schemas/teams/v{manifest['manifestVersion']}/MicrosoftTeams.schema.json"
        require(manifest.get('$schema')==expected_schema,'Microsoft manifest schema/version agreement')
        schema=json.loads(schema_path.read_text())
        validator=validators.validator_for(schema)
        # This vendor schema uses ECMAScript Unicode property escapes in unused
        # optional extension definitions. Python's metaschema regex format check
        # cannot parse that dialect. Validate this manifest against the unchanged
        # official schema, without meta-validating the vendor's regex syntax.
        errors=sorted(validator(schema,format_checker=FormatChecker()).iter_errors(manifest),key=lambda e:str(e.path))
        require(not errors,'Official Microsoft manifest schema: '+'; '.join(e.message for e in errors))
        require(str(uuid.UUID(manifest['id']))==manifest['id'],'Stable valid app UUID')
        require(not any(p in json.dumps(manifest).lower() for p in ('example.com','your-guid','contoso','placeholder')),'No placeholder manifest metadata')
        for key,size in [('color',(192,192)),('outline',(32,32))]:
            path=manifest['icons'][key]
            require(path in names,'Icon exists: '+key)
            with Image.open(BytesIO(archive.read(path))) as image:
                require(image.format=='PNG' and image.size==size,'PNG dimensions: '+key)
                if key=='outline':
                    rgba=image.convert('RGBA')
                    pixels=[rgba.getpixel((x,y)) for y in range(size[1]) for x in range(size[0])]
                    require(any(p[3]==0 for p in pixels),'Outline has transparent background')
                    require(all(p[:3]==(255,255,255) for p in pixels if p[3]>0),'Outline is white on transparency')
        skills=manifest.get('agentSkills',[])
        require(1<=len(skills)<=20,'Supported skill count')
        folders=[entry['folder'] for entry in skills]
        require(len(folders)==len(set(folders)),'Unique declared skill folders')
        file_summary=[]
        for folder in folders:
            normalized=folder.removeprefix('./').rstrip('/')
            skill_file=normalized+'/SKILL.md'
            require(skill_file in names,'Declared SKILL.md exists: '+normalized)
            content=archive.read(skill_file).decode('utf-8')
            match=re.match(r'^---\n(.*?)\n---\n',content,re.S)
            require(bool(match),'YAML frontmatter: '+normalized)
            front=yaml.safe_load(match.group(1))
            require(isinstance(front,dict) and 1<=len(front.get('name',''))<=64
                and bool(KEBAB.fullmatch(front['name'])) and front['name']==PurePosixPath(normalized).name,
                'Kebab-case frontmatter matches folder: '+normalized)
            require(isinstance(front.get('description'),str) and 1<=len(front['description'])<=1024,
                'Skill description length: '+normalized)
            require(len(content.split())<2000,'Lean SKILL.md word count: '+normalized)
            companions=[name for name in names if name.startswith(normalized+'/') and name!=skill_file]
            sizes=[archive.getinfo(name).file_size for name in companions]
            require(len(companions)<=20 and all(s<=5*1024*1024 for s in sizes) and sum(sizes)<=10*1024*1024,
                'Companion file/count limits: '+normalized)
            for target in re.findall(r'`((?:references|scripts)/[^`]+)`',content):
                target=target.split(' ',1)[0]
                require(normalized+'/'+target in names,'Referenced companion exists: '+target)
            file_summary.append({'skill':front['name'],'words':len(content.split()),'companions':len(companions)})
        require(not manifest.get('agentConnectors'),'Skills-only package has no undeclared server dependencies')
        require(all(name in ('manifest.json','color.png','outline.png') or any(name.startswith(f.removeprefix('./')+'/') for f in folders) for name in names),
            'Only manifest, icons and declared skills in upload ZIP')
    return {'result':'passed','checks':len(checks),'archive_sha256':hashlib.sha256(archive_path.read_bytes()).hexdigest(),
        'schema_sha256':hashlib.sha256(schema_path.read_bytes()).hexdigest(),'app_id':manifest['id'],
        'version':manifest['version'],'manifest_version':manifest['manifestVersion'],
        'files':len(names),'skills':file_summary,
        'not_tested':['Microsoft tenant upload/ingestion','Skill activation in Cowork/Code','End-to-end source migration','Live SharePoint operations','App deployment/player launch'],
        'notes':['Local checks cover the saved Microsoft schema and documented package constraints; tenant-specific validation is separate.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path)
    parser.add_argument('--schema',type=Path)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    try:
        if args.schema is None:
            with zipfile.ZipFile(args.archive) as archive:
                manifest_version=json.loads(archive.read('manifest.json'))['manifestVersion']
            if not re.fullmatch(r'1\.[0-9]+',manifest_version):
                raise ValueError('Unsupported manifest schema version')
            args.schema=ROOT/'schemas'/f'MicrosoftTeams-v{manifest_version}.schema.json'
        result=validate(args.archive,args.schema)
        encoded=json.dumps(result,indent=2)+'\n'
        if args.report:args.report.write_text(encoded)
        print(encoded,end='')
    except Exception as exc:
        print('Validation failed: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
