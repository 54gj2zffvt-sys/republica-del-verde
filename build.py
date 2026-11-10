"""Arma index.html (un solo archivo) a partir de src/page.html y assets/.
Uso: python3 build.py"""
import base64, re, pathlib
ROOT = pathlib.Path(__file__).parent
b64 = lambda p: base64.b64encode((ROOT / p).read_bytes()).decode()
ICONS = {'whatsapp': 'whatsapp-logo', 'plus': 'plus', 'minus': 'minus', 'x': 'x', 'copy': 'copy'}
symbols = []
for sid, name in ICONS.items():
    svg = (ROOT / f'assets/icons/{name}-bold.svg').read_text()
    inner = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.S).group(1)
    symbols.append(f'<symbol id="i-{sid}" viewBox="0 0 256 256">{inner}</symbol>')
sprite = '<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">' + ''.join(symbols) + '</svg>'
html = (ROOT / 'src/page.html').read_text(encoding='utf-8')
for key, val in {'%%ROMAN%%': b64('assets/rdv-roman.woff2'), '%%ITALIC%%': b64('assets/rdv-italic.woff2'),
                 '%%SEAL%%': b64('assets/seal-cream.webp'), '%%ICONS%%': sprite}.items():
    assert html.count(key) == 1, key
    html = html.replace(key, val)
assert '%%' not in html
(ROOT / 'index.html').write_text(html, encoding='utf-8')
print('index.html', f'{len(html.encode())/1024:.0f} KB')
