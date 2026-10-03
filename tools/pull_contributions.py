from urllib.request import Request, urlopen
from datetime import datetime
import json,re

USER="parigalaprashanthkumvsr-code"
URL=f"https://github.com/users/{USER}/contributions"
req=Request(URL,headers={"User-Agent":"Mozilla/5.0"})
html=urlopen(req,timeout=30).read().decode("utf-8","ignore")
cells=re.findall(r'<td[^>]*class="[^"]*ContributionCalendar-day[^"]*"[^>]*>',html)
data=[]
for c in cells:
    d=re.search(r'data-date="([^"]+)"',c)
    n=re.search(r'data-count="([^"]+)"',c)
    l=re.search(r'data-level="([^"]+)"',c)
    if d:
        data.append({"date":d.group(1),"count":int(n.group(1)) if n else 0,"level":int(l.group(1)) if l else 0})
if not data:
    raise RuntimeError("No contribution cells found; GitHub markup may have changed.")
total=sum(x["count"] for x in data)
with open("assets/contributions.json","w",encoding="utf-8") as f:
    json.dump({"generated_at":datetime.utcnow().isoformat()+"Z","user":USER,"total":total,"days":data},f,indent=2)
print(f"saved {len(data)} days, {total} contributions")