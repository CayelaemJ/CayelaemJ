/** Build a custom, dependency-free 1200 x 630 PNG social card for the public Study Room.
 * Uses only Node's zlib at build time. The deployed Worker serves the static result.
 * This is intentionally an original pixel-art image, not a client's logo or stock art.
 */
import { deflateSync } from "node:zlib";

const WIDTH = 1200;
const HEIGHT = 630;
const FONT = {
 A:[".###.","#...#","#...#","#####","#...#","#...#","#...#"],
 B:["####.","#...#","#...#","####.","#...#","#...#","####."],
 C:[".####","#....","#....","#....","#....","#....",".####"],
 D:["####.","#...#","#...#","#...#","#...#","#...#","####."],
 E:["#####","#....","#....","####.","#....","#....","#####"],
 F:["#####","#....","#....","####.","#....","#....","#...."],
 G:[".####","#....","#....","#.###","#...#","#...#",".###."],
 H:["#...#","#...#","#...#","#####","#...#","#...#","#...#"],
 I:["#####","..#..","..#..","..#..","..#..","..#..","#####"],
 J:["..###","...#.","...#.","...#.","#..#.","#..#.",".##.."],
 K:["#...#","#..#.","#.#..","##...","#.#..","#..#.","#...#"],
 L:["#....","#....","#....","#....","#....","#....","#####"],
 M:["#...#","##.##","#.#.#","#.#.#","#...#","#...#","#...#"],
 N:["#...#","##..#","#.#.#","#..##","#...#","#...#","#...#"],
 O:[".###.","#...#","#...#","#...#","#...#","#...#",".###."],
 P:["####.","#...#","#...#","####.","#....","#....","#...."],
 Q:[".###.","#...#","#...#","#...#","#.#.#","#..#.",".##.#"],
 R:["####.","#...#","#...#","####.","#.#..","#..#.","#...#"],
 S:[".####","#....","#....",".###.","....#","....#","####."],
 T:["#####","..#..","..#..","..#..","..#..","..#..","..#.."],
 U:["#...#","#...#","#...#","#...#","#...#","#...#",".###."],
 V:["#...#","#...#","#...#","#...#","#...#",".#.#.","..#.."],
 W:["#...#","#...#","#...#","#.#.#","#.#.#","##.##","#...#"],
 X:["#...#","#...#",".#.#.","..#..",".#.#.","#...#","#...#"],
 Y:["#...#","#...#",".#.#.","..#..","..#..","..#..","..#.."],
 Z:["#####","....#","...#.","..#..",".#...","#....","#####"],
 "0":[".###.","#...#","#..##","#.#.#","##..#","#...#",".###."],
 "1":["..#..",".##..","..#..","..#..","..#..","..#..",".###."],
 "2":[".###.","#...#","....#","...#.","..#..",".#...","#####"],
 "3":["####.","....#","....#",".###.","....#","....#","####."],
 "4":["#...#","#...#","#...#","#####","....#","....#","....#"],
 "5":["#####","#....","#....","####.","....#","....#","####."],
 "6":[".###.","#....","#....","####.","#...#","#...#",".###."],
 "7":["#####","....#","...#.","..#..",".#...",".#...",".#..."],
 "8":[".###.","#...#","#...#",".###.","#...#","#...#",".###."],
 "9":[".###.","#...#","#...#",".####","....#","....#",".###."],
 " ":[".....",".....",".....",".....",".....",".....","....."],
 ".":[".....",".....",".....",".....",".....","..##.","..##."],
 ":":[".....","..##.","..##.",".....","..##.","..##.","....."],
 "/":["....#","....#","...#.","..#..",".#...","#....","#...."],
 "-":[".....",".....",".....","#####",".....",".....","....."],
 "&":[".##..","#..#.","#.#..",".#...","#.#.#","#..#.",".##.#"],
 "+":[".....","..#..","..#..","#####","..#..","..#..","....."],
 "|":["..#..","..#..","..#..","..#..","..#..","..#..","..#.."]
};
const PIXELS = Buffer.alloc(WIDTH * HEIGHT * 4);
function pixel(x,y,r,g,b){
 if(x<0||y<0||x>=WIDTH||y>=HEIGHT)return;
 const i=(y*WIDTH+x)*4;
 PIXELS[i]=r; PIXELS[i+1]=g;PIXELS[i+2]=b;PIXELS[i+3]=255;
}
function fill(x,y,w,h,col){
 const left=Math.max(0,Math.floor(x)),top=Math.max(0,Math.floor(y));
 const right=Math.min(WIDTH,Math.ceil(x+w)),bottom=Math.min(HEIGHT,Math.ceil(y+h));
 for(let yy=top;yy<bottom;yy++)for(let xx=left;xx<right;xx++)pixel(xx,yy,...col);
}
function line(x1,y1,x2,y2,col,width=2){
 const steps=Math.ceil(Math.hypot(x2-x1,y2-y1));
 for(let n=0;n<=steps;n++){const t=steps?n/steps:0;const x=x1+(x2-x1)*t,y=y1+(y2-y1)*t;fill(x-width/2,y-width/2,width,width,col)}
}
function text(label,x,y,scale,col,gap=1){
 let cursor=x;
 for(const char of label.toUpperCase()){
  const glyph=FONT[char];
  if(!glyph)throw new Error("Missing glyph "+char);
  for(let row=0;row<7;row++)for(let colx=0;colx<5;colx++)if(glyph[row][colx]==="#"){
    fill(cursor+colx*scale,y+row*scale,scale,scale,col);
  }
  cursor+=(5+gap)*scale;
 }
 return cursor;
}
function labelBox(x,y,w,h,color){
 fill(x,y,w,h,[22,52,62]);fill(x,y,4,h,color);
 line(x,y,x+w,y,[49,94,100],1);line(x+w,y,x+w,y+h,[49,94,100],1);
}
function pngChunk(name,buffer){
 const type=Buffer.from(name,"ascii"),len=Buffer.alloc(4);
 len.writeUInt32BE(buffer.length,0);
 const crcBytes=Buffer.concat([type,buffer]),crcBuf=Buffer.alloc(4);
 let crc=0xffffffff;
 for(const byte of crcBytes){crc^=byte;for(let k=0;k<8;k++)crc=(crc>>>1)^((crc&1)?0xedb88320:0)}
 crcBuf.writeUInt32BE((crc^0xffffffff)>>>0,0);
 return Buffer.concat([len,type,buffer,crcBuf]);
}
export function makeSocialPreviewPng(){
 // Editorial dark navy / deep teal artwork, designed for 1.91:1 link cards.
 for(let y=0;y<HEIGHT;y++)for(let x=0;x<WIDTH;x++){
  const glow=Math.max(0,1-Math.hypot(x-1040,y-85)/800);
  const l=y/HEIGHT;
  pixel(x,y,Math.round(7+15*l+7*glow),Math.round(25+19*l+26*glow),Math.round(36+23*l+24*glow));
 }
 // Subtle construction-grid / constellation visual identity.
 for(let x=56;x<WIDTH;x+=58)line(x,25,x,605,[16,52,63],1);
 for(let y=35;y<HEIGHT;y+=58)line(20,y,1180,y,[16,52,63],1);
 for(let n=0;n<9;n++){
  const x=965+n*24,y=75+n*29;
  line(x,y,x+136,y+60,[36,104,103],2);
  fill(x+132,y+55,10,10,n%3===0?[235,199,133]:[98,215,194]);
 }
 fill(63,57,1057,8,[240,202,143]);fill(63,68,365,3,[107,230,210]);
 text("OMNIMASTER",67,107,9,[235,204,155],1);
 text("STUDY ROOM",66,221,15,[240,248,245],1);
 fill(66,349,963,4,[101,221,196]);
 text("ENGINEERING. EXPLAINED.",67,378,6,[143,232,212],1);
 labelBox(65,481,302,79,[240,202,143]);text("54 LESSONS",86,504,5,[240,242,220]);
 labelBox(385,481,302,79,[101,221,196]);text("7 SCENARIOS",402,504,5,[220,242,237]);
 labelBox(705,481,417,79,[240,202,143]);text("FREE TO LEARN",731,504,5,[240,242,220]);
 text("DATA / FULL STACK / AI / UX",66,594,3,[160,198,198],1);
 // 1200x630 RGBA, no network assets, no external font.
 const scanlineSize=WIDTH*4+1,raw=Buffer.alloc(scanlineSize*HEIGHT);
 for(let y=0;y<HEIGHT;y++){
  const row=y*scanlineSize;raw[row]=0;PIXELS.copy(raw,row+1,y*WIDTH*4,(y+1)*WIDTH*4);
 }
 const header=Buffer.alloc(13);header.writeUInt32BE(WIDTH,0);header.writeUInt32BE(HEIGHT,4);
 header[8]=8;header[9]=6;
 const signature=Buffer.from([137,80,78,71,13,10,26,10]);
 return Buffer.concat([signature,pngChunk("IHDR",header),pngChunk("IDAT",deflateSync(raw,{level:9})),pngChunk("IEND",Buffer.alloc(0))]);
}
