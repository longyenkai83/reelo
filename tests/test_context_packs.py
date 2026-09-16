"""D1 synthetic context tests: no model calls or private sources."""
import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path

import pytest

from integrations.content_intelligence.context_packs import assemble, asset_id, manifest, ROOT
from integrations.content_intelligence.creative_plan import validate_proposal
from tests.test_creative_plan import setup


@pytest.fixture
def pack_fixture(setup, tmp_path):
    _, context, approval, assets, store = setup
    assets = deepcopy(assets)
    paths = {}
    for name, body in {
        'brand/creator-b/voice-profile.md': 'PRIVATE B VOICE distinctive rhythm',
        'brand/creator-b/about-me.md': 'PRIVATE B IDENTITY',
        'brand/creator-b/kho-cau-chuyen.md': '# selected\nPRIVATE SELECTED STORY\n# unused\nUNUSED STORY BODY',
        'wiki/selected.md': '# selected\nPRIVATE KNOWLEDGE SUPPORT\n# unused\nUNUSED KNOWLEDGE BODY',
        'wiki/unrelated.md': '# other\nUNRELATED WIKI',
        'hook-system.md': 'HOOK CANDIDATE LIBRARY',
        'bo-tieu-de.md': 'TITLE CANDIDATE LIBRARY',
        'deep-lexical.md': 'UNRELATED LEXICAL',
    }.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding='utf8')
        paths[name] = path
        assets.append(dict(path=path.as_posix(), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    approval = deepcopy(approval)
    approval['selected_mode'] = 'SHORT_ARTICLE'
    return context, approval, assets, paths, store


def match(path, origin):
    return dict(source_ref=path.as_posix(), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                section='selected', origin=origin, support_quote='', match_type='ADJACENT',
                why_relevant='SYNTHETIC', allowed_use='SYNTHETIC')


def test_planner_metadata_is_available_not_loaded(pack_fixture):
    _, _, assets, _, _ = pack_fixture
    pack, trace = assemble('CREATIVE_PLAN', {}, assets)
    text = json.dumps(pack)
    for body in ('UNUSED STORY BODY', 'UNRELATED WIKI', 'HOOK CANDIDATE LIBRARY', 'UNRELATED LEXICAL'):
        assert body not in text
    assert 'PRIVATE B VOICE' in text and 'PRIVATE B IDENTITY' in text
    assert len(pack['knowledge']['recipe']) == 9
    assert pack['available_for_matching']
    assert trace['load_summary']['OMITTED'] > 0


@pytest.mark.parametrize('stage', ['WRITER', 'CRITIC1', 'REWRITE', 'CRITIC2'])
def test_selected_source_sections_only_and_trace_has_no_private_text(pack_fixture, stage):
    _, approval, assets, paths, _ = pack_fixture
    approval['selected_story_refs'] = [match(paths['brand/creator-b/kho-cau-chuyen.md'], 'creator_story')]
    approval['selected_knowledge_refs'] = [match(paths['wiki/selected.md'], 'external_knowledge')]
    pack, trace = assemble(stage, {'approved_plan': approval}, assets)
    text = json.dumps(pack)
    assert 'PRIVATE SELECTED STORY' in text and 'PRIVATE KNOWLEDGE SUPPORT' in text
    assert 'UNUSED STORY BODY' not in text and 'UNUSED KNOWLEDGE BODY' not in text
    assert 'UNRELATED WIKI' not in text
    assert 'PRIVATE' not in json.dumps(trace)
    assert all(r['model_read'] == 'UNKNOWN' for r in trace['receipts'])
    if stage in ('WRITER', 'REWRITE'):
        assert 'HOOK CANDIDATE LIBRARY' not in text
        assert 'TITLE CANDIDATE LIBRARY' not in text
        assert 'Synthetic alternative' not in text
        assert pack['knowledge']['recipe']['job'] == 'TEACH'
        assert 'repair_layers' in pack['knowledge'] if stage == 'REWRITE' else True


def test_none_story_and_unused_knowledge_have_no_bodies(pack_fixture):
    _, approval, assets, _, _ = pack_fixture
    pack, trace = assemble('WRITER', {'approved_plan': approval}, assets)
    assert pack['source_support'] == []
    assert 'PRIVATE SELECTED STORY' not in json.dumps(pack)
    assert 'PRIVATE KNOWLEDGE SUPPORT' not in json.dumps(pack)
    assert all('OMITTED' in r['states'] for r in trace['receipts'] if r['role'] in ('STORY', 'KNOWLEDGE'))


def test_critic_reads_again_not_writer_self_report(pack_fixture):
    _, approval, assets, paths, _ = pack_fixture
    path = paths['wiki/selected.md']
    approval['selected_knowledge_refs'] = [match(path, 'external_knowledge')]
    assemble('WRITER', {'approved_plan': approval}, assets)
    path.write_text('# selected\nCHANGED SUPPORT', encoding='utf8')
    with pytest.raises(ValueError, match='context_asset_load_failed') as caught:
        assemble('CRITIC1', {'approved_plan': approval}, assets)
    assert any('READ_FAILED' in r['states'] for r in caught.value.trace['receipts'])


@pytest.mark.parametrize('mode', ['REEL', 'SHORT_ARTICLE', 'LONG_ARTICLE'])
def test_mode_projection_and_exact_approval_words(pack_fixture, mode):
    _, approval, assets, _, _ = pack_fixture
    approval['selected_mode'] = mode
    pack, _ = assemble('WRITER', {'approved_plan': approval}, assets)
    assert ('VISUAL' in pack['knowledge']['hook']) == (mode == 'REEL')
    assert ('AUDIO' in pack['knowledge']['hook']) == (mode == 'REEL')
    assert pack['approved_plan']['selected_hook'] == approval['selected_hook']
    assert pack['approved_plan']['selected_title'] == approval['selected_title']


def test_reference_identity_not_display_annotations(pack_fixture):
    _, _, assets, paths, _ = pack_fixture
    rid = asset_id(paths['hook-system.md'])
    selection = dict(asset_id=rid, stages=['CREATIVE_PLAN'], display_note='useful opening')
    first, _ = assemble('CREATIVE_PLAN', {}, assets, [selection])
    selection['display_note'] = 'path.md (principle #2 and #3)'
    second, _ = assemble('CREATIVE_PLAN', {}, assets, [selection])
    assert first == second
    selection['asset_id'] += ' (principle #2)'
    with pytest.raises(ValueError, match='unknown_reference_identity'):
        assemble('CREATIVE_PLAN', {}, assets, [selection])


def test_explicit_planner_story_section_not_full_vault(pack_fixture):
    _, _, assets, paths, _ = pack_fixture
    selection = dict(asset_id=asset_id(paths['brand/creator-b/kho-cau-chuyen.md']),
                     stages=['CREATIVE_PLAN'], display_note='candidate', section='selected')
    pack, _ = assemble('CREATIVE_PLAN', {}, assets, [selection])
    assert 'PRIVATE SELECTED STORY' in json.dumps(pack)
    assert 'UNUSED STORY BODY' not in json.dumps(pack)
    del selection['section']
    with pytest.raises(ValueError, match='context_asset_load_failed'):
        assemble('CREATIVE_PLAN', {}, assets, [selection])


def test_editorial_explicit_section_overrides_recent_table_default(pack_fixture, tmp_path):
    _, _, assets, _, _ = pack_fixture
    path = tmp_path / '_INDEX.md'
    path.write_text('# recent\nRECENT ENTRY\n# archive\nOLD CAMPAIGN', encoding='utf8')
    assets.append(dict(path=path.as_posix(), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    selection = dict(asset_id=asset_id(path), stages=['CREATIVE_PLAN'], section='recent')
    pack, _ = assemble('CREATIVE_PLAN', {}, assets, [selection])
    assert 'RECENT ENTRY' in json.dumps(pack) and 'OLD CAMPAIGN' not in json.dumps(pack)
    with pytest.raises(ValueError, match='duplicate_reference_selection'):
        assemble('CREATIVE_PLAN', {}, assets, [selection, selection])


@pytest.mark.parametrize('creator', ['creator-b', 'nhi-hien'])
def test_configured_creator_only(tmp_path, creator):
    path = tmp_path / creator / 'voice-profile.md'
    path.parent.mkdir(); path.write_text('SYNTHETIC ' + creator)
    assets = manifest([path], ROOT)
    pack, _ = assemble('CREATIVE_PLAN', {}, assets)
    assert pack['creator_assets'][0]['text'] == 'SYNTHETIC ' + creator
    assert len(pack['creator_assets']) == 1


def test_old_plan_readable_not_upgraded_and_job_change_invalidates(setup):
    _, context, approval, assets, store = setup
    old = deepcopy(approval['plan']['proposal'])
    old.pop('content_job'); old.pop('recipe_id')
    old_plan = store.save(old, context, assets, 'SYNTHETIC-OLD')
    assert 'content_job' not in store.get(old_plan['creative_plan_id'])['proposal']
    reviewed = store.review(old_plan['creative_plan_id'], dict(decision='approved', reviewer='SYNTHETIC TEST',
        human_attested=True, approval_kind='synthetic_fixture', expected_plan_hash=old_plan['plan_hash']))
    assert 'recipe_id' not in store.approved(reviewed['approval_id'], context, assets)['plan']['proposal']
    with pytest.raises(ValueError, match='invalid_canonical_job_recipe'):
        assemble('WRITER', {'approved_plan': reviewed}, assets)
    new = deepcopy(old); new.update(content_job='REFLECT', recipe_id='c1:REFLECT')
    store.save(new, context, assets, 'SYNTHETIC-NEW')
    with pytest.raises(ValueError, match='approval_not_current'):
        store.approved(reviewed['approval_id'], context, assets)


def test_new_job_and_recipe_must_match_catalog(setup):
    _, context, approval, assets, _ = setup
    raw = deepcopy(approval['plan']['proposal']); raw['recipe_id'] = 'c1:REFLECT'
    with pytest.raises(ValueError, match='invalid_canonical_job_recipe'):
        validate_proposal(raw, context, assets)


def test_psychology_stable_id_and_path_both_validated(setup):
    _, context, approval, assets, _ = setup
    raw = deepcopy(approval['plan']['proposal'])
    raw['psychology']['reference_id'] = asset_id(raw['psychology']['library_source'])
    assert validate_proposal(raw, context, assets)['psychology']['reference_id']
    id_only = deepcopy(raw); id_only['psychology'].pop('library_source')
    assert validate_proposal(id_only, context, assets)['psychology']['library_source'] == raw['psychology']['library_source']
    raw['psychology']['library_source'] += ' (principle #2)'
    with pytest.raises(ValueError, match='psychology_reference_identity_mismatch'):
        validate_proposal(raw, context, assets)


def test_load_evidence_and_auto_injection_unknown(pack_fixture):
    _, approval, assets, _, _ = pack_fixture
    _, trace = assemble('WRITER', {'approved_plan': approval}, assets)
    assert trace['auto_injection']['status'] == 'UNKNOWN'
    voice = next(r for r in trace['receipts'] if r['role'] == 'VOICE')
    assert voice['states'] == ['ALLOWED', 'SELECTED', 'READ_ATTEMPTED', 'READ_SUCCEEDED']
    omitted = next(r for r in trace['receipts'] if r['role'] == 'STORY')
    assert omitted['sha256'] and omitted['states'] == ['ALLOWED', 'OMITTED']
    assert 'not a model read' in voice['hash_verification']


@pytest.mark.parametrize('stage', ['CREATIVE_PLAN', 'WRITER', 'CRITIC1', 'REWRITE', 'CRITIC2'])
def test_pack_reaches_actual_agent_prompt_without_exploration_leak(pack_fixture, stage):
    context, approval, assets, _, _ = pack_fixture
    inputs = dict(approved_plan=approval, draft={'format': 'SHORT_ARTICLE'}, critic={'findings': []},
                  plan_schema={}, asset_roles=[])
    if stage == 'CREATIVE_PLAN': inputs.pop('approved_plan')
    pack, _ = assemble(stage, inputs, assets)
    bound = dict(context=context, execution={'receipt': {}}, assets=[], inputs=inputs,
                 stage={'stage_type': stage}, context_pack=pack)
    code = """
const fs=require('fs'),vm=require('vm');
const bound=JSON.parse(fs.readFileSync(0,'utf8'));
const script=fs.readFileSync('.claude/workflows/batch-content.js','utf8').replace('export const meta','const meta');
let calls=[];
const env={args:[],V2_BOUND:bound,log:()=>{},agent:async(p,o)=>{calls.push(p);return {synthetic:true}}};
(async()=>{await vm.runInNewContext('(async()=>{'+script+'})()',env);process.stdout.write(JSON.stringify(calls))})();
"""
    result = subprocess.run(['node', '-e', code], input=json.dumps(bound), text=True,
                            encoding='utf8', capture_output=True, cwd=ROOT, check=True)
    calls = json.loads(result.stdout)
    assert len(calls) == 1
    prompt = calls[0]
    assert 'D1 STAGE CONTEXT PACK' in prompt and 'PRIVATE B VOICE' in prompt
    assert 'UNUSED STORY BODY' not in prompt and 'UNRELATED WIKI' not in prompt
    if stage in ('WRITER', 'REWRITE'):
        assert 'Synthetic alternative' not in prompt
        assert 'HOOK CANDIDATE LIBRARY' not in prompt
        assert 'TITLE CANDIDATE LIBRARY' not in prompt
    if stage != 'CREATIVE_PLAN':
        assert approval['selected_hook']['text'] in prompt
        assert approval['selected_title']['text'] in prompt
