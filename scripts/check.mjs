import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const readme = readFileSync(resolve(root, 'README.md'),'utf8');
const names = [...readme.matchAll(/src="(\.\/assets\/svg\/[^\"]+\.svg)"/g)].map(m=>m[1]);
let valid=true;
for(const name of names){
  const abs=resolve(root,name);
  if(!existsSync(abs) || !readFileSync(abs,'utf8').includes('<svg')){
    console.error('Missing or invalid SVG:',name); valid=false;
  }
}
console.log(`README references checked: ${names.length}`);
if(!valid)process.exit(1);
