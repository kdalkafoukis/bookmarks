const API = 'http://127.0.0.1:7777';

const q = document.getElementById('q');
const results = document.getElementById('results');
const statusEl = document.getElementById('status');

let timer;
q.addEventListener('input', () => {
  clearTimeout(timer);
  timer = setTimeout(search, 120);
});

async function search() {
  const term = q.value.trim();
  if (!term) {
    results.replaceChildren();
    statusEl.textContent = '';
    return;
  }
  try {
    const res = await fetch(`${API}/search?q=${encodeURIComponent(term)}&limit=50`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    render(data.results || []);
  } catch (e) {
    statusEl.innerHTML = '';
    const err = document.createElement('span');
    err.className = 'error';
    err.textContent = `Can't reach local server (${e.message}). Run \`uv run bookmarks-serve\`.`;
    statusEl.appendChild(err);
    results.replaceChildren();
  }
}

function render(rows) {
  statusEl.textContent = `${rows.length} result${rows.length === 1 ? '' : 's'}`;
  results.replaceChildren();
  for (const r of rows) {
    const li = document.createElement('li');

    const name = document.createElement('div');
    name.className = 'name';
    name.textContent = r.name || r.title || '(untitled)';

    const url = document.createElement('div');
    url.className = 'url';
    url.textContent = r.url;

    const folder = document.createElement('div');
    folder.className = 'folder';
    folder.textContent = r.folder || '';

    const snippet = document.createElement('div');
    snippet.className = 'snippet';
    snippet.innerHTML = renderSnippet(r.snippet || '');

    li.append(name, url, folder, snippet);
    li.addEventListener('click', () => chrome.tabs.create({ url: r.url }));
    results.appendChild(li);
  }
}

// FTS5 returns text with literal <mark>/</mark> markers. Escape everything,
// then re-allow only those two tags.
function renderSnippet(s) {
  const escaped = s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
  return escaped
    .replace(/&lt;mark&gt;/g, '<mark>')
    .replace(/&lt;\/mark&gt;/g, '</mark>');
}
