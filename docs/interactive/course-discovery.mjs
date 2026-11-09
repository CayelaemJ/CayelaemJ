/* Self-contained public course discovery and reading tools. No external APIs. */
const CATALOGUE_CSS="\n.catalogue-intro{padding:10px 0 19px}.catalogue-lead{color:var(--muted);max-width:70ch;font-size:1.08rem}\n.catalogue-controls{display:grid;grid-template-columns:minmax(0,2fr) minmax(180px,1fr);gap:14px;align-items:end;margin:25px 0}\n.catalogue-controls label{display:block;font-size:.88rem;font-weight:750;color:var(--gold);margin-bottom:8px}\n.catalogue-controls input,.catalogue-controls select{font:inherit;min-height:48px;width:100%;background:#173446;color:var(--ink);border:1px solid #608275;border-radius:10px;padding:10px}\n.catalogue-controls :is(input,select):focus-visible,.reading-tools button:focus-visible{outline:3px solid var(--gold);outline-offset:3px}\n.catalogue-count{color:var(--muted);font-size:.95rem;padding:6px 0 20px}\n.catalogue-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,255px),1fr));gap:15px}\n.catalogue-card{min-height:173px;background:linear-gradient(155deg,#183947,#122737);border:1px solid var(--line);border-radius:15px;padding:19px;display:flex;flex-direction:column;justify-content:space-between}\n.catalogue-card:hover{border-color:var(--mint)}\n.catalogue-card .cat{color:var(--gold);font-size:.75rem;font-weight:850;letter-spacing:.07em;text-transform:uppercase}\n.catalogue-card h2{font-size:1.12rem;line-height:1.33;margin:10px 0 6px}\n.catalogue-card p{font-size:.86rem;color:var(--muted);margin:6px 0}\n.catalogue-card .view{font-weight:750}\n.catalogue-card[hidden]{display:none}\n.catalogue-note{background:#183643;border-left:3px solid var(--gold);padding:15px;margin:22px 0;color:var(--muted)}\n.reader-meta{color:var(--muted);font-size:.87rem;margin:10px 0}\n.reader-toc{margin:20px 0;background:#142f41;border:1px solid var(--line);padding:14px 20px;border-radius:12px}\n.reader-toc summary{cursor:pointer;font-weight:800;color:var(--gold)}\n.reader-toc ol{columns:2;padding-left:22px;column-gap:25px}\n.reader-toc li{break-inside:avoid;font-size:.88rem;margin:7px 0}\n.reader-navigation{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px;padding:20px 0}\n.reader-navigation a{background:#19394a;border:1px solid var(--line);border-radius:10px;padding:12px;text-decoration:none}\n.reader-navigation .reader-navlabel{display:block;color:var(--gold);font-size:.76rem;letter-spacing:.06em;font-weight:900}\n.reading-tools{display:flex;align-items:center;flex-wrap:wrap;gap:12px;margin:14px 0}\n.reading-tools button{padding:8px 15px;background:var(--panel);color:var(--mint);border:1px solid var(--mint);font:inherit;font-weight:750;border-radius:8px;cursor:pointer}\n#read-state{color:var(--muted);font-size:.85rem}\n@media(max-width:700px){.catalogue-controls{grid-template-columns:1fr}.reader-toc ol{columns:1}.reader-navigation{grid-template-columns:1fr}}\n@media print{header,.reader-toc,.reading-tools,.reader-navigation,.actions,footer{display:none!important}body{background:white!important;color:black!important}main{max-width:none;margin:0}a{color:#153e64!important}}\n";
const READING_KEY="omnimaster.reader.completed.v1";
function lessonRoute(path){return path.startsWith("docs/")?"/"+path.slice(5):"/"+path}
function lessonCategory(path){
 if(path.startsWith("docs/academy/"))return "Academy";
 if(path.startsWith("docs/human-interface/"))return "UI/UX";
 if(path.startsWith("docs/reliability/"))return "Reliability";
 if(path.startsWith("docs/build-with-me/"))return "Build with me";
 if(path.startsWith("docs/handbook/"))return "Career & systems";
 if(path.startsWith("docs/field-guide/"))return "Architecture";
 if(path.startsWith("docs/personal/"))return "The person";
 if(path.startsWith("projects/"))return "Projects";
 if(path.includes("THIRTY_DAY"))return "Study plans";
 return "Books & guides";
}
function lessonTitle(path){
 const md=PAGES[path]||"";
 const match=md.match(/^#\s+(.+)$/m);
 return (match?match[1]:path.split("/").pop().replace(/\.md$/i,"").replace(/_/g," ")).replace(/\*/g,"").trim();
}
function lessonMinutes(path){
 const words=((PAGES[path]||"").match(/\S+/g)||[]).length;
 return Math.max(1,Math.ceil(words/220));
}
function lessonOrder(a,b){
 const rank={"Books & guides":0,"Academy":1,"Build with me":2,"UI/UX":3,"Reliability":4,"Architecture":5,"Career & systems":6,"The person":7,"Projects":8,"Study plans":9};
 return rank[lessonCategory(a)]-rank[lessonCategory(b)]||a.localeCompare(b);
}
const LESSON_PATHS=Object.keys(PAGES).sort(lessonOrder);
function catalogPage(){
 const options=["All subjects",...new Set(LESSON_PATHS.map(lessonCategory))];
 const cards=LESSON_PATHS.map(path=>{
   const title=lessonTitle(path),cat=lessonCategory(path),mins=lessonMinutes(path);
   const search=[title,cat,path,(PAGES[path]||"").slice(0,900)].join(" ").replace(/[\*\#\[\]()]/g," ").toLowerCase();
   return '<article class="catalogue-card" data-category="'+esc(cat)+'" data-search="'+esc(search)+'">'+
     '<div><div class="cat">'+esc(cat)+'</div><h2><a href="'+esc(lessonRoute(path))+'">'+esc(title)+'</a></h2></div>'+
     '<p>'+mins+' min estimated reading time</p><a class="view" href="'+esc(lessonRoute(path))+'">Open lesson</a></article>';
 }).join("");
 const form='<div class="catalogue-controls">'+
  '<div><label for="lesson-search">Search subjects, topics or chapters</label>'+
  '<input id="lesson-search" type="search" autocomplete="off" placeholder="Try: frontend, SQL, accessibility, reliability"></div>'+
  '<div><label for="lesson-filter">Subject</label><select id="lesson-filter">'+
  options.map((cat,i)=>'<option value="'+esc(i===0?"":cat)+'">'+esc(cat)+'</option>').join("")+'</select></div></div>';
 const js='(function(){const search=document.getElementById("lesson-search"),filter=document.getElementById("lesson-filter"),list=Array.from(document.querySelectorAll(".catalogue-card")),count=document.getElementById("catalogue-count");function render(){const q=search.value.toLowerCase().trim();const cat=filter.value;let shown=0;for(const item of list){const show=(!cat||item.dataset.category===cat)&&(!q||item.dataset.search.includes(q));item.hidden=!show;if(show)shown++;}count.textContent=shown+" of "+list.length+" lessons shown";}search.addEventListener("input",render);filter.addEventListener("change",render);render();})();';
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+
 '<title>All lessons | OmniMaster Study Room</title><meta name="description" content="Browse a searchable collection of publicly accessible engineering lessons. No GitHub login required."><style>'+CSS+CATALOGUE_CSS+'</style></head>'+
 '<body><header><div><a class="brand" href="/">OMNIMASTER · STUDY ROOM</a><nav aria-label="Main"><a href="/">Study Room home</a><a href="/OMNIMASTER_FULLSTACK_PLAYBOOK.md">Frontend vs backend</a></nav></div></header>'+
 '<main id="content"><div class="catalogue-intro"><p>THE OPEN ENGINEERING LIBRARY</p><h1>Explore all '+LESSON_PATHS.length+' lessons.</h1>'+
 '<p class="catalogue-lead">A fieldbook of data engineering, full-stack software, AI, UI/UX, reliability and the decisions behind them. Learn here, without browsing source repositories.</p></div>'+
 form+'<p id="catalogue-count" role="status" aria-live="polite" class="catalogue-count"></p><div class="catalogue-grid" id="catalogue-grid">'+cards+'</div>'+
 '<p class="catalogue-note">Search runs locally in your browser. No tracking, login or server-side search history. Lessons use synthetic examples and explain their limits.</p></main>'+
 '<footer><a href="/">Return to the Study Room</a> · Source and recruiter access are managed separately.</footer><script>'+js+'</script></body></html>';
}
function readingToc(md){
 const sections=md.split("\n").filter(l=>/^##\s+/.test(l)).map(x=>x.replace(/^##\s+/,"").trim());
 if(!sections.length)return "";
 return '<details class="reader-toc" open><summary>On this page ('+sections.length+' sections)</summary><ol>'+
  sections.map(title=>'<li><a href="#'+esc(slug(title))+'">'+esc(title.replace(/\*/g,""))+'</a></li>').join("")+'</ol></details>';
}
function readingNeighbours(path){
 const group=LESSON_PATHS.filter(p=>lessonCategory(p)===lessonCategory(path));
 const pos=group.indexOf(path);if(pos<0||group.length===1)return "";
 const left=pos>0?'<a href="'+esc(lessonRoute(group[pos-1]))+'"><span class="reader-navlabel">PREVIOUS</span>'+esc(lessonTitle(group[pos-1]))+'</a>':"<span></span>";
 const right=pos<group.length-1?'<a href="'+esc(lessonRoute(group[pos+1]))+'"><span class="reader-navlabel">NEXT</span>'+esc(lessonTitle(group[pos+1]))+'</a>':"<span></span>";
 return '<nav class="reader-navigation" aria-label="Previous and next lessons">'+left+right+'</nav>';
}
function readToolScript(){
 return '<script>(function(){const key='+JSON.stringify(READING_KEY)+',path=location.pathname,button=document.getElementById("mark-read"),status=document.getElementById("read-state");if(!button)return;function load(){try{const found=JSON.parse(localStorage.getItem(key)||"[]");return Array.isArray(found)?found.filter(x=>typeof x==="string"):[]}catch{return []}}function render(){const read=load().includes(path);button.textContent=read?"Mark as unread":"Mark as read";button.setAttribute("aria-pressed",String(read));status.textContent=read?"Saved on this device only":"Optional progress stays in this browser";}button.addEventListener("click",function(){const done=load();const next=done.includes(path)?done.filter(x=>x!==path):[...done,path];try{localStorage.setItem(key,JSON.stringify(next))}catch{status.textContent="Progress storage is unavailable in this browser";return;}render()});render();})();</script>';
}
function readingTools(){
 return '<div class="reading-tools"><button type="button" id="mark-read" aria-pressed="false">Mark as read</button><span id="read-state" role="status" aria-live="polite">Optional browser-local progress</span></div>';
}
