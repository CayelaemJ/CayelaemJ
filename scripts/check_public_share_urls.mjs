/* Public HTTP smoke test for the OmniMaster profile and learning library.
 * Uses only Node.js builtins; no credentials, external npm modules or private API.
 * Intended for CI from an independent runner, not a LinkedIn ingestion guarantee.
 */
import assert from "node:assert/strict";

const SHARE="https://omnimaster-study-room-share.onrender.com";
const PORTFOLIO="https://omnimaster-portfolio.onrender.com";
const CASES=[
  {name:"study home",url:SHARE+"/",kind:"html",canonical:SHARE+"/"},
  {name:"study catalogue",url:SHARE+"/library.html",kind:"html",canonical:SHARE+"/library.html"},
  {name:"full-stack book",url:SHARE+"/OMNIMASTER_FULLSTACK_PLAYBOOK.html",kind:"html",canonical:SHARE+"/OMNIMASTER_FULLSTACK_PLAYBOOK.html"},
  {name:"study social image",url:SHARE+"/og/omnimaster-study-room.png",kind:"png"},
  {name:"study PDF",url:SHARE+"/downloads/omnimaster-fullstack.pdf",kind:"pdf"},
  {name:"portfolio home",url:PORTFOLIO+"/",kind:"html",canonical:PORTFOLIO+"/"},
  {name:"portfolio bookcase",url:PORTFOLIO+"/library",kind:"html",canonical:PORTFOLIO+"/library"},
  {name:"portfolio PDF redirect",url:PORTFOLIO+"/book.pdf",kind:"redirect",location:SHARE+"/downloads/omnimaster-fullstack.pdf"}
];
const NORMAL_UA="OmniMaster-Public-HealthCheck/1.0";
const LINKEDIN_UA="LinkedInBot/1.0 (+http://www.linkedin.com)";
const failures=[];
let checks=0;

async function get(url,userAgent=NORMAL_UA){
  let last;
  for(let attempt=1;attempt<=3;attempt++){
    try {
      const response=await fetch(url,{
        method:"GET",
        redirect:"manual",
        headers:{"User-Agent":userAgent,"Accept":"text/html,image/png,application/pdf,*/*"},
        signal:AbortSignal.timeout(35000),
        cache:"no-store"
      });
      // Render's free services can take time to wake on first request.
      if(response.status===502||response.status===503||response.status===504){
        last=new Error("Temporary "+response.status);
      }else return response;
    }catch(e){last=e}
    if(attempt<3)await new Promise(done=>setTimeout(done,3500));
  }
  throw last||new Error("Connection failed");
}

function og(html,property){
  const m=html.match(new RegExp('<meta\\s+property="'+property+'"\\s+content="([^"]+)"','i'));
  return m?.[1]||null;
}

async function inspect(info,userAgent=NORMAL_UA){
  const response=await get(info.url,userAgent);
  const type=response.headers.get("content-type")||"";
  const label=userAgent===LINKEDIN_UA?"LinkedIn UA":"normal UA";
  checks++;
  if(info.kind==="redirect"){
    assert.equal(response.status,302,info.name+" redirects with status 302");
    assert.equal(response.headers.get("location"),info.location,info.name+" redirect target");
  }else{
    assert.equal(response.status,200,info.name+" HTTP status");
  }
  if(info.kind==="html"){
    assert.match(type,/text\/html/i,info.name+" HTML response");
    const content=await response.text();
    assert.ok(content.length>1000,"HTML is substantial");
    assert.ok(og(content,"og:title"),info.name+" initial HTML must expose OG title");
    assert.ok(og(content,"og:description"),info.name+" initial HTML must expose OG description");
    assert.equal(og(content,"og:url"),info.canonical,info.name+" canonical social URL");
    assert.ok(og(content,"og:image")?.startsWith(SHARE+"/og/"),info.name+" public preview image");
    assert.ok(content.includes('name="twitter:card" content="summary_large_image"'),info.name+" large image Twitter card");
    if(info.name==="study catalogue")assert.equal((content.match(/class="catalogue-card"/g)||[]).length,54);
    if(info.name==="portfolio home")assert.ok(content.includes('id="learning-library"'));
    if(info.name==="portfolio bookcase")assert.ok(content.includes('href="'+SHARE+'/OMNIMASTER_FULLSTACK_PLAYBOOK.html"'));
    if(info.name==="study home")assert.ok(content.includes('data-share-url="'+SHARE+'/"'));
  }else if(info.kind==="png"){
    assert.match(type,/image\/png/i,"Image content-type");
    const b=Buffer.from(await response.arrayBuffer());
    assert.equal(b.subarray(0,8).toString("hex"),"89504e470d0a1a0a");
    assert.equal(b.readUInt32BE(16),1200);assert.equal(b.readUInt32BE(20),630);
  }else if(info.kind==="pdf"){
    assert.match(type,/application\/pdf/i);
    const b=Buffer.from(await response.arrayBuffer());
    assert.equal(b.subarray(0,8).toString("utf8"),"%PDF-1.4");
    assert.ok(b.length>10000);
  }
  console.log("PASS",label,info.name,response.status,type);
}

for(const testcase of CASES){
  try{await inspect(testcase)}catch(e){
    failures.push({name:testcase.name,agent:"normal",error:String(e)});
    console.error("FAIL",testcase.name,String(e));
  }
}
// A spoofed UA doesn't prove what LinkedIn's actual crawler sees. It confirms
// that the public host doesn't universally block that user-agent string.
for(const testcase of [CASES[0],CASES[1],CASES[5]]){
  try{await inspect(testcase,LINKEDIN_UA)}catch(e){
    failures.push({name:testcase.name,agent:"LinkedIn UA",error:String(e)});
    console.error("FAIL LinkedIn UA",testcase.name,String(e));
  }
}
console.log("Checked",checks,"public HTTP response paths with",failures.length,"failures.");
if(failures.length){
  console.error(JSON.stringify(failures,null,2));
  process.exitCode=1;
}
