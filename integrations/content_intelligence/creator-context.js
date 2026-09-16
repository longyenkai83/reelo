// Shared read-only creator context. No creator identity or preference defaults.
// Included verbatim in batch-content.js. Paths originate in the operator manifest
// (V2) or explicit legacy workspace input; this does not discover/read new files.
function creatorContext(assets, legacyWorkspace = false) {
  const list = Array.isArray(assets) ? assets : []
  const names = new Set(['about-me.md', 'voice-profile.md', 'writing-rules.md',
    'writing-rules-chi-tiet.md', 'kho-cta.md', 'kho-cau-chuyen.md'])
  const selected = list.filter(a => a && typeof a.path === 'string' &&
    names.has(a.path.replaceAll('\\', '/').split('/').at(-1)))
  if (legacyWorkspace && !selected.length) return 'CREATOR CONTEXT — no explicit asset list. ' +
    'Use only the creator already explicitly selected in the existing private workspace, following the existing brand checks. ' +
    'Read its voice/preferences/CTA and sourced Story; do not infer a creator or substitute another workspace. ' +
    'If no creator is selected or required context is missing, report missing context. No default creator name or voice.'
  return 'CREATOR CONTEXT — use only explicitly supplied creator assets below. ' +
    'Voice, preferred address, cadence, CTA and lived examples belong to this creator, never to shared Reelo. ' +
    'Read the supplied voice/profile/preferences and keep their intended behavior for this creator. ' +
    'Creator references do not establish customer truth. Use Story only with its approved classification and source. ' +
    'No supplied creator value means no assumed name, CTA, life example or voice preference. ' +
    'Report missing required context; never substitute another creator. No recursive discovery or additional permission.\n' +
    JSON.stringify(selected)
}
