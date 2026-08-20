import fs from 'node:fs';
import path from 'node:path';

const projectRoot = path.resolve(import.meta.dirname, '..');
const entry = path.join(projectRoot, 'works/drafts/ring_v12_lateral_accretion_study_18.html');
const output = path.join(projectRoot, 'works/publish/ring_v12_the_river_remembers.html');

function escapeSrcdoc(html) {
  return html
    .replaceAll('&', '&amp;')
    .replaceAll('"', '&quot;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

function bundleHtml(filename, stack = []) {
  const resolved = path.resolve(filename);
  if (stack.includes(resolved)) {
    throw new Error(`Circular iframe dependency: ${[...stack, resolved].join(' -> ')}`);
  }

  let html = fs.readFileSync(resolved, 'utf8');
  const iframePattern = /<iframe([^>]*?)src="([^"?#]+\.html)"([^>]*)><\/iframe>/g;
  html = html.replace(iframePattern, (_match, before, source, after) => {
    const childPath = path.resolve(path.dirname(resolved), source);
    const childHtml = bundleHtml(childPath, [...stack, resolved]);
    return `<iframe${before}srcdoc="${escapeSrcdoc(childHtml)}"${after}></iframe>`;
  });
  return html;
}

let published = bundleHtml(entry)
  .replace('<title>Ring V12 · Lateral Accretion Study 18</title>', '<title>Ring V12 · The River Remembers</title>')
  .replace('../assets/ring_v12/ergun_river.jpeg', '../assets/ring_v12/ergun_river_web.jpg?v=2')
  .replace('../assets/ring_v12/hand-drawing.jpeg', '../assets/ring_v12/hand-drawing_web.jpg?v=2')
  .replace('../assets/ring_v12/excalidraw-process.png', '../assets/ring_v12/excalidraw_process_web.png?v=2')
  .replace('../publish/ring_of_ideas_index.html', './ring_of_ideas_index.html');

const marker = '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">';
published = published.replace(marker, `${marker}\n<meta name="description" content="Ring V12 · The River Remembers — 额尔古纳河的迁移、沉积与植物洲体。">`);

fs.writeFileSync(output, published);
console.log(`Built ${path.relative(projectRoot, output)} (${Buffer.byteLength(published)} bytes)`);
