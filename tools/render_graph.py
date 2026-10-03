import json,html
from datetime import datetime

D=json.load(open("assets/contributions.json",encoding="utf-8"))
days=D["days"]
by_date={x["date"]:x for x in days}
dates=sorted(by_date)
# Align to Sunday and render the latest ~53 weeks.
last=datetime.strptime(dates[-1],"%Y-%m-%d").date()
start=last
while start.weekday()!=6:
    start=start.fromordinal(start.toordinal()-1)
start=start.fromordinal(start.toordinal()-52*7)
colors=["#161b22","#0e4429","#006d32","#26a641","#39d353"]
parts=[]
for week in range(53):
    for dow in range(7):
        dt=start.fromordinal(start.toordinal()+week*7+dow)
        item=by_date.get(dt.isoformat(),{"level":0,"count":0})
        x=20+week*15;y=48+dow*15
        level=max(0,min(4,int(item["level"])))
        delay=week*.04+dow*.005
        title=html.escape(f'{dt.isoformat()} — {item["count"]} contributions')
        parts.append(f'<rect x="{x}" y="{y}" width="11" height="11" rx="3" fill="{colors[level]}" opacity="0"><title>{title}</title><animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur=".3s" fill="freeze"/></rect>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="820" height="190" viewBox="0 0 820 190"><rect width="820" height="190" rx="14" fill="#0d1117"/><g font-family="monospace"><text x="20" y="30" fill="#58a6ff" font-size="14">$ contribution_graph --live</text>{''.join(parts)}<text x="20" y="178" fill="#8b949e" font-size="11">Total: {D["total"]} • Generated: {D["generated_at"]}</text></g></svg>'''
open("graph.svg","w",encoding="utf-8").write(svg)