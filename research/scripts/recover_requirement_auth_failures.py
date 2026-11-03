"""Manual, single recovery of pre-existing HTTP 401 attempts after key correction.

No semantic/validation failure is eligible. Original logs remain unchanged.
The same evaluation IDs and requests are retained in a separate attempt log.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from run_requirement_judgments import load as load_original, execute
from check_openai_judge import read_key


def load(source, directory):
    original = directory.parent/'judge-contract-v2-preparation'
    plan, queue, mapping, candidates = load_original(source, original)
    events=list(map(json.loads,(original/'judgments.v2.jsonl').read_text(encoding='utf-8').splitlines()))
    failed={e['evaluation_id']:e for e in events[1:] if e['event']=='result' and e['status']=='api_error' and e['http_status']==401}
    # Bounded exception for the two authentication failures predating key correction.
    if len(failed)!=2:
        raise ValueError('expected exactly the two historical authentication failures')
    selected=[q for q in queue if q['evaluation_id'] in failed]
    recovery_plan={'event':'plan','protocol':'manual-auth-recovery-v1','planned':2,
        'automatic_retries':0,'attempt':2,'original_plan':plan,
        'prior_failed_attempts_sha256':{eid:sha256(json.dumps(e,sort_keys=True,ensure_ascii=False).encode()).hexdigest() for eid,e in sorted(failed.items())},
        'policy':'Only two pre-existing HTTP 401 failures, no prior model response. No validation/semantic failures eligible. Original IDs and request bodies retained; separate attempt log.'}
    directory.mkdir(parents=True,exist_ok=True)
    return recovery_plan,selected,{eid:mapping[eid] for eid in failed},candidates


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--live',action='store_true')
    args=parser.parse_args()
    if args.live:
        key=read_key()
        if not key:
            raise SystemExit('credential absent')
        result=execute(args.source,args.directory,key,max_jobs=2,workers=2,plan_loader=load)
        print(json.dumps({'completed':result['completed'],'statuses':result['statuses']}))
    else:
        plan,*_=load(args.source,args.directory)
        print(json.dumps({'planned':plan['planned'],'api_calls':0,'policy':plan['policy']}))
