/* OmniMaster public course reader Worker. Build embeds approved lesson text. */
const HOME=__HOME__;
const PAGES=__PAGES__;
/*__COURSE_DISCOVERY__*/
/*__SOCIAL_META__*/
const CSS=":root{color-scheme:dark;--bg:#091724;--ink:#eff8f8;--muted:#b9cfd7;--panel:#173547;--line:#33566c;--mint:#85eeda;--gold:#f2cd87}*{box-sizing:border-box}body{margin:0;background:linear-gradient(120deg,#163a49,var(--bg) 55%);color:var(--ink);font:16px/1.7 system-ui,-apple-system,sans-serif}a{color:var(--mint);text-underline-offset:.2em}a:focus-visible{outline:3px solid var(--gold);outline-offset:4px}header{background:#102838;border-bottom:1px solid var(--line);padding:16px 5vw}header>div{max-width:920px;display:flex;gap:17px;justify-content:space-between;flex-wrap:wrap;margin:auto}.brand{font-weight:900;color:var(--gold);text-decoration:none}nav{display:flex;gap:16px;flex-wrap:wrap}main{max-width:920px;margin:35px auto 70px;padding:0 22px}h1,h2,h3{line-height:1.2;scroll-margin-top:25px}h1{font-size:clamp(2rem,5vw,3.1rem)}h2{margin-top:35px}h3{margin-top:24px}p,li{max-width:80ch}table{display:block;overflow-x:auto;border-collapse:collapse;margin:22px 0}td,th{border:1px solid var(--line);padding:10px;text-align:left;vertical-align:top}th{background:#23475b}td{background:#132d40}pre{overflow:auto;padding:16px;border:1px solid var(--line);background:#102738;border-radius:9px}code{background:#1b4052;padding:1px 5px}pre code{background:none}blockquote{margin:22px 0;padding:10px 16px;border-left:4px solid var(--gold);background:#182f40}footer{max-width:920px;margin:auto;border-top:1px solid var(--line);padding:25px;color:var(--muted)}.action{display:inline-block;padding:9px 15px;border:1px solid var(--mint);border-radius:30px;margin:6px 10px 6px 0;text-decoration:none}details{border:1px solid var(--line);background:#152e40;border-radius:8px;padding:10px;margin:8px 0}summary{cursor:pointer}hr{border:0;border-top:1px solid var(--line);margin:34px 0}";
const TICK=String.fromCharCode(96);
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;")}
function slug(s){return s.toLowerCase().replace(/[^a-z0-9 -]/g,"").trim().replace(/\s+/g,"-")}
function link(raw,source){
 if(raw.startsWith("#"))return raw;
 if(!raw||raw.includes("://")||raw.startsWith("mailto:"))return null;
 try{let u=new URL(raw,"https://learn.invalid/"+source);let p=u.pathname.slice(1);if(!Object.prototype.hasOwnProperty.call(PAGES,p))return null;return (p.startsWith("docs/")?"/"+p.slice(5):"/"+p)+u.hash}catch{return null}
}
function inline(s,source){
 const slots=[];
 let result=String(s).replace(/\[([^\]]+)\]\(([^)]+)\)/g,function(_,title,url){let dest=link(url,source);slots.push(dest?'<a href="'+esc(dest)+'">'+esc(title)+'</a>':esc(title));return "SLOT"+(slots.length-1)+"END"});
 result=esc(result).replace(new RegExp(TICK+"([^"+TICK+"]+)"+TICK,"g"),"<code>$1</code>").replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>").replace(/\*([^*]+)\*/g,"<em>$1</em>");
 return result.replace(/SLOT(\d+)END/g,function(_,n){return slots[Number(n)]})
}
function markdown(md,path){
 const ls=md.split("\n");let out="",para=[],list="",table=false,code=false,codeLines=[];
 const flush=()=>{if(para.length){out+="<p>"+inline(para.join(" "),path)+"</p>";para=[]}if(list){out+="</"+list+">";list=""}if(table){out+="</table>";table=false}};
 for(let i=0;i<ls.length;i++){
  let t=ls[i].trim();
  if(t.startsWith("~~~")||t.startsWith(TICK.repeat(3))){flush();if(code){out+="<pre><code>"+esc(codeLines.join("\n"))+"</code></pre>";codeLines=[];code=false}else code=true;continue}
  if(code){codeLines.push(ls[i]);continue}
  if(!t){flush();continue}
  let head=t.match(/^(#{1,6})\s+(.+)/);
  if(head){flush();let n=head[1].length;out+="<h"+n+' id="'+esc(slug(head[2]))+'">'+inline(head[2],path)+"</h"+n+">";continue}
  if(t==="---"){flush();out+="<hr>";continue}
  if(t.startsWith("|")&&t.endsWith("|")){
   if(!table){flush();table=true;out+="<table>"}
   let cells=t.slice(1,-1).split("|").map(x=>x.trim());if(cells.every(x=>/^:?-{3,}:?$/.test(x)))continue;
   let tag=i+1<ls.length&&/^\s*\|[\s:|-]+\|\s*$/.test(ls[i+1])?"th":"td";
   out+="<tr>"+cells.map(c=>"<"+tag+">"+inline(c,path)+"</"+tag+">").join("")+"</tr>";continue
  }
  if(table){out+="</table>";table=false}
  if(t==="<details>"||t==="</details>"){flush();out+=t;continue}
  if(t.startsWith("<summary>")){flush();out+="<summary>"+inline(t.replace(/<\/?summary>/g,""),path)+"</summary>";continue}
  if(t.startsWith(">")){flush();out+="<blockquote>"+inline(t.slice(1).trim(),path)+"</blockquote>";continue}
  let item=t.match(/^([-*]|\d+\.)\s+(.+)/);
  if(item){if(para.length){out+="<p>"+inline(para.join(" "),path)+"</p>";para=[]}let kind=item[1].endsWith(".")?"ol":"ul";if(list!==kind){if(list)out+="</"+list+">";list=kind;out+="<"+list+">"}out+="<li>"+inline(item[2],path)+"</li>";continue}
  if(list){out+="</"+list+">";list=""}
  para.push(t)
 }
 flush();return out
}
function page(path){
 const md=PAGES[path],title=lessonTitle(path),book=path==="docs/OMNIMASTER_FULLSTACK_PLAYBOOK.md";
 const actions='<a class="action" href="/library">Browse all lessons</a>'+(book?'<a class="action" href="/downloads/omnimaster-fullstack.pdf">Download PDF</a>':"");
 const meta='<p class="reader-meta">'+esc(lessonCategory(path))+' · approximately '+lessonMinutes(path)+' minutes to read</p>';
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+' | OmniMaster Study Room</title><style>'+CSS+CATALOGUE_CSS+'</style></head>'+
 '<body><header><div><a class="brand" href="/">OMNIMASTER · LEARNING ROOM</a><nav aria-label="Read"><a href="/">Home</a><a href="/library">All lessons</a><a href="/OMNIMASTER_FULLSTACK_PLAYBOOK.md">Full-stack book</a><a href="/THIRTY_DAY_ENGINEERING_EXPEDITION.md">30-day plan</a></nav></div></header>'+
 '<main><p>Public learning · No repository login required</p>'+actions+meta+readingTools()+readingToc(md)+markdown(md,path)+
 readingNeighbours(path)+'<hr><p>Educational examples are synthetic and explicitly distinguish implementation from production guarantees.</p>'+actions+
 '</main><footer>One mind. Every layer. Public lessons, restricted technical review by separate approval.</footer>'+readToolScript()+'</body></html>'
}
function makePdf(md){
 let lines=["OMNIMASTER FULL-STACK PLAYBOOK","Frontend vs Backend Engineering","Cayelaem Jantjies | Public Study Edition",""];
 for(const raw of md.split("\n")){
  let t=raw.replace(/^\s*#{1,6}\s*/,"").replace(/\*\*|~~/g,"").split(TICK).join("").replace(/\[([^\]]+)\]\([^)]+\)/g,"$1").replace(/[^\x20-\x7e]/g," ").trim();
  if(!t||t.startsWith("~~~")||t.startsWith("<")){lines.push("");continue}
  while(t.length>90){let i=t.lastIndexOf(" ",90);if(i<20)i=90;lines.push(t.slice(0,i));t=t.slice(i).trim()}
  if(t)lines.push(t)
 }
 let chunks=[];for(let i=0;i<lines.length;i+=51)chunks.push(lines.slice(i,i+51));
 let objs=[null,"<< /Type /Catalog /Pages 2 0 R >>",null,"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"],ids=[];
 for(let p=0;p<chunks.length;p++){
  let id=objs.length;ids.push(id);objs.push("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents "+(id+1)+" 0 R >>");
  let content="BT /F1 10 Tf 38 795 Td 14 TL\n";
  for(let x of chunks[p])content+="("+x.replace(/([\\()])/g,"\\$1")+") Tj T*\n";
  content+="ET\nBT /F1 8 Tf 38 31 Td (OmniMaster | Page "+(p+1)+" of "+chunks.length+") Tj ET\n";
  objs.push("<< /Length "+content.length+" >>\nstream\n"+content+"endstream")
 }
 objs[2]="<< /Type /Pages /Count "+chunks.length+" /Kids ["+ids.map(id=>id+" 0 R").join(" ")+"] >>";
 let file="%PDF-1.4\n",offsets=[0];for(let i=1;i<objs.length;i++){offsets[i]=file.length;file+=i+" 0 obj\n"+objs[i]+"\nendobj\n"}
 let index=file.length;file+="xref\n0 "+objs.length+"\n0000000000 65535 f \n";
 for(let i=1;i<objs.length;i++)file+=String(offsets[i]).padStart(10,"0")+" 00000 n \n";
 file+="trailer\n<< /Size "+objs.length+" /Root 1 0 R >>\nstartxref\n"+index+"\n%%EOF";
 return new TextEncoder().encode(file)
}
const PDF=makePdf(PAGES["docs/OMNIMASTER_FULLSTACK_PLAYBOOK.md"]);
const H={"cache-control":"public,max-age=300","x-content-type-options":"nosniff","referrer-policy":"no-referrer","content-security-policy":"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"};
export default {async fetch(request){
 let path=new URL(request.url).pathname;if(request.method!=="GET"&&request.method!=="HEAD")return new Response("Method not allowed",{status:405,headers:{allow:"GET, HEAD"}});
 if(path==="/og/omnimaster-study-room.png")return new Response(request.method==="HEAD"?null:SHARE_PNG,{headers:{"content-type":"image/png","cache-control":"public,max-age=3600","content-length":String(SHARE_PNG.length),"x-content-type-options":"nosniff","referrer-policy":"no-referrer"}});
 if(path==="/robots.txt")return new Response(request.method==="HEAD"?null:"User-agent: *\nAllow: /\n",{headers:{"content-type":"text/plain;charset=utf-8","cache-control":"public,max-age=86400"}});
 if(path==="/"||path==="/index.html")return new Response(request.method==="HEAD"?null:withSocialHead(HOME,"/"),{headers:{...H,"content-type":"text/html;charset=utf-8"}});
 if(path==="/library")return new Response(request.method==="HEAD"?null:withSocialHead(catalogPage(),"/library"),{headers:{...H,"content-type":"text/html;charset=utf-8"}});
 if(path==="/downloads/omnimaster-fullstack.pdf")return new Response(request.method==="HEAD"?null:PDF,{headers:{...H,"content-type":"application/pdf","content-disposition":'attachment; filename="OmniMaster_Fullstack_Playbook.pdf"',"content-length":String(PDF.length)}});
 let key=path.startsWith("/projects/")?path.slice(1):"docs"+path;
 if(Object.prototype.hasOwnProperty.call(PAGES,key))return new Response(request.method==="HEAD"?null:withSocialHead(page(key),path),{headers:{...H,"content-type":"text/html;charset=utf-8"}});
 return new Response(request.method==="HEAD"?null:"Not found",{status:404,headers:{...H,"content-type":"text/plain;charset=utf-8"}});
}};