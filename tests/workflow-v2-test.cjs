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
const pass = () => ({ verdict: 'PASS', truth_preserved: true, selected_intent_preserved: true, limitations_preserved: true,
  external_claims_safe: true, title_criteria: Array(8).fill(true), issues: [] })
async function run(queue, bound = true) {
  const prompts = []
  const env = { args: [], log: () => {}, parallel: jobs => Promise.all(jobs.map(job => job())),
    agent: async (prompt, options) => { prompts.push({prompt, options}); const next = queue.shift(); if (next instanceof Error) throw next; return next } }
  if (bound) env.V2_BOUND = { execution: { receipt: { context_hash: 'test' }, generation_id: 'g', status: 'RUNNING', critic_status: 'NOT_RUN' }, context: structuredClone(context), assets: [] }
  const result = await vm.runInNewContext('(async()=>{' + script + '})()', env)
  return { result, prompts, env }
}
;(async () => {
  let r = await run([draft(), pass()])
  assert.equal(r.result.execution.status, 'DRAFT_READY')
  assert.equal(r.prompts[1].options.agentType, 'critic-ban-giam-khao')
  assert.equal(JSON.stringify(r.env.V2_BOUND.context), JSON.stringify(context))
  for (const field of ['truth_preserved', 'selected_intent_preserved', 'limitations_preserved', 'external_claims_safe']) {
    let fail = pass(); fail[field] = false
    r = await run([draft(), fail, draft(), fail])
    assert.equal(r.result.execution.status, 'CRITIC_FAILED', field)
    assert.equal(r.prompts.length, 4)
    assert.equal(r.result.execution.artifacts.length, 2)
    assert.equal(r.result.execution.artifacts[1].parent_version, 1)
  }
  r = await run([draft(), null, draft(), pass()])
  assert.equal(r.result.execution.status, 'DRAFT_READY')
  r = await run([new Error('child died')])
  assert.equal(r.result.execution.status, 'CRITIC_FAILED')
  let bad = draft(); bad.customer_evidence_ids = ['invented']
  r = await run([bad]); assert.equal(r.result.execution.status, 'CRITIC_FAILED'); assert.equal(r.prompts.length, 1)
  r = await run([], false); assert(Array.isArray(r.result)); assert.equal(r.prompts.length, 0)
  console.log('V2 workflow truth, bounded rewrite, failure slots, immutable context, legacy empty path PASS')
})().catch(e => { console.error(e); process.exitCode = 1 })
