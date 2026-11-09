/**
 * Offline export regression suite: all static lesson links, PDF, image and
 * social metadata must be usable without calling the Cloudflare Worker.
 */
import assert from "node:assert/strict";
import {execFileSync} from "node:child_process";
import {readFileSync,existsSync,readdirSync} from "node:fs";
import {resolve,join,dirname} from "node:path";
import {fileURLToPath} from "node:url";

const root=resolve(dirname(fileURLToPath(import.meta.url)),"../..");
const base="https://omnimaster-study-room-share.onrender.com";
execFileSync(process.execPath,["docs/interactive/export_static.mjs"],{
  cwd:root,env:{...process.env,OMNIMASTER_PUBLIC_ORIGIN:base},stdio:"pipe"
});
const dir=resolve(root,"docs/interactive/.static-publish");
const read=p=>readFileSync(join(dir,p));
const man=JSON.parse(read("manifest.json").toString("utf8"));
assert.equal(man.lessons,54);
assert.equal(man.routes,59);
assert.equal(man.publicOrigin,base);
assert.ok(man.files.find(f=>f.route==="/downloads/omnimaster-fullstack.pdf"));
const htmls=man.files.filter(f=>f.name.endsWith(".html"));
assert.equal(htmls.length,56,"54 course articles, one catalogue and one homepage");
let checked=0;
const localRefs=[];
for(const file of htmls){
 const html=read(file.name.slice(1)).toString("utf8");
 const socialTitle=html.match(/property="og:title" content="([^"]+)"/);
 assert.ok(socialTitle,"OG title absent: "+file.name);
 assert.match(html,/property="og:description"/);
 assert.match(html,/property="og:image"/);
 assert.match(html,/name="twitter:card" content="summary_large_image"/);
 assert.ok(!html.includes("omnimaster-study-room.cabo-solutions-za.workers.dev"),"Old host leaks: "+file.name);
 assert.ok(html.includes('property="og:image" content="'+base+'/og/omnimaster-study-room.png"'));
 const rawPath=file.route==="/"?"/":file.name;
 assert.ok(html.includes('property="og:url" content="'+base+rawPath+'"'),"Canonical share URL incorrect: "+file.name);
 const links=[...html.matchAll(/\bhref="([^"]+)"/g)].map(x=>x[1]);
 for(const href of links) {
  if(href.startsWith("#")||href.startsWith("mailto:")||/^https?:\/\//i.test(href))continue;
  const dest=new URL(href,base+rawPath);
  if(dest.origin!==base)continue;
  let path=dest.pathname;
  if(path==="/")path="/index.html";
  const filepath=resolve(dir,"."+path);
  if(!filepath.startsWith(dir+"/"))throw new Error("Unsafe link "+href);
  localRefs.push({from:file.name,href,to:path,exists:existsSync(filepath)});
 }
 checked++;
}
const broken=localRefs.filter(x=>!x.exists);
assert.deepEqual(broken,[],"Static site must not have unresolved local hyperlinks");
const home=read("index.html").toString("utf8");
assert.match(home,/id="share-study-room"/);
assert.ok(home.includes('data-share-url="'+base+'/'));
assert.ok(home.includes('href="/library.html"'));
const listing=read("library.html").toString("utf8");
assert.equal((listing.match(/class="catalogue-card"/g)||[]).length,54);
assert.match(listing,/href="\/OMNIMASTER_FULLSTACK_PLAYBOOK.html"/);
assert.match(listing,/id="lesson-search"/);
const preview=read("og/omnimaster-study-room.png");
assert.equal(preview.subarray(0,8).toString("hex"),"89504e470d0a1a0a");
assert.equal(preview.readUInt32BE(16),1200);
assert.equal(preview.readUInt32BE(20),630);
const pdf=read("downloads/omnimaster-fullstack.pdf");
assert.equal(pdf.subarray(0,8).toString("utf8"),"%PDF-1.4");
assert.ok(pdf.length>10000);
assert.ok(pdf.includes(Buffer.from('/F1 3 0 R')),'Page must reference Helvetica font object');
assert.ok(!pdf.includes(Buffer.from('/F1 4 0 R')),'Regression: page wrongly referenced as font');
assert.ok(pdf.toString("latin1").includes("%%EOF"));
assert.match(read("robots.txt").toString("utf8"),/Allow: \//);
assert.match(read("sitemap.xml").toString("utf8"),/OMNIMASTER_FULLSTACK_PLAYBOOK.html/);
console.log("Static mirror PASS:",checked,"HTML pages,",localRefs.length,"local links; canonical preview, PNG and PDF verified.");
