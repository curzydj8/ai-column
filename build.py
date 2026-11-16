#!/usr/bin/env python3
"""Build the AI 专栏 timeline page from data.json -> index.html."""
import json, html
from collections import OrderedDict

SRC = "/home/hatch/workspace/ai-column/data.json"
DST = "/home/hatch/workspace/ai-column/index.html"

with open(SRC, encoding="utf-8") as f:
    items = json.load(f)

items.sort(key=lambda x: x["date"], reverse=True)

cats = []
for it in items:
    if it["cat"] not in cats:
        cats.append(it["cat"])

price_class = {"免费": "free", "免费+订阅": "freemium", "付费": "paid", "已停服": "dead"}
price_label = {"免费": "免费", "免费+订阅": "免费+订阅", "付费": "付费", "已停服": "已停服"}

def esc(s):
    return html.escape(s or "")

# group by year, newest first
years = OrderedDict()
for it in items:
    y = it["date"][:4]
    years.setdefault(y, []).append(it)

cards = []
for y, group in years.items():
    cards.append(f'<h2 class="year">{y} 年 <span class="ycount">{len(group)} 个</span></h2>')
    cards.append('<div class="tl">')
    for it in group:
        pc = price_class[it["price"]]
        pl = price_label[it["price"]]
        miles = f'<p class="miles">{esc(it["miles"])}</p>' if it.get("miles") else ""
        status = f'<p class="status">⚠ {esc(it["status"])}</p>' if it.get("status") else ""
        note = f'<p class="note">注：{esc(it["note"])}</p>' if it.get("note") else ""
        cards.append(f'''<article class="card" data-cat="{esc(it["cat"])}" data-price="{esc(it["price"])}">
  <div class="top"><span class="date">{esc(it["date"])}</span><span class="cat">{esc(it["cat"])}</span><span class="price {pc}">{pl}</span></div>
  <h3><a href="{esc(it["url"])}" target="_blank" rel="noopener">{esc(it["name"])}</a></h3>
  <p class="vendor">{esc(it["vendor"])}</p>
  <p class="best">{esc(it["best"])}</p>
  {miles}
  <p class="priced">💰 {esc(it["price_detail"])}</p>
  {status}{note}
</article>''')
    cards.append('</div>')

filters = '<button class="fbtn on" data-cat="全部">全部</button>' + "".join(
    f'<button class="fbtn" data-cat="{esc(c)}">{esc(c)}</button>' for c in cats)

page = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 专栏 · 新 AI 时间线（2022–2026）</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#f6f7f9;color:#1c1c1e;line-height:1.6}}
.wrap{{max-width:860px;margin:0 auto;padding:36px 18px 60px}}
header{{margin-bottom:24px}}
h1{{font-size:28px;margin-bottom:6px}}
.sub{{color:#666;font-size:15px}}
.stats{{display:flex;gap:16px;flex-wrap:wrap;margin-top:14px;color:#555;font-size:14px}}
.stats b{{color:#111}}
.filters{{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0 8px;position:sticky;top:0;background:#f6f7f9;padding:10px 0;z-index:5}}
.fbtn{{border:1px solid #d4d4d8;background:#fff;border-radius:999px;padding:6px 14px;font-size:14px;cursor:pointer}}
.fbtn.on{{background:#111;color:#fff;border-color:#111}}
.pfbtn{{border:1px solid #d4d4d8;background:#fff;border-radius:999px;padding:6px 14px;font-size:14px;cursor:pointer}}
.pfbtn.on{{background:#2563eb;color:#fff;border-color:#2563eb}}
.year{{font-size:22px;margin:28px 0 12px;border-bottom:2px solid #111;padding-bottom:6px}}
.ycount{{font-size:14px;color:#888;font-weight:400}}
.tl{{display:flex;flex-direction:column;gap:14px}}
.card{{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:18px 20px}}
.card.hide{{display:none}}
.top{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:6px}}
.date{{font-family:ui-monospace,Menlo,monospace;font-size:13px;color:#666;background:#f0f0f2;border-radius:6px;padding:2px 8px}}
.cat{{font-size:12px;color:#555;background:#eef2ff;border-radius:999px;padding:2px 9px}}
.price{{font-size:12px;border-radius:999px;padding:2px 9px}}
.price.free{{background:#dcfce7;color:#166534}}
.price.freemium{{background:#dbeafe;color:#1d4ed8}}
.price.paid{{background:#fef3c7;color:#92400e}}
.price.dead{{background:#e5e7eb;color:#6b7280}}
.card h3{{font-size:19px}}
.card h3 a{{color:#111;text-decoration:none}}
.card h3 a:hover{{color:#2563eb;text-decoration:underline}}
.vendor{{color:#888;font-size:13px;margin:2px 0 8px}}
.best{{font-size:15px}}
.miles{{color:#666;font-size:13px;margin-top:6px}}
.priced{{font-size:14px;margin-top:8px;color:#333}}
.status{{color:#b91c1c;font-size:13px;margin-top:6px}}
.note{{color:#888;font-size:13px;margin-top:4px}}
footer{{margin-top:40px;color:#888;font-size:13px;border-top:1px solid #e5e7eb;padding-top:16px}}
footer p{{margin-bottom:6px}}
.empty{{display:none;text-align:center;color:#888;padding:40px 0}}
</style>
</head>
<body>
<div class="wrap">
<header>
<h1>AI 专栏 · 新 AI 时间线</h1>
<p class="sub">从 2022 年 ChatGPT 到现在，值得知道的 AI 产品按发布时间倒序排列：每个都写清是什么、要不要充值、最适合干什么。</p>
<div class="stats"><span>共 <b>{len(items)}</b> 个产品</span><span><b>{len(cats)}</b> 个分类</span><span>更新于 <b>2026-11-16</b></span></div>
</header>
<div class="filters" id="catFilters">{filters}</div>
<div class="filters" id="priceFilters" style="position:static;padding-top:0">
<button class="pfbtn on" data-price="全部">全部价格</button>
<button class="pfbtn" data-price="免费">免费</button>
<button class="pfbtn" data-price="免费+订阅">免费+订阅</button>
<button class="pfbtn" data-price="付费">付费</button>
</div>
{''.join(cards)}
<p class="empty" id="empty">没有符合筛选的产品，换个分类试试。</p>
<footer>
<p>口径：日期为产品首次公开上线的月份；定价为 2026-11 核查时的公开价，订阅价常变，以官网为准。标“待核验”的价格或地址未完全核实，请以官网为准。</p>
<p>海外产品在中国大陆多需自行解决网络访问，国内产品可直接用。2026 年是“大版本年”：全新独立产品线只有 Muse、Gemini Omni、Claude Cowork 三条，其余多为既有产品的大版本升级。</p>
<p>数据来源：各产品官网与公开报道整理；发现错误或有新 AI 想补上，欢迎提 issue。</p>
</footer>
</div>
<script>
let cat="全部", price="全部";
function apply(){{
  let n=0;
  document.querySelectorAll(".card").forEach(c=>{{
    const ok=(cat==="全部"||c.dataset.cat===cat)&&(price==="全部"||c.dataset.price===price);
    c.classList.toggle("hide",!ok); if(ok)n++;
  }});
  document.querySelectorAll(".year").forEach(y=>{{
    const next=y.nextElementSibling;
    const vis=[...next.querySelectorAll(".card")].some(c=>!c.classList.contains("hide"));
    y.style.display=vis?"":"none"; next.style.display=vis?"":"none";
  }});
  document.getElementById("empty").style.display=n?"none":"block";
}}
document.getElementById("catFilters").addEventListener("click",e=>{{
  if(e.target.tagName!=="BUTTON")return;
  document.querySelectorAll("#catFilters .fbtn").forEach(b=>b.classList.remove("on"));
  e.target.classList.add("on"); cat=e.target.dataset.cat; apply();
}});
document.getElementById("priceFilters").addEventListener("click",e=>{{
  if(e.target.tagName!=="BUTTON")return;
  document.querySelectorAll("#priceFilters .pfbtn").forEach(b=>b.classList.remove("on"));
  e.target.classList.add("on"); price=e.target.dataset.price; apply();
}});
</script>
</body>
</html>'''

with open(DST, "w", encoding="utf-8") as f:
    f.write(page)
print(f"wrote {DST}: {len(items)} items, {len(years)} years, {len(page)} bytes")
