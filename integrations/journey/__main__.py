"""Opt-in local CLI. Human commands are operator-only, never model tools."""
import argparse
import json
import sys
from pathlib import Path

from integrations.content_intelligence.host import HostConfig, NativeHost
from .models import CampaignRequest, Source
from .strategy import propose_flow
from .store import CampaignStore
from .engine import JourneyEngine


def load(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description='Reelo Journey — local planning and bounded draft execution; no publish')
    parser.add_argument('--store', required=True, type=Path)
    sub=parser.add_subparsers(dest='command',required=True)
    explore=sub.add_parser('explore'); explore.add_argument('--request',required=True);explore.add_argument('--sources',required=True)
    explore.add_argument('--history')
    inspect=sub.add_parser('inspect');inspect.add_argument('--plan-hash',required=True)
    decide=sub.add_parser('decide');decide.add_argument('--plan-hash',required=True)
    decide.add_argument('--action',required=True,choices=['AUTHORIZE_AUTOPILOT','APPROVE_SAMPLE','EXECUTE_REMAINDER','REVOKE'])
    decide.add_argument('--reviewer',required=True);decide.add_argument('--confirm-human',action='store_true')
    decide.add_argument('--authority-ref',required=True);decide.add_argument('--sample-hash');decide.add_argument('--calibration')
    for command in ('prepare','run','batch','approve-sample-plan'):
        p=sub.add_parser(command);p.add_argument('--plan-hash',required=True);p.add_argument('--config',required=True)
        if command=='prepare':p.add_argument('--slot',required=True)
        if command in ('run','approve-sample-plan'):p.add_argument('--creative-plan-id',required=True)
        if command=='approve-sample-plan':
            p.add_argument('--reviewer',required=True);p.add_argument('--confirm-human',action='store_true');p.add_argument('--authority-ref',required=True)
    args=parser.parse_args(argv);store=CampaignStore(args.store)
    if args.command=='explore':
        request=CampaignRequest.model_validate(load(args.request))
        sources=[Source.model_validate(s) for s in load(args.sources)]
        # Historical plans remain immutable; imported metadata never grants execution.
        plan=propose_flow(request,sources,history=load(args.history) if args.history else ())
        output=dict(plan_hash=store.save(plan),plan=plan.model_dump(),execution_authorized=False)
    elif args.command=='inspect':
        output=dict(plan=store.load(args.plan_hash).model_dump(),memory=store.memory(args.plan_hash))
    elif args.command=='decide':
        output=dict(event_id=store.decide(args.plan_hash,args.action,reviewer=args.reviewer,
            human_attested=args.confirm_human,authority_ref=args.authority_ref,sample_hash=args.sample_hash,
            calibration=load(args.calibration) if args.calibration else None))
    else:
        cfg=load(args.config)
        # A generic CLI cannot guess where CURRENT authoritative CI ledgers live.
        # CI campaigns use the API with the producer's actual current-ledger callback.
        if any(s.kind=='VERIFIED_INSIGHT' for s in store.load(args.plan_hash).sources):
            raise ValueError('use_journey_api_with_current_insight_authority')
        host=NativeHost(HostConfig(executable=Path(cfg['executable']),execution_workspace=Path(cfg['execution_workspace']),
            state_directory=Path(cfg['state_directory']),read_files=tuple(Path(p) for p in cfg['read_files']),
            timeout_seconds=cfg.get('timeout_seconds',600),max_budget_usd=cfg.get('max_budget_usd',5),
            effort_level=cfg.get('effort_level')))
        engine=JourneyEngine(store,host.config.state_directory,host.invoke_stage,host.config.read_files)
        if args.command=='prepare':output=engine.prepare(args.plan_hash,args.slot)
        elif args.command=='run':output=engine.run(args.plan_hash,args.creative_plan_id).model_dump(mode='json')
        elif args.command=='batch':output=[r.model_dump(mode='json') for r in engine.execute_remaining(args.plan_hash)]
        else:output=dict(event_id=engine.approve_sample_plan(args.plan_hash,args.creative_plan_id,
            reviewer=args.reviewer,human_attested=args.confirm_human,authority_ref=args.authority_ref))
    print(json.dumps(output,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
