"""Rebuild the two gallery levels after appending to assets/rings/catalog.json.
Uses Python standard library only; published artwork files are never written.
"""
from pathlib import Path
from html import escape as esc
import json
import hashlib
ROOT = Path(__file__).resolve().parents[1]
items = json.loads((ROOT/'assets/rings/catalog.json').read_text())
assert items and len({x['version'] for x in items}) == len(items)
latest = items[-1]
css_version = hashlib.sha256((ROOT/'assets/gallery.css').read_bytes()).hexdigest()[:10]

def head(title,prefix):
 social = ''
 if prefix == '../../':
  social = '<meta property="og:type" content="website"><meta property="og:title" content="Ring of Ideas · An Evolving Visual Study"><meta property="og:description" content="从粒子、轨道与自然意象出发，一组持续生长的浏览器视觉实验。"><meta property="og:url" content="https://moonstarlinda.github.io/Digital_Playground/works/publish/ring_of_ideas_index.html">'
 return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#292e2b"><meta name="description" content="灵感、自然与代码之间，一处持续生长的个人数字艺术创作空间。">{social}<title>{title}</title><link rel="stylesheet" href="{prefix}assets/gallery.css?v={css_version}"></head><body><a class="skip" href="#main">跳至内容</a>'''
def image(item,prefix,lazy=True):
 return f'<img src="{prefix}assets/rings/{esc(item["preview"])}" alt="{esc(item["title"])} · 作品画面" width="720" height="540" '+('loading="lazy"' if lazy else 'fetchpriority="high"')+' decoding="async">'
def artwork_href(item): return esc('./' + item['file'])
def footer(prefix): return f'<footer class="footer"><a href="{prefix}index.html">Digital Playground</a><a href="#top">回到顶部 ↑</a></footer></div></body></html>'
# The portfolio has its own layout and project manifest.
from build_playground import build_home
build_home()
page=head('Ring of Ideas · 数字艺术展览目录','../../')+f'''
<div class="page" id="top"><nav class="topbar" aria-label="页面导航"><a class="brand" href="../../index.html">← Digital Playground</a><span class="small" aria-current="page">RING OF IDEAS</span></nav>
<main id="main"><header class="collection-hero"><div><p class="eyebrow">AN EVOLVING VISUAL STUDY</p><h1>Ring <em>of Ideas</em></h1></div><div class="collection-intro"><p>从一个环开始，向不同的方向生长。</p><p class="secondary">从粒子的聚散、轨迹与几何，到自然、光影与时间。以代码为媒介，让每一次想法获得不同的形态。</p><a class="text-link" href="#collection">浏览全部作品 ↓</a></div></header>
<section class="latest" aria-labelledby="latest-title"><a class="latest-image" href="{artwork_href(latest)}">{image(latest,'../../',False)}</a><div class="latest-copy"><p class="eyebrow">最新作品 / V{latest['version']:02}</p><h2 id="latest-title">{esc(latest['title'])}</h2><p>{esc(latest['note'])}</p><a class="text-link" href="{artwork_href(latest)}">进入作品 ↗</a></div></section>
<section id="collection" class="collection" aria-labelledby="collection-title"><div class="section-heading"><h2 id="collection-title">环的演变 <span> / ALL WORKS</span></h2><span class="small">{len(items):02} 件作品 · 按创作顺序</span></div><div class="work-grid">'''
for item in items:
 date=f'<time datetime="{esc(item["date"])}">{esc(item["dateLabel"])}</time>' if item.get('date') else ''
 page+=f'''<article class="work" id="v{item['version']:02}"><a href="{artwork_href(item)}" aria-labelledby="title-{item['version']}"><div class="thumbnail">{image(item,'../../')}<span class="image-arrow" aria-hidden="true">↗</span></div><div class="work-meta"><span>V{item['version']:02}</span>{date}</div><h3 id="title-{item['version']}">{esc(item['title'])}</h3><p>{esc(item['note'])}</p></a></article>'''
page+=f'''</div></section><section class="colophon" aria-labelledby="about-series-title"><div class="about-copy"><p class="about-label">ABOUT THE SERIES</p><h2 id="about-series-title">从抽象结构，到自然与诗意。</h2><p class="about-description">Ring 最初从粒子、轨迹与几何结构出发，逐渐将探索延伸至自然景观、光影和诗歌意象。</p><p class="about-description">没有预设的视觉风格，也没有固定的创作边界。每一件作品，都是一次独立的尝试，也是这个系列持续变化的痕迹。</p></div><dl><div><dt>PERIOD</dt><dd>2025.11 — 持续更新</dd></div><div><dt>COLLECTION</dt><dd>{len(items)} Works</dd></div></dl></section></main>'''+footer('../../')
(ROOT/'works/publish/ring_of_ideas_index.html').write_text(page)
print(f'Built homepage and catalog with {len(items)} works; latest V{latest["version"]}.')
