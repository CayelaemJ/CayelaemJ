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
}
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
console.log("Reader integration OK: "+assertions+" valid HTTP routes, live book chapters, repository-free navigation, downloadable PDF.");
