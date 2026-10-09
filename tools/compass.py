"""Helpers for scripted calendar edits.

The published page (website/EISCompass.html) is the source of truth: it carries
all event data. load() reads that data; build(data) runs admin.html's own
publish code in headless Chrome and writes the new page, calendar feeds and
spreadsheet back into the project. Then run ./publish.sh to upload.

    import sys; sys.path.insert(0, 'tools')
    from compass import load, build
    d = load()
    ...edit d['events'] / d['closures'] / d['info']...
    build(d)
"""
import base64, html, json, os, re, shutil, subprocess, sys, tempfile, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'website', 'EISCompass.html')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
DATA_RE = re.compile(r'<script type="application/json" id="compass-data">([\s\S]*?)</script>')


def file_url(path):
    return 'file://' + urllib.parse.quote(path)


def load():
    m = DATA_RE.search(open(PAGE, encoding='utf-8').read())
    return json.loads(m.group(1).replace('<\\/', '</'))


def build(data):
    tmp = tempfile.mkdtemp(prefix='eis-compass-')
    shutil.copy(os.path.join(ROOT, 'admin', 'admin.html'), os.path.join(tmp, 'admin.html'))
    shutil.copy(PAGE, os.path.join(tmp, 'EISCompass.html'))
    json.dump(data, open(os.path.join(tmp, 'seed.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    url = file_url(os.path.join(tmp, 'admin.html')) + '?build=1&tpl=EISCompass.html&seed=seed.json'
    dom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--allow-file-access-from-files', '--no-first-run',
                          '--virtual-time-budget=30000', '--dump-dom', url], capture_output=True, text=True, timeout=180).stdout
    title = re.search(r'<title>(.*?)</title>', dom)
    if not title or title.group(1) != 'BUILD-DONE':
        sys.exit('Build failed: ' + (title.group(1) if title else dom[:500]))
    issues = []
    for path, body in re.findall(r'<textarea data-out="([^"]+)">(.*?)</textarea>', dom, re.S):
        body = html.unescape(body)
        if path == '_validation.json':
            issues = json.loads(body); continue
        if path.startswith('_'):
            continue
        if path.endswith('.b64'):
            dest, content = os.path.join(ROOT, 'admin', path[:-4]), base64.b64decode(body)
        else:
            dest, content = os.path.join(ROOT, 'website', path), body.encode('utf-8')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'wb').write(content)
    for x in issues:
        if x['level'] != 'info':
            print(f"  {x['level']}: {x.get('start') or ''} {x.get('event') or ''} — {x['msg']}")
    print('Built website/EISCompass.html, feeds and admin/EIS-Compass-events.xlsx')
