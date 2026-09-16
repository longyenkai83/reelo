const fs = require('fs')
const assert = require('assert/strict')
const vm = require('vm')
const raw = fs.readFileSync('.claude/workflows/batch-content.js', 'utf8')
const moduleBody = fs.readFileSync('integrations/content_intelligence/workflow-v2.js', 'utf8')
assert(raw.includes(moduleBody), 'embedded V2 module drift')
const script = raw.replace('export const meta', 'const meta')
const packet = JSON.parse(fs.readFileSync('integrations/content_intelligence/contracts/fixtures/synthetic-content-intelligence-packet.json', 'utf8'))
const context = { schema_version: 'reelo.execution-context.1', packet }
const draft = () => ({ status: 'DRAFT', content: 'SYNTHETIC draft only', title: 'Synthetic title', format: 'Reel', issues: [],
  customer_evidence_ids: [packet.customer_truth.verified_insight.evidence_refs[0].evidence_id],
  external_dispositions: packet.external_evidence_requirements.map(r => ({ strategy_field: r.strategy_field, disposition: 'omitted', explanation: 'Not supported' })) })
const pass = () => ({ title_meaning_clear: true, reader_centered_pov: true, non_prescriptive_tone: true, findings: [], verdict: 'PASS', truth_preserved: true, selected_intent_preserved: true, limitations_preserved: true,
  external_claims_safe: true, creator_truth_preserved: true, context_scope_preserved: true,
  source_verification_complete: true, title_criteria: Array(8).fill(true), blocking_issues: [], notes: [] })
async function run(queue, bound = true, inputContext = context, stageType = 'WRITER', selectedMode = null, legacyItems = []) {
  const prompts = []
  const env = { args: legacyItems, log: () => {}, parallel: jobs => Promise.all(jobs.map(job => job())),
    agent: async (prompt, options) => { prompts.push({prompt, options}); const next = queue.shift(); if (next instanceof Error) throw next; return next } }
  if (bound) env.V2_BOUND = { execution: { receipt: { context_hash: 'test' }, generation_id: 'g', status: 'RUNNING', critic_status: 'NOT_RUN' }, context: structuredClone(inputContext), assets: [], stage: {stage_type: stageType, stage_id: 'stage', input_hash: 'test'}, inputs: {approved_plan: {decision: 'approved', selected_hook: {text:'SYNTHETIC hook'}, selected_title:{text:'Synthetic title'}, approved_outline:['Synthetic outline']}, draft: draft(), critic: pass()} }
  if (bound && selectedMode) env.V2_BOUND.inputs.approved_plan.selected_mode = selectedMode
  const result = await vm.runInNewContext('(async()=>{' + script + '})()', env)
  return { result, prompts, env }
}
;(async () => {
  const semantics = JSON.parse(fs.readFileSync('integrations/content_intelligence/semantics-a1.json', 'utf8'))
  for (const [mode, rule] of Object.entries(semantics.modes)) {
    for (const stageType of ['WRITER', 'CRITIC1', 'REWRITE', 'CRITIC2']) {
      const output = stageType.startsWith('CRITIC') ? pass() : draft()
      const r = await run([output], true, context, stageType, mode)
      const {prompt, options} = r.prompts[0]
      assert(prompt.includes(rule.representation))
      assert(prompt.includes('"selected_mode":"' + mode + '"'))
      assert(prompt.includes('Selected hook/title are exact approved wording; use them unchanged.'))
      if (stageType.startsWith('CRITIC')) {
        assert.equal(options.schema.properties.title_criteria.minItems, semantics.title_checks.length)
        assert.equal(options.schema.properties.title_criteria.maxItems, semantics.title_checks.length)
        assert.deepEqual(Array.from(options.schema.properties.verdict.enum), ['PASS', 'REVISE'])
        for (const category of semantics.hard_categories)
          assert(options.schema.properties.findings.items.properties.category.enum.includes(category))
      }
    }
  }
  for (const kind of ['comparison', 'question_answer', 'story']) {
    const selected = structuredClone(context)
    selected.packet.content_strategy.angle.angle_type = kind
    selected.packet.content_strategy.angle.opening_direction.text = 'SELECTED_OPENING_' + kind
    selected.packet.content_strategy.angle.core_argument.text = 'SELECTED_ARGUMENT_' + kind
    for (const stageType of ['WRITER', 'CRITIC1', 'REWRITE', 'CRITIC2']) {
      const output = stageType.startsWith('CRITIC') ? pass() : draft()
      const r = await run([output, new Error('must never run a second agent')], true, selected, stageType)
      assert.equal(r.prompts.length, 1)
      assert.equal(r.result.schema_version, 'reelo.host-stage.1')
      assert.equal(r.result.stage.stage_type, stageType)
      assert.equal(JSON.stringify(r.result.output), JSON.stringify(output))
      assert.equal(JSON.stringify(r.env.V2_BOUND.context), JSON.stringify(selected))
      const {prompt, options} = r.prompts[0]
      for (const text of ['SELECTED_OPENING_' + kind, 'SELECTED_ARGUMENT_' + kind, 'No forced axis',
                         'psychology or story treatment', 'independent Critic must read',
                         'AUTHORITATIVE EXECUTION IDENTITY', 'IMMUTABLE PACKET', 'OWNER-CONFIRMED V2 QUALITY', 'personal-story-first', 'Do not disguise a meaningless contrast by paraphrasing it', 'Keep the reader', 'Invite reflection']) assert(prompt.includes(text))
      if (stageType === 'WRITER') {
        assert(prompt.includes('HUMAN-APPROVED INTERNAL CREATIVE PLAN'))
        assert(!prompt.includes('**' + String.fromCodePoint(110,103,104,7883,99,104,32,108,253) + '**'))
      }
      if (stageType.startsWith('CRITIC')) {
        assert.equal(options.agentType, 'critic-ban-giam-khao')
        assert.equal(options.schema.properties.title_criteria.minItems, 8)
        for (const key of ['title_meaning_clear', 'reader_centered_pov', 'non_prescriptive_tone']) {
          assert(options.schema.required.includes(key))
        }
        assert(prompt.includes('do not count pronouns'))
        assert(prompt.includes('Never trust writer self-certification'))
      }
      assert.equal(options.schema.additionalProperties, false)
    }
  }
  await assert.rejects(() => run([new Error('child died')]), /child died/)
  await assert.rejects(() => run([], true, context, 'UNKNOWN'), /TRUSTED_STAGE_REQUIRED/)
  const planner = await run([{status:'PROPOSED'}], true, context, 'CREATIVE_PLAN')
  assert(planner.prompts[0].prompt.includes('WHAT TO SAY is locked'))
  assert(planner.prompts[0].prompt.includes('external knowledge cannot become creator story'))
  assert(planner.prompts[0].prompt.includes('No article, approval or writes'))
  const legacy = await run([], false)
  assert(Array.isArray(legacy.result)); assert.equal(legacy.prompts.length, 0)
  for (const revise of [false, true]) {
    const metadata = {ten:'Synthetic legacy', file:'synthetic-only.md', ok:true, dinh_dang:'Reel'}
    const queue = revise ? [metadata, {verdict:'CẦN SỬA', loi:['synthetic']}, {}, {verdict:'ĐẠT'}]
                         : [metadata, {verdict:'ĐẠT'}]
    const old = await run(queue, false, context, 'WRITER', null, [{chu_de:'SYNTHETIC ONLY'}])
    assert.equal(old.prompts.length, revise ? 4 : 2)
    assert(old.result[0].critic.includes('ĐẠT'))
    assert(old.prompts[0].prompt.includes('Reel 170–220'))
    assert(old.prompts[1].prompt.includes('Chấm đủ 7 ô'))
    assert(!old.prompts[1].prompt.includes('V2 override'))
    assert.equal(old.prompts[1].options.schema.properties.title_criteria, undefined)
  }
  console.log('Single-stage schema/craft/Zone-B/context gates and legacy empty path PASS')
})().catch(e => { console.error(e); process.exitCode = 1 })
