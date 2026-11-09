/* Integration tests for the generated offline-bundled study website. */
import assert from "node:assert/strict";
import {execFileSync} from "node:child_process";
import {readFileSync} from "node:fs";
import {resolve,dirname} from "node:path";
import {fileURLToPath,pathToFileURL} from "node:url";
const root=resolve(dirname(fileURLToPath(import.meta.url)),"../..");
execFileSync(process.execPath,["docs/interactive/build_worker.mjs"],{cwd:root,stdio:"pipe"});
const built=readFileSync(resolve(root,"docs/interactive/.generated-study-room-worker.mjs"),"utf8");
const file=await import("data:text/javascript;base64,"+Buffer.from(built).toString("base64"));
const worker=file.default;
const url="https://omnimaster-study-room.cabo-solutions-za.workers.dev";
let assertions=0;
async function check(path,expectStatus,expectedContentType){
 const response=await worker.fetch(new Request(url+path));
 assert.equal(response.status,expectStatus,path);
 if(expectedContentType)assert.match(response.headers.get("content-type"),expectedContentType);
 assertions++;return response;
}
const home=await check("/",200,/text\/html/);
const html=await home.text();
assert.ok(html.includes("OMNIMASTER_FULLSTACK_PLAYBOOK.md"));
assert.ok(html.includes("/downloads/omnimaster-fullstack.pdf"));
assert.ok(!html.includes("github.com/CayelaemJ"));
assert.ok(!html.includes("blob/main"));
const catalogue=await check("/library",200,/text\/html/);
const catalogueHtml=await catalogue.text();
assert.ok(catalogueHtml.includes('id="lesson-search"'),"Search input missing");
assert.ok(catalogueHtml.includes('id="lesson-filter"'),"Category selector missing");
assert.ok(catalogueHtml.includes('id="catalogue-count"'),"Live result count missing");
assert.ok(catalogueHtml.includes("54 lessons"),"Incorrect course catalogue total");
assert.equal((catalogueHtml.match(/class="catalogue-card"/g)||[]).length,54,"Every approved lesson must be discoverable");
assert.ok(catalogueHtml.includes('href="/reliability/01_JOBS_AND_STATE.md"'),"Reliability course missing");
assert.ok(catalogueHtml.includes('href="/OMNIMASTER_FULLSTACK_PLAYBOOK.md"'),"Full-stack textbook missing");
assert.ok(!catalogueHtml.includes('href="https://github.com/'),"Catalogue must not send learners into GitHub source");
assert.ok(catalogueHtml.includes('search.addEventListener("input",render)'),"Local-only search logic missing");
const catalogueHead=await worker.fetch(new Request(url+"/library",{method:"HEAD"}));
assert.equal(catalogueHead.status,200);
assert.equal((await catalogueHead.arrayBuffer()).byteLength,0);
const socialOrigin="https://omnimaster-study-room.cabo-solutions-za.workers.dev";
const socialImage=socialOrigin+"/og/omnimaster-study-room.png";
function validateSocialMeta(text,path,expectedTitle){
 for(const tag of ['property="og:title"','property="og:description"','property="og:url"',
                   'property="og:image"','property="og:type"','property="og:image:width"','property="og:image:height"',
                   'name="twitter:card"','name="twitter:image"']) {
   assert.ok(text.includes(tag),"Social metadata missing: "+tag+" on "+path);
 }
 assert.ok(text.includes('property="og:url" content="'+socialOrigin+path+'"'),"Bad canonical URL "+path);
 assert.ok(text.includes('property="og:image" content="'+socialImage+'"'),"Bad preview image URL");
 assert.ok(text.includes('property="og:image:width" content="1200"'));
 assert.ok(text.includes('property="og:image:height" content="630"'));
 assert.ok(text.includes('name="twitter:card" content="summary_large_image"'));
 assert.ok(text.includes('content="'+expectedTitle+'"'),"Wrong page-specific share title "+path);
 assert.ok(!text.includes('href="https://github.com/'),"Preview page links to source repository");
}
validateSocialMeta(html,"/","OmniMaster Study Room | Learn Engineering");
validateSocialMeta(catalogueHtml,"/library","54 Free Engineering Lessons | OmniMaster");
const socialResponse=await check("/og/omnimaster-study-room.png",200,/image\/png/);
const socialBytes=Buffer.from(await socialResponse.arrayBuffer());
assert.ok(socialBytes.length>20000 && socialBytes.length<5*1024*1024,"Preview image must be substantive and under LinkedIn 5 MB limit");
assert.equal(socialBytes.subarray(0,8).toString("hex"),"89504e470d0a1a0a","Expected real PNG signature");
assert.equal(socialBytes.readUInt32BE(16),1200,"OG width must be 1200");
assert.equal(socialBytes.readUInt32BE(20),630,"OG height must be 630");
assert.equal(socialResponse.headers.get("content-length"),String(socialBytes.length));
assert.ok(!socialResponse.headers.has("set-cookie"),"OG image must not set tracking cookies");
const imageHead=await worker.fetch(new Request(url+"/og/omnimaster-study-room.png",{method:"HEAD"}));
assert.equal(imageHead.status,200);
assert.equal((await imageHead.arrayBuffer()).byteLength,0);
const robots=await check("/robots.txt",200,/text\/plain/);
assert.match(await robots.text(),/User-agent: \*/);
for(const [path,title] of [
 ["/OMNIMASTER_FULLSTACK_PLAYBOOK.md","Frontend vs Backend | OmniMaster Textbook"],
 ["/OMNIMASTER_RELIABILITY_FIELD_GUIDE.md","Reliability Engineering | OmniMaster"],
 ["/academy/01_START_HERE.md","Academy"]
]) {
 const response=await check(path,200,/text\/html/);
 const body=await response.text();
 if(path.startsWith("/academy")) {
   assert.ok(body.includes('property="og:title"'));
   assert.ok(body.includes('property="og:url" content="'+socialOrigin+path+'"'));
 } else validateSocialMeta(body,path,title);
}

