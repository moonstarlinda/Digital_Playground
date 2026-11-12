"""Build the portfolio from a mixed list of series and standalone works."""
from pathlib import Path
from html import escape
import json
import hashlib
ROOT = Path(__file__).resolve().parents[1]

def build_home():
 projects = json.loads((ROOT/'assets/playground/projects.json').read_text())
 rings = json.loads((ROOT/'assets/rings/catalog.json').read_text())
 collections=[]
 independent=[]
 for index, project in enumerate(projects):
  series=project['kind']=='series'
  if project.get('previews'):
   images=[]
   for selected in project['previews']:
    work=rings[-1] if selected=='latest' else next(w for w in rings if w['version']==selected)
    images.append(f'<div><img src="assets/rings/{escape(work["preview"])}" alt="{escape(work["title"])} · 作品画面" width="720" height="540" loading="lazy" decoding="async"></div>')
   visual='<div class="project-visual collage">'+''.join(images)+'</div>'
  else:
   visual=f'<div class="project-visual"><img src="{escape(project["preview"])}" alt="{escape(project["title"])} · 作品画面" width="1008" height="700" loading="lazy" decoding="async"></div>'
  extra=' target="_blank" rel="noopener noreferrer"' if project.get('external') else ''
  cards=collections if series else independent
  if not series:
   english = f'<small>{escape(project["titleEnglish"])}</small>' if project.get('titleEnglish') else ''
   new_window = f'<span class="visually-hidden" id="window-{index}">在新窗口打开</span>' if project.get('external') else ''
   accessible = f' aria-describedby="window-{index}"' if project.get('external') else ''
   cards.append(f'''<article class="project independent-entry {escape(project['id'])}"><a href="{escape(project['href'])}"{extra} aria-labelledby="project-{index}"{accessible}>{visual}<div class="project-info"><h3 id="project-{index}"><span class="project-title">{escape(project['title'])}{english}</span><span class="title-arrow" aria-hidden="true">↗</span></h3><p class="project-description">{escape(project.get('summary',project['description']))}</p>{new_window}</div></a></article>''')
   continue
  meta=f'{len(rings):02} 件作品 · 持续生长' if project['id']=='ring-of-ideas' else project.get('subtitle','浏览器作品')
  cards.append(f'''<article class="project collection-entry {escape(project['id'])}"><a href="{escape(project['href'])}"{extra} aria-labelledby="project-{index}">{visual}<div class="project-info"><div class="project-meta"><span>{escape(meta)}</span></div><h3 id="project-{index}">{escape(project['title'])}</h3><p class="project-description">{escape(project['description'])}</p><p class="project-note">{escape(project.get('note',''))}</p><div class="project-action"><span>探索系列</span><span aria-hidden="true">↗</span></div></div></a></article>''')
 waves = '<div class="hero-waves" aria-hidden="true"><svg viewBox="0 0 1600 600" preserveAspectRatio="none"><defs><linearGradient id="wave-violet" x1="0%" y1="0%" x2="100%" y2="0%"><stop stop-color="#aa94cd" stop-opacity="0"/><stop offset=".12" stop-color="#aa94cd" stop-opacity=".3"/><stop offset=".88" stop-color="#aa94cd" stop-opacity=".3"/><stop offset="1" stop-color="#aa94cd" stop-opacity="0"/></linearGradient><linearGradient id="wave-soft-violet" x1="0%" y1="0%" x2="100%" y2="0%"><stop stop-color="#aa94cd" stop-opacity="0"/><stop offset=".5" stop-color="#aa94cd" stop-opacity=".3"/><stop offset="1" stop-color="#aa94cd" stop-opacity="0"/></linearGradient><filter id="wave-soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter></defs><g fill="url(#wave-violet)" filter="url(#wave-soft)">'
 for x,width,bend,strength in [(-40,230,9,.85),(142,195,12,1),(337,285,7,.8),(563,215,10,1),(747,275,8,.85),(1008,230,12,1),(1203,305,9,.8),(1475,245,10,1),(1660,230,8,.9),(395,135,6,.62),(1110,185,8,.7),(1368,115,7,.65)]:
  left, right = x-width/2, x+width/2
  band_fill = ' fill="url(#wave-soft-violet)"' if x == 1368 else ''
  waves += f'<g class="light-band" opacity="{strength}"{band_fill}><path d="M{left},-100 C{left-bend},50 {left+bend},135 {left+3},260 S{left-bend},440 {left+6},700 L{right+6},700 C{right-bend},440 {right+bend},350 {right+3},260 S{right-bend},50 {right},-100 Z"/></g>'
 waves += '</g></svg></div>'
 # Use the same parameters as the author-spectrum tuning tool.
 spectrum = json.loads((ROOT/'assets/playground/author-spectrum.json').read_text())
 closing_waves = f'<div class="hero-waves closing-waves" aria-hidden="true" style="opacity:{spectrum["density"]/100}"><svg viewBox="0 0 1600 600" preserveAspectRatio="none"><defs><filter id="closing-blur" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="{spectrum["blur"]}"/></filter>'
 for i, band in enumerate(spectrum['bands']):
  alpha, edge = band['a']/250, spectrum['softness']/100
  closing_waves += f'<linearGradient id="closing-{i}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#aa94cd" stop-opacity="0"/><stop offset="{edge}" stop-color="#aa94cd" stop-opacity="{alpha}"/><stop offset="{1-edge}" stop-color="#aa94cd" stop-opacity="{alpha}"/><stop offset="1" stop-color="#aa94cd" stop-opacity="0"/></linearGradient>'
 closing_waves += '</defs><g filter="url(#closing-blur)">'
 for i, band in enumerate(spectrum['bands']):
  closing_waves += f'<rect x="-100" y="{(band["y"]-band["w"]/2)*6}" width="1800" height="{band["w"]*6}" fill="url(#closing-{i})"/>'
 closing_waves += '</g></svg></div>'
 html='''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#eeedf4"><meta name="description" content="Digital Playground，个人数字艺术作品集。系列、独立作品与浏览器中的创作实验。"><title>Digital Playground · 数字艺术作品集</title><link rel="stylesheet" href="assets/playground.css"></head><body><a class="skip" href="#main">跳至内容</a><div class="portfolio" id="top"><header class="site-header"><a href="./index.html" class="brand"><span class="brand-mark" aria-hidden="true">✳</span> Digital Playground</a><nav class="header-nav" aria-label="首页导航"><a href="#collections">创作系列</a><a href="#independent-works">独立作品</a><a href="#about">关于作者</a></nav></header><main id="main"><section class="intro">'''+waves+'''<div class="intro-heading"><p class="eyebrow">AN OPEN SPACE FOR IDEAS</p><h1>Digital<br><em>Playground.</em></h1></div><div class="intro-opening"><div class="opening-poem"><p>这些页面，<br>就像我生活的一张张立体照片；</p><p>就像一道光，<br>复现那些瞬间的全息影像；</p><p>就像未知维度的弦，<br>拨动时间之轴，<br>短暂回到当时，<br>也与未来共鸣。</p></div></div></section><div id="works"><section id="collections" aria-labelledby="collections-title"><div class="works-heading"><h2 id="collections-title">创作系列 <span>/ COLLECTIONS</span></h2></div><div class="collections">'''+''.join(collections)+'''</div></section><section id="independent-works" aria-labelledby="independent-title"><div class="works-heading"><h2 id="independent-title">独立作品 <span>/ INDEPENDENT WORKS</span></h2></div><div class="independent-grid">'''+''.join(independent)+'''</div></section></div><section id="about" class="author-section" aria-labelledby="author-title">'''+closing_waves+'''<div class="author-copy"><p class="author-label">关于作者 <span>/ ABOUT THE CREATOR</span></p><h2 id="author-title">你好，我是 Lin。</h2><p>我是一个非职业的数字艺术创作者，目前住在中国北京。</p><details class="author-details"><summary><span class="when-closed">更多关于我</span><span class="when-open">收起介绍</span><span class="details-arrow" aria-hidden="true">↓</span></summary><div class="author-details-body"><p>我喜欢在自然风光中漫步闲游，也喜欢逛展、听音乐、看电影；对天文物理充满好奇，也乐于了解科技的最新进展。</p><p>近一年来，我有了更多闲暇时间。借助日益强大的 AI 工具，我开始以自己生活中的所见、所思、所感为灵感和素材，将它们制作成网页形式的作品。</p><p>这些页面就像是我生活的一张张立体照片，或许稚嫩，却无比真实。</p><p>Digital Playground 收录了我的大部分作品，就如同一个线上博物馆。随着时光流逝，展品会越来越多，希望精品也越来越多。</p></div></details></div><div class="author-contact"><p class="author-label">交流与联系 <span>/ GET IN TOUCH</span></p><h3>留下你的想法。</h3><p>欢迎分享观看感受、提出问题，或聊聊作品背后的想法。</p><div class="guestbook-entry"><a href="https://github.com/moonstarlinda/Digital_Playground/discussions/1" target="_blank" rel="noopener noreferrer">在 GitHub 留言 ↗</a><p class="contact-note">通过 GitHub Discussions 留言，与我公开交流。需要 GitHub 账号。</p></div></div></section></main><footer class="site-footer"><span>Digital Playground · Lin 的数字艺术作品集</span><nav class="footer-nav" aria-label="作者与页面导航"><a href="#top">回到顶部 ↑</a></nav></footer></div></body></html>'''
 css_version = hashlib.sha256((ROOT/'assets/playground.css').read_bytes()).hexdigest()[:10]
 html = html.replace('href="assets/playground.css"', f'href="assets/playground.css?v={css_version}"')
 (ROOT/'index.html').write_text(html)
 print(f'Built portfolio with {len(projects)} entries.')

if __name__=='__main__':build_home()
