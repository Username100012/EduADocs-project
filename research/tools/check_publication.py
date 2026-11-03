"""Read-only credential scan and original snapshot integrity check. No networks."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
PATTERNS={
 'google_api_key':r'AIza[\w-]{30,}',
 'openai_api_key':r'sk-(?:proj-)?[\w-]{30,}',
 'huggingface_token':r'hf_[A-Za-z0-9]{20,}',
 'github_token':r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})',
 'aws_access_key':r'(?:AKIA|ASIA)[A-Z0-9]{16}',
 'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
}
SENSITIVE=re.compile(r'^(?:api[_-]?key|password|secret|authorization|access[_-]?token|refresh[_-]?token|client[_-]?secret)$',re.I)
MASKS={'','[REDACTED]','***','redacted','<redacted>','[redacted]'}


def check(root=ROOT, known_env_file=None):
    findings=[]; count=0; known=[]
    if known_env_file:
        for line in Path(known_env_file).read_text(encoding='utf-8').splitlines():
            key,sep,value=line.partition('=')
            value=value.strip().strip('\"\'')
            if sep and re.search(r'key|secret|password|token',key,re.I) and len(value)>=8:
                known.append(value)
    compiled={k:re.compile(v) for k,v in PATTERNS.items()}
    def inspect(value,path,where):
        if isinstance(value,dict):
            for key,item in value.items():
                if SENSITIVE.fullmatch(key) and isinstance(item,str) and item not in MASKS:
                    findings.append({'path':path,'type':'nonempty_credential_field','location':where+'.'+key})
                inspect(item,path,where+'.'+key)
        elif isinstance(value,list):
            for i,item in enumerate(value):inspect(item,path,where+f'[{i}]')
    for path in root.rglob('*'):
        if not path.is_file() or any(x in path.relative_to(root).parts for x in ['.git','.venv','__pycache__','reproduced']):continue
        relative=path.relative_to(root).as_posix()
        if path.name.startswith('.env') or path.name in ['secrets.toml','credentials.json'] or path.suffix in ['.pem','.key','.p12','.pfx']:
            findings.append({'path':relative,'type':'sensitive_filename'})
        try:text=path.read_text(encoding='utf-8-sig')
        except UnicodeError:
            findings.append({'path':relative,'type':'unreviewed_binary'});continue
        count+=1
        for name,pattern in compiled.items():
            if pattern.search(text):findings.append({'path':relative,'type':name})
        if any(value in text for value in known):findings.append({'path':relative,'type':'known_local_secret'})
        if path.suffix=='.json':
            inspect(json.loads(text),relative,'$')
        elif path.suffix=='.jsonl':
            for n,line in enumerate(text.splitlines(),1):
                if line.strip():inspect(json.loads(line),relative,f'line:{n}')
    manifest=json.loads((root/'MANIFEST_SHA256.json').read_text(encoding='utf-8'))
    changed=[name for name,item in manifest.items() if not (root/name).is_file() or sha256((root/name).read_bytes()).hexdigest()!=item['sha256']]
    return {'files_scanned':count,'known_local_secrets_checked':len(known),'findings':findings,
            'original_files_verified':len(manifest),'original_snapshot_changed':changed,'api_calls':0}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--known-env-file',type=Path);p.add_argument('--output',type=Path);args=p.parse_args()
    report=check(known_env_file=args.known_env_file)
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report));raise SystemExit(bool(report['findings'] or report['original_snapshot_changed']))