const lessonPaths=[
 "/academy/01_START_HERE.md",
 "/academy/02_SQL_AND_MODELLING.md",
 "/academy/03_PIPELINES_AND_CDC.md",
 "/academy/04_BUILD_APPLICATIONS.md",
 "/academy/05_APPLIED_AI.md",
 "/academy/06_SECURITY_AND_DELIVERY.md",
 "/academy/07_CAPSTONES.md",
 "/human-interface/01_MY_UX_JOURNEY.md",
 "/human-interface/06_UX_WORKBOOK.md",
 "/build-with-me/01_SOURCE_AND_CONTRACT.md",
 "/OMNIMASTER_ACADEMY.md",
 "/OMNIMASTER_HUMAN_INTERFACE.md",
 "/THIRTY_DAY_ENGINEERING_EXPEDITION.md",
 "/projects/README.md",
 "/OMNIMASTER_FULLSTACK_PLAYBOOK.md",
 "/OMNIMASTER_HANDBOOK.md",
 "/OMNIMASTER_RELIABILITY_FIELD_GUIDE.md",
 "/reliability/01_JOBS_AND_STATE.md",
 "/reliability/02_RETRIES_AND_IDEMPOTENCY.md",
 "/reliability/04_STATUS_UX_AND_OPERATIONS.md"
];
for(const path of lessonPaths){
 const response=await check(path,200,/text\/html/);
 const text=await response.text();
 assert.ok(text.includes("OMNIMASTER"),path);
 assert.ok(!text.includes('href="https://github.com/'),"Article unexpectedly links visitors to source: "+path);
 assert.ok(text.includes("All lessons"),path);
 assert.ok(text.includes('class="reader-toc"')||text.includes('class="reader-meta"'),"Reader navigation missing: "+path);
 assert.ok(text.includes('id="mark-read"'),"Reader progress button missing: "+path);
 assert.ok(text.includes("omnimaster.reader.completed.v1"),"Browser-local reading progress missing: "+path);
}
const chapter=await check("/reliability/02_RETRIES_AND_IDEMPOTENCY.md",200,/text\/html/);
const chapterHtml=await chapter.text();
assert.ok(chapterHtml.includes('aria-label="Previous and next lessons"'),"Prev/next lesson navigation missing");
assert.ok(chapterHtml.includes('href="/reliability/01_JOBS_AND_STATE.md"'));
assert.ok(chapterHtml.includes('href="/reliability/03_DEAD_LETTERS_AND_RECONCILIATION.md"'));
const book=(await worker.fetch(new Request(url+"/OMNIMASTER_FULLSTACK_PLAYBOOK.md"))).text();
assert.match(await book,/id="2-frontend-what-people-experience"/);
const pdf=await check("/downloads/omnimaster-fullstack.pdf",200,/application\/pdf/);
assert.match(pdf.headers.get("content-disposition"),/attachment/);
const bytes=new Uint8Array(await pdf.arrayBuffer());
assert.ok(bytes.byteLength>10000,"PDF should contain actual book content");
assert.equal(new TextDecoder().decode(bytes.slice(0,8)),"%PDF-1.4");
assert.ok(new TextDecoder().decode(bytes).includes("%%EOF"));
await check("/definitely-not-a-lesson",404,/text\/plain/);
const disallowed=await worker.fetch(new Request(url+"/",{method:"POST"}));
assert.equal(disallowed.status,405);
const head=await worker.fetch(new Request(url+"/downloads/omnimaster-fullstack.pdf",{method:"HEAD"}));
assert.equal(head.status,200);assert.equal((await head.arrayBuffer()).byteLength,0);
console.log("Reader integration OK: "+assertions+" routes, 54-page catalogue, social sharing PNG (1200x630), per-page OG cards, chapter navigation, local progress and PDF.");
