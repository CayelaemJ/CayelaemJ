/* Build a self-contained Worker from public educational Markdown.
   Run from the repository root: node docs/interactive/build_worker.mjs
   No remote GitHub fetch, secrets, external packages or tracking. */
import {readFileSync,writeFileSync} from "node:fs";
import {fileURLToPath} from "node:url";
import {resolve,dirname} from "node:path";
const root=resolve(dirname(fileURLToPath(import.meta.url)),"../..");
const lessons=[
 "docs/OMNIMASTER_FULLSTACK_PLAYBOOK.md",
 "docs/OMNIMASTER_HANDBOOK.md",
 "docs/OMNIMASTER_FIELD_GUIDE.md",
 "docs/OMNIMASTER_ACADEMY.md",
 "docs/OMNIMASTER_OPERATING_MANUAL.md",
 "docs/OMNIMASTER_BUILD_WITH_ME.md",
 "docs/OMNIMASTER_HUMAN_INTERFACE.md",
 "docs/OMNIMASTER_RELIABILITY_FIELD_GUIDE.md",
 "docs/OMNIMASTER_ARCADE.md",
 "docs/THIRTY_DAY_ENGINEERING_EXPEDITION.md",
 "projects/README.md",
 ...["01_START_HERE","02_SQL_AND_MODELLING","03_PIPELINES_AND_CDC","04_BUILD_APPLICATIONS",
     "05_APPLIED_AI","06_SECURITY_AND_DELIVERY","07_CAPSTONES"].map(x=>"docs/academy/"+x+".md"),
 ...["01_MY_UX_JOURNEY","02_HUMAN_CENTRED_DESIGN","03_UX_CASE_STUDIES",
     "04_DESIGN_SYSTEMS_AND_ACCESSIBILITY","05_MEASURE_USABILITY","06_UX_WORKBOOK"].map(x=>"docs/human-interface/"+x+".md"),
 ...["01_SOURCE_AND_CONTRACT","02_INGESTION_AND_TRANSACTIONS","03_PROJECTIONS_AND_GRAIN",
     "04_FROM_METRICS_TO_USERS","05_FAILURE_LAB","06_BEYOND_THE_DEMO"].map(x=>"docs/build-with-me/"+x+".md"),
 ...["01_THE_ENGINEER","02_THE_CAREER","03_SYSTEMS_IN_THE_WILD","04_DATA_ENGINEERING",
     "05_ANALYTICS_ENGINEERING","06_PRODUCTS_AND_AI","07_SECURITY_AND_DELIVERY",
     "08_REPRODUCE_THE_WORK","09_LEADERSHIP_AND_NEXT","10_GLOSSARY_AND_EVIDENCE"].map(x=>"docs/handbook/"+x+".md"),
 ...["01_ARCHITECTURE_ATLAS","02_DEBUGGING_CASEBOOK","03_ENGINEERING_WORKBOOK",
     "04_ROLE_AND_EVIDENCE_MAP","05_DECISION_JOURNAL"].map(x=>"docs/field-guide/"+x+".md"),
 ...["01_INTJ_AND_ME","02_WHY_I_THINK_IN_SYSTEMS","03_IT_RANGE_AND_LIMITS",
     "04_COLLABORATION_AND_QUIRKS"].map(x=>"docs/personal/"+x+".md"),
 ...["01_JOBS_AND_STATE","02_RETRIES_AND_IDEMPOTENCY",
     "03_DEAD_LETTERS_AND_RECONCILIATION","04_STATUS_UX_AND_OPERATIONS",
     "05_PRODUCTION_BOUNDARIES"].map(x=>"docs/reliability/"+x+".md")
];
const content=Object.fromEntries(lessons.map(path=>[path,readFileSync(resolve(root,path),"utf8")]));
const home=readFileSync(resolve(root,"docs/interactive/index.html"),"utf8");
const template=readFileSync(resolve(root,"docs/interactive/library-worker-template.mjs"),"utf8");
const built=template.replace("__HOME__",JSON.stringify(home)).replace("__PAGES__",JSON.stringify(content));
if(built.includes("__HOME__")||built.includes("__PAGES__"))throw new Error("Unreplaced template marker");
const output=resolve(root,"docs/interactive/.generated-study-room-worker.mjs");
writeFileSync(output,built,"utf8");
console.log("Built "+Object.keys(content).length+" on-site lesson pages; Worker "+Buffer.byteLength(built)+" bytes.");
