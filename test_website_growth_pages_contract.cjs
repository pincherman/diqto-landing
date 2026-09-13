const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const cp = require('node:child_process');
const root = __dirname;
const contract = JSON.parse(fs.readFileSync(path.join(root, 'config/public_website_pages.json')));
const backend = process.env.DIQTO_BACKEND_ROOT || path.resolve(root, '../batiboss');
assert.deepEqual(contract, JSON.parse(fs.readFileSync(path.join(backend, 'config/public_website_pages.json'))), 'frontend/backend closed registry drift');
const constants = JSON.parse(cp.execFileSync('python3', ['-c',
  'import ast,json,sys; t=ast.parse(open(sys.argv[1]).read()); names={"ALLOWED_PLACEMENTS","PUBLIC_EVENTS","ALLOWED_STATUSES"}; print(json.dumps({n.targets[0].id:sorted(ast.literal_eval(n.value)) for n in t.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in names}))',
  path.join(backend, 'services/growth_events.py')], {encoding:'utf8'}));
const code = fs.readFileSync(path.join(root, 'growth.js'), 'utf8');
const shell = fs.readFileSync(path.join(root, 'site-shell.js'), 'utf8');
const pageKeys = new Set(contract.pages.map(p=>p.key));
function environment(pathname='/', search='', hostname='diqto.fr') {
  const sent=[]; const listeners={}; const saved={}; let id=0;
  const context = {
    URL, URLSearchParams, Date, Math,
    window: {
      location:{pathname,search,hostname,origin:`https://${hostname}`},
      crypto:{randomUUID:()=>String(++id).padStart(32,'0')},
      sessionStorage:{getItem:k=>saved[k]||null,setItem:(k,v)=>saved[k]=v},
      fetch:(_url,o)=>{sent.push(JSON.parse(o.body));return Promise.resolve({ok:true});},
    },
    document:{body:{getAttribute:()=>null},querySelectorAll:()=>[],addEventListener:(name,fn)=>{(listeners[name] ||= []).push(fn);}},
  };
  vm.createContext(context);
  return {sent,context,run:()=>vm.runInContext(code,context),click:(href,placement,container='')=>{
    const link={getAttribute:name=>name==='href'?href:name==='data-growth-placement'?placement:null,closest:selector=>selector===container?link:null};
    for(const fn of listeners.click||[])fn({target:{closest:()=>link}});
  }};
}
function accepted(payload) {
  assert(pageKeys.has(payload.page), `unrecognized page ${payload.page}`);
  assert(constants.PUBLIC_EVENTS.includes(payload.event));
  assert(constants.ALLOWED_PLACEMENTS.includes(payload.placement), `placement ${payload.placement}`);
  assert(constants.ALLOWED_STATUSES.includes(payload.status));
  assert(!JSON.stringify(payload).includes('https://'));
}
let routeCount=0;
for(const p of contract.pages)for(const route of [p.path,...p.aliases]){
  const e=environment(route);e.run();e.run();
  assert.equal(e.sent.length,1,'double script must not duplicate view');
  assert.equal(e.sent[0].page,p.key);accepted(e.sent[0]);
  e.click('https://apps.apple.com/fr/app/diqto/id6761616034',null,'.global-header');
  assert.equal(e.sent.length,2,'one click only');accepted(e.sent[1]);
  assert.equal(e.sent[1].event,'appstore_outbound');assert.equal(e.sent[1].placement,'header');
  const file=route==='/'?'index.html':route.slice(1);
  const html=fs.readFileSync(path.join(root,file),'utf8');
  assert(html.includes('site-shell.js'),`${file}: shared bootstrap missing`);
  const re=/data-growth-placement="([^"]+)"/g;
  for(const m of html.matchAll(re)){e.click('https://apps.apple.com/fr/app/diqto/id6761616034',m[1]);accepted(e.sent.at(-1));}
  routeCount++;
}
for(const route of ['/private@example.test','/tmp/preview.html','/unknown.html']){const e=environment(route);e.run();assert.equal(e.sent.length,0);}
for(const host of ['localhost','diqto.fr.attacker.test']){const e=environment('/','',host);e.run();assert.equal(e.sent.length,0);}
for(const source of ['constructor','__proto__','private@example.test']){
  const e=environment('/plombier.html',`?source=${source}&client=secret@example.test`);e.run();
  assert.equal(e.sent[0].source,'direct_or_organic');assert(!JSON.stringify(e.sent).includes('secret@example.test'));
  e.context.window.diqtoGrowthTrack('constructor','private@example.test','constructor');assert.equal(e.sent.length,1);
}
const e=environment('/');e.run();e.click('https://apps.apple.com.attacker.test/id6761616034',null);assert.equal(e.sent.length,1);
e.click('https://apps.apple.com/fr/app/other/id0000000000',null);assert.equal(e.sent.length,1);
for(const [alias,expected]of Object.entries({final:'final_cta','intent-evening':'hero',hero_ec_demo:'hero',offer_ec_demo:'expert_entry'})){
  e.click('https://apps.apple.com/fr/app/diqto/id6761616034',alias);assert.equal(e.sent.at(-1).placement,expected);
}
// Header-free documents still load tracking; duplicate/static script loads do not.
for(const existing of [false,true]){
  const added=[];let marked=existing;
  const doc={head:{appendChild:s=>{added.push(s);marked=true;}},querySelector:q=>q.startsWith('script[')&&marked?{}:null,createElement:()=>({setAttribute:()=>{}})};
  const c={window:{},document:doc};vm.runInNewContext(shell,c);vm.runInNewContext(shell,c);
  assert.equal(added.length,existing?0:1);
}
console.log(`PASS website growth payload/backend contract: ${contract.pages.length} pages, ${routeCount} routes, idempotence/privacy/legacy placements`);
