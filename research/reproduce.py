"""Recompute the main-study tables in an isolated copy, with network blocked."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'reproduced')
    parser.add_argument('--tests',action='store_true',help='Also run the original offline unittest suite.')
    args=parser.parse_args(); output=args.output.resolve()
    if output.exists() and any(output.iterdir()):raise SystemExit('Output directory is not empty; choose a new directory.')
    source_hashes={name:sha256((ROOT/name).read_bytes()).hexdigest() for name in ['artifacts/main-study-v1/generations.jsonl','artifacts/main-judgments-v1/judgments.v2.jsonl']}
    with tempfile.TemporaryDirectory(prefix='eduadocs-reproduction-') as tmp:
        work=Path(tmp)
        for name in ['src','scripts','tests','docs','experiments','artifacts']:
            shutil.copytree(ROOT/name,work/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        shutil.copyfile(ROOT/'requirements.txt', work/'requirements.txt')
        blocker=work/'offline_guard';blocker.mkdir()
        (blocker/'sitecustomize.py').write_text('import socket\ndef deny(*a, **k):\n    raise RuntimeError("Network disabled during offline reproduction")\nsocket.socket.connect = deny\nsocket.create_connection = deny\n',encoding='utf-8')
        env=os.environ.copy();env['PYTHONPATH']=os.pathsep.join([str(blocker),str(work/'src'),str(work/'scripts')]);env['PYTHONDONTWRITEBYTECODE']='1'
        # The offline route neither loads .env nor invokes live executors.
        for key in list(env):
            if any(x in key.upper() for x in ['API_KEY','ACCESS_TOKEN','SECRET_KEY']):env.pop(key,None)
        commands=[['scripts/freeze_main_study.py'],
                  ['scripts/observe_saved_requirements.py','artifacts/main-study-v1'],
                  ['scripts/summarize_main_observations.py','artifacts/main-study-v1'],
                  ['scripts/report_requirement_results.py','artifacts/main-study-v1','artifacts/main-judgments-v1']]
        if args.tests:commands.append(['-m','unittest','discover','-s','tests'])
        for command in commands:
            result=subprocess.run([sys.executable,*command],cwd=work,env=env,text=True,encoding='utf-8',errors='replace',capture_output=True)
            if result.returncode:
                print(result.stdout);print(result.stderr,file=sys.stderr);raise SystemExit(result.returncode)
            print('OK:', ' '.join(command),flush=True)
        compared=['artifacts/main-study-v1/requirement_observations.v1.json',
                  'artifacts/main-study-v1/automatic_summary.v1.json',
                  'artifacts/main-judgments-v1/results_tables.json']
        metadata_differences=[]
        for name in compared:
            original=json.loads((ROOT/name).read_text(encoding='utf-8'))
            new=json.loads((work/name).read_text(encoding='utf-8'))
            if name.endswith('automatic_summary.v1.json'):
                # observe() serializes the derived JSON using OS line endings.
                # Validate each provenance hash against its actual bytes, then
                # compare the analysis payload exactly; do not rewrite outputs.
                key='source_observations_sha256'
                observed='artifacts/main-study-v1/requirement_observations.v1.json'
                assert original[key]==sha256((ROOT/observed).read_bytes()).hexdigest()
                assert new[key]==sha256((work/observed).read_bytes()).hexdigest()
                if original[key]!=new[key]:
                    metadata_differences.append({'file':name,'field':key,
                        'reason':'OS line endings in derived observations; JSON content identical',
                        'published':original[key],'recomputed':new[key]})
                original.pop(key);new.pop(key)
            if original!=new:
                raise SystemExit('Recomputed analysis data differ: '+name)
        for name,digest in source_hashes.items():
            if sha256((work/name).read_bytes()).hexdigest()!=digest or sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
                raise SystemExit('Raw log changed: '+name)
        output.mkdir(parents=True,exist_ok=True)
        copied=[]
        for folder,names in {
            'main-study-v1':['requirement_observations.v1.json','automatic_summary.v1.json','AUTOMATIC_METRICS.md','automatic_fields.v1.csv','automatic_operations.v1.csv','automatic_duration.v1.csv'],
            'main-judgments-v1':['results_tables.json','RESULTS.md','requirements_by_condition.csv','requirements_by_task.csv'],
        }.items():
            (output/folder).mkdir()
            for name in names:
                shutil.copyfile(work/'artifacts'/folder/name,output/folder/name);copied.append(folder+'/'+name)
        report={'api_calls':0,'network_blocked':True,'analysis_payloads_equal_to_published':compared,'serialization_metadata_differences':metadata_differences,
                'raw_logs_unchanged':True,'raw_sha256':source_hashes,'tests_run':args.tests,
                'python':sys.version.split()[0],'outputs':copied}
        (output/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':main()
