/* Social sharing metadata for the public OmniMaster Study Room.
 * Metadata is returned in the initial HTML, so LinkedIn/WhatsApp/X crawlers
 * don't need to execute JavaScript. The image is hosted on this Worker.
 */
const SHARE_ORIGIN="https://omnimaster-study-room.cabo-solutions-za.workers.dev";
const SHARE_IMAGE_PATH="/og/omnimaster-study-room.png";
const SHARE_PNG=Uint8Array.from(atob(__SOCIAL_IMAGE_BASE64__),c=>c.charCodeAt(0));
const SHARE_TITLES={
 "/":"OmniMaster Study Room | Learn Engineering",
 "/library":"54 Free Engineering Lessons | OmniMaster",
 "/OMNIMASTER_FULLSTACK_PLAYBOOK.md":"Frontend vs Backend | OmniMaster Textbook",
 "/OMNIMASTER_RELIABILITY_FIELD_GUIDE.md":"Reliability Engineering | OmniMaster"
};
const SHARE_DESCRIPTIONS={
 "/":"Explore 54 engineering lessons, interactive challenges, a 30-day study plan and a free full-stack textbook.",
 "/library":"Search 54 practical lessons covering data, software engineering, AI, UI/UX, security and reliability.",
 "/OMNIMASTER_FULLSTACK_PLAYBOOK.md":"Understand frontend, backend and full-stack engineering through examples, diagrams and hands-on exercises.",
 "/OMNIMASTER_RELIABILITY_FIELD_GUIDE.md":"Learn retries, idempotency, dead letters and honest user-facing status through a runnable Python lab."
};
function shareEscape(value){return String(value).replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}
function socialPageDescription(path){
 return SHARE_DESCRIPTIONS[path]||
  "Study "+lessonCategory(path.startsWith("/projects/")?path.slice(1):"docs"+path)+
  " through practical explanations, reproducible examples and exercises on OmniMaster.";
}
function socialPageTitle(path){
 return SHARE_TITLES[path]||
  (Object.prototype.hasOwnProperty.call(PAGES,path.startsWith("/projects/")?path.slice(1):"docs"+path)
   ?lessonTitle(path.startsWith("/projects/")?path.slice(1):"docs"+path)+" | OmniMaster"
   :"OmniMaster Study Room");
}
function socialHead(path){
 const canonical=SHARE_ORIGIN+path,title=socialPageTitle(path),desc=socialPageDescription(path),image=SHARE_ORIGIN+SHARE_IMAGE_PATH;
 const tags=[
  ["meta",'property="og:type" content="website"'],
  ["meta",'property="og:site_name" content="OmniMaster Study Room"'],
  ["meta",'property="og:title" content="'+shareEscape(title)+'"'],
  ["meta",'property="og:description" content="'+shareEscape(desc)+'"'],
  ["meta",'property="og:url" content="'+shareEscape(canonical)+'"'],
  ["meta",'property="og:image" content="'+image+'"'],
  ["meta",'property="og:image:secure_url" content="'+image+'"'],
  ["meta",'property="og:image:type" content="image/png"'],
  ["meta",'property="og:image:width" content="1200"'],
  ["meta",'property="og:image:height" content="630"'],
  ["meta",'property="og:image:alt" content="OmniMaster Study Room: engineering explained; 54 lessons, seven scenarios, free to learn"'],
  ["meta",'name="twitter:card" content="summary_large_image"'],
  ["meta",'name="twitter:title" content="'+shareEscape(title)+'"'],
  ["meta",'name="twitter:description" content="'+shareEscape(desc)+'"'],
  ["meta",'name="twitter:image" content="'+image+'"']
 ];
 return '\n<link rel="canonical" href="'+shareEscape(canonical)+'">\n'+tags.map(([tag,attrs])=>"<"+tag+" "+attrs+">").join("\n")+"\n";
}
function withSocialHead(html,path){
 if(!html.includes("</head>"))throw new Error("HTML missing head");
 return html.replace("</head>",socialHead(path)+"</head>");
}
