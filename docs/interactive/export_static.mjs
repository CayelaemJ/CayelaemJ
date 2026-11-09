/**
 * Export the public, tested OmniMaster Worker into a complete static website.
 *
 * Purpose: use an independent public HTTPS hostname for social crawlers that
 * may be challenged by the mandatory browser-integrity checks on workers.dev.
 *
 * Usage:
 *   OMNIMASTER_PUBLIC_ORIGIN=https://your-static-host.example \
 *     node docs/interactive/export_static.mjs
 *
 * No user data, API credentials, dependencies, or external network calls.
 * The original Worker stays online as an independent fallback.
 */
import {execFileSync} from "node:child_process";
import {readFileSync,writeFileSync,mkdirSync,rmSync,existsSync} from "node:fs";
import {resolve,dirname,join} from "node:path";
import {fileURLToPath} from "node:url";

const root=resolve(dirname(fileURLToPath(import.meta.url)),"../..");
const directory=resolve(root,"docs/interactive/.static-publish");
const WORKER_HOST="https://omnimaster-study-room.cabo-solutions-za.workers.dev";
const publicOrigin=(process.env.OMNIMASTER_PUBLIC_ORIGIN||"https://omnimaster-study-room-share.onrender.com").replace(/\/+$/,"");
const checkHost=new URL(publicOrigin);
if(checkHost.protocol!=="https:"||checkHost.pathname!=="/"||checkHost.search||checkHost.hash)
  throw new Error("OMNIMASTER_PUBLIC_ORIGIN must be a public HTTPS origin, without path or query");
if(checkHost.hostname.endsWith(".workers.dev"))
  throw new Error("Crawler-compatible mirror must not use the workers.dev hostname");

execFileSync(process.execPath,["docs/interactive/build_worker.mjs"],{cwd:root,stdio:"inherit"});
const bundle=readFileSync(resolve(root,"docs/interactive/.generated-study-room-worker.mjs"),"utf8");
const {default:worker}=await import("data:text/javascript;base64,"+Buffer.from(bundle).toString("base64"));

function staticPath(route){
  if(route==="/")return "/index.html";
  if(route==="/library")return "/library.html";
  if(route.endsWith(".md"))return route.slice(0,-3)+".html";
  return route;
}
function editHtml(source,route){
  const published=staticPath(route);
  let html=source.replaceAll(WORKER_HOST,publicOrigin);
  // On the CDN a Markdown lesson is an actual .html file. Repoint every
  // hyperlink, preserving relative paths and in-page anchors.
  html=html.replace(/(\bhref=")([^"]+?\.md)(#[^"]*)?(")/g,
                    (_,prefix,path,anchor="",end)=>prefix+path.slice(0,-3)+".html"+anchor+end);
  html=html.replaceAll('href="/library"','href="/library.html"');
  // The original homepage share action holds a literal workers.dev URL;
  // global hostname replacement above makes the shared URL match the mirror.
  // Social crawlers must see a self-consistent canonical URL in raw HTML.
  const canonical=publicOrigin+published;
  html=html.replace(/(<meta property="og:url" content=")[^"]+(")/,
                    (_,start,end)=>start+canonical+end);
  html=html.replace(/(<link rel="canonical" href=")[^"]+(")/,
                    (_,start,end)=>start+canonical+end);
  if(!html.includes('property="og:image" content="'+publicOrigin+'/og/omnimaster-study-room.png"'))
    throw new Error("Social preview image does not point to public static host: "+route);
  if(html.includes(WORKER_HOST))throw new Error("Worker URL remains in static page "+route);
  return html;
}
async function output(route){
  const result=await worker.fetch(new Request(WORKER_HOST+route));
  if(result.status!==200)throw new Error("Cannot export "+route+": status "+result.status);
  const name=staticPath(route),path=resolve(directory,"."+name);
  if(!path.startsWith(directory+"/"))throw new Error("Unsafe export path "+name);
  mkdirSync(dirname(path),{recursive:true});
  const type=result.headers.get("content-type")||"";
  let data;
  if(type.includes("text/html")){
    data=Buffer.from(editHtml(await result.text(),route),"utf8");
  } else {
    data=Buffer.from(await result.arrayBuffer());
  }
  if(!data.length)throw new Error("Empty export "+route);
  writeFileSync(path,data);
  return {route,path,name,size:data.length};
}

rmSync(directory,{recursive:true,force:true});
const catalogue=await worker.fetch(new Request(WORKER_HOST+"/library"));
if(catalogue.status!==200)throw new Error("Catalogue cannot be read");
const catalogueHtml=await catalogue.text();
const lessons=[...new Set([...catalogueHtml.matchAll(/href="(\/[^"#?]+\.md)"/g)].map(x=>x[1]))];
if(lessons.length!==54)throw new Error("Expected 54 bundled courses; found "+lessons.length);

const routes=[
 "/", "/library", ...lessons,
 "/downloads/omnimaster-fullstack.pdf",
 "/og/omnimaster-study-room.png",
 "/robots.txt"
];
const results=[];
for(const route of routes)results.push(await output(route));

const sitemap='<?xml version="1.0" encoding="UTF-8"?>\n'+
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+
  routes.filter(x=>x==="/"||x==="/library"||x.endsWith(".md"))
    .map(x=>'  <url><loc>'+publicOrigin+staticPath(x)+'</loc></url>').join("\n")+
  '\n</urlset>\n';
writeFileSync(join(directory,"sitemap.xml"),sitemap);

const manifest={
  source:"CayelaemJ/CayelaemJ",
  publicOrigin,
  routes:routes.length,
  lessons:lessons.length,
  generated:new Date().toISOString(),
  files:results.map(({route,name,size})=>({route,name,size}))
};
writeFileSync(join(directory,"manifest.json"),JSON.stringify(manifest,null,2));

console.log("Exported "+results.length+" pages/assets including "+lessons.length+
  " lessons to "+directory+" for "+publicOrigin);
