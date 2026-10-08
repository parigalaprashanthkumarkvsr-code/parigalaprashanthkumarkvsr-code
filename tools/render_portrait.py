from urllib.request import Request,urlopen
from PIL import Image,ImageOps
from io import BytesIO
import numpy as np

USER="parigalaprashanthkumarkvsr-code"
src=urlopen(Request(f"https://github.com/{USER}.png?size=512",headers={"User-Agent":"Mozilla/5.0"}),timeout=30).read()
img=Image.open(BytesIO(src)).convert("L")
side=min(img.size); left=(img.width-side)//2; top=(img.height-side)//2
img=img.crop((left,top,left+side,top+side))
W,H=64,42
img=ImageOps.autocontrast(img.resize((W,H)))
a=np.array(img)
glyphs=" '.,:;~+*xXO#"
lines=[]
for row in a:
    lines.append("".join(glyphs[min(len(glyphs)-1,int((255-v)/256*len(glyphs)))] for v in row))
rows=[]
for i,line in enumerate(lines):
    safe=line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    rows.append(f'<text x="28" y="{70+i*11}" fill="#58a6ff" font-size="10" xml:space="preserve" clip-path="url(#c{i})">{safe}</text>')
clips=[f'<clipPath id="c{i}"><rect x="20" y="{58+i*11}" width="0" height="12"><animate attributeName="width" from="0" to="580" begin="{i*.04:.2f}s" dur=".45s" fill="freeze"/></rect></clipPath>' for i in range(H)]
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="620" height="620" viewBox="0 0 620 620"><rect width="620" height="620" rx="18" fill="#0d1117"/><text x="24" y="34" fill="#58a6ff" font-family="monospace" font-size="15">$ render_identity --avatar-to-ascii</text><defs>{''.join(clips)}</defs><g font-family="monospace">{''.join(rows)}</g><text x="24" y="570" fill="#8b949e" font-family="monospace" font-size="11">source: GitHub avatar • self-drawing ASCII portrait</text></svg>'''
open("assets/portrait.svg","w",encoding="utf-8").write(svg)
print("portrait.svg generated")