// Deterministic assembly only. No model, host, source writes or private files.
const fs = require('fs')
const vm = require('vm')
const assert = require('assert/strict')
const cases = JSON.parse(fs.readFileSync('tests/creator-workspaces.json', 'utf8'))
const raw = fs.readFileSync('.claude/workflows/batch-content.js', 'utf8')
const helper = fs.readFileSync('integrations/content_intelligence/creator-context.js', 'utf8').trimEnd()
assert(raw.includes(helper), 'creator context embedded mirror drift')
const assemble = vm.runInNewContext(helper + '\ncreatorContext')
const packet = JSON.parse(fs.readFileSync('integrations/content_intelligence/contracts/fixtures/synthetic-content-intelligence-packet.json', 'utf8'))
const badTitle = 'Tiền thuê nặng, hay phần giữ lại đang mỏng?'
;(async () => {
  for (const c of cases) {
    const other = cases.find(x => x.id !== c.id)
    const files = {
      'about-me.md': c.name, 'voice-profile.md': c.voice, 'writing-rules.md': c.writing,
      'kho-cta.md': c.cta, 'kho-cau-chuyen.md': c.story,
    }
    const assets = Object.keys(files).map(name => ({path:'/synthetic/brand/'+c.id+'/'+name, sha256:'synthetic-hash'}))
    const description = assemble(assets)
    const selected = JSON.parse(description.slice(description.indexOf('\n') + 1))
    assert.deepEqual(selected, assets)
    // Simulated authorized Read: compare every supplied preference/source intact.
    const suppliedMemory = selected.map(a => files[a.path.split('/').at(-1)]).join('\n')
    for (const value of [c.name, c.voice, c.cta, c.writing, c.story]) assert(suppliedMemory.includes(value))
    assert(!suppliedMemory.includes(other.name))
    assert(!suppliedMemory.includes(other.cta))
    assert(!suppliedMemory.includes(other.story))
    for (const type of ['WRITER', 'CRITIC1', 'REWRITE', 'CRITIC2']) {
      const captured = []
      const bound = {context:{packet}, execution:{receipt:{}}, assets,
        stage:{stage_type:type}, inputs:{
          approved_plan:{decision:'approved',selected_mode:'SHORT_ARTICLE'},
          draft:{format:'SHORT_ARTICLE'}, critic:{notes:[]},
        }}
      const env = {args:[], V2_BOUND:structuredClone(bound), log:()=>{},
        agent:async (prompt,options)=>{captured.push({prompt,options});return {synthetic:true}}}
      await vm.runInNewContext('(async()=>{'+raw.replace('export const meta','const meta')+'})()',env)
      assert.equal(captured.length,1)
      const prompt=captured[0].prompt
      assert(prompt.includes(description))
      assert(!prompt.includes(other.id))
      assert(!prompt.includes('Hiền')) // Identity is not hard-coded; real text is read from supplied source.
      assert(!prompt.includes(badTitle))
      for (const clause of ['Keep the reader', 'Invite reflection', 'Do not disguise a meaningless contrast',
                            'Selected hook/title are exact approved wording']) assert(prompt.includes(clause))
      assert.equal(JSON.stringify(env.V2_BOUND.assets),JSON.stringify(assets))
    }
    const prompts=[]
    const queue=[{ten:'SYNTHETIC',file:'synthetic.md',ok:true,dinh_dang:'Reel'},{verdict:'ĐẠT'}]
    const env={args:[{chu_de:'SYNTHETIC',creator_assets:assets}],log:()=>{},
      parallel:jobs=>Promise.all(jobs.map(job=>job())),
      agent:async prompt=>{prompts.push(prompt);return queue.shift()}}
    await vm.runInNewContext('(async()=>{'+raw.replace('export const meta','const meta')+'})()',env)
    assert.equal(prompts.length,2)
    for (const prompt of prompts) assert(prompt.includes(description))
  }
  const empty=assemble([])
  assert(empty.endsWith('[]'))
  for(const c of cases) assert(!empty.includes(c.name) && !empty.includes(c.cta))
  const noStory=assemble([{path:'/synthetic/brand/creator-b/voice-profile.md',sha256:'fixture'}])
  assert(!noStory.includes('kho-cau-chuyen.md'))
  console.log('Creator A/B, missing context, legacy/V2 assembly and case-neutral quality PASS')
})().catch(e=>{console.error(e);process.exitCode=1})
