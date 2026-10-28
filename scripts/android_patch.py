#!/usr/bin/env python3
"""GitHub Actions içinde, `npx cap add android` sonrası çalışır.
İkonları, açılış ekranını, renkleri ve sürüm numarasını ayarlar."""
import os, re, sys, glob
from PIL import Image

RUN = int(sys.argv[1]) if len(sys.argv) > 1 else 1
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, 'android', 'app', 'src', 'main', 'res')
BG = '#140629'

icon = Image.open(os.path.join(ROOT, 'resources', 'icon.png')).convert('RGBA')
fg = Image.open(os.path.join(ROOT, 'resources', 'icon_fg.png')).convert('RGBA')
splash = Image.open(os.path.join(ROOT, 'resources', 'splash.png')).convert('RGB')

# 1) Uygulama ikonları (eski tip + yuvarlak + adaptive foreground)
LEGACY = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
FORE = {'mdpi': 108, 'hdpi': 162, 'xhdpi': 216, 'xxhdpi': 324, 'xxxhdpi': 432}
for d, px in LEGACY.items():
    folder = os.path.join(RES, f'mipmap-{d}')
    os.makedirs(folder, exist_ok=True)
    sq = icon.resize((px, px), Image.LANCZOS)
    sq.save(os.path.join(folder, 'ic_launcher.png'))
    mask = Image.new('L', (px, px), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).ellipse([0, 0, px - 1, px - 1], fill=255)
    rnd = Image.new('RGBA', (px, px), (0, 0, 0, 0)); rnd.paste(sq, (0, 0), mask)
    rnd.save(os.path.join(folder, 'ic_launcher_round.png'))
    fg.resize((FORE[d], FORE[d]), Image.LANCZOS).save(os.path.join(folder, 'ic_launcher_foreground.png'))

# adaptive ikon arka plan rengi
vals = os.path.join(RES, 'values')
os.makedirs(vals, exist_ok=True)
bgxml = os.path.join(vals, 'ic_launcher_background.xml')
open(bgxml, 'w').write(f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">{BG}</color>\n</resources>\n')

# 2) Açılış ekranı: şablondaki bütün splash.png dosyalarını aynı boyutta yenisiyle değiştir
for p in glob.glob(os.path.join(RES, 'drawable*', 'splash.png')):
    w, h = Image.open(p).size
    s = max(w / splash.width, h / splash.height)
    im = splash.resize((int(splash.width * s) + 1, int(splash.height * s) + 1), Image.LANCZOS)
    l = (im.width - w) // 2; t = (im.height - h) // 2
    im.crop((l, t, l + w, t + h)).save(p)

# 3) Tema: koyu durum çubuğu, Android 15 kenardan kenara zorunluluğundan çıkış
sty = os.path.join(vals, 'styles.xml')
x = open(sty, encoding='utf-8').read()
if 'xmlns:tools' not in x:
    x = x.replace('<resources>', '<resources xmlns:tools="http://schemas.android.com/tools">', 1)
ITEMS = [('android:statusBarColor', BG, ''), ('android:navigationBarColor', BG, ''),
         ('android:windowLightStatusBar', 'false', ''),
         ('android:windowOptOutEdgeToEdgeEnforcement', 'true', ' tools:targetApi="35"')]
def add_items(name, xml):
    m = re.search(r'<style name="' + re.escape(name) + r'"[^>]*>', xml)
    if not m:
        return xml
    end = xml.index('</style>', m.end())
    block = xml[m.end():end]
    add = ''.join(f'\n        <item name="{k}"{a}>{v}</item>' for k, v, a in ITEMS if f'name="{k}"' not in block)
    return xml[:m.end()] + add + xml[m.end():]
x = add_items('AppTheme.NoActionBar', x)
x = add_items('AppTheme.NoActionBarLaunch', x)
open(sty, 'w', encoding='utf-8').write(x)

# 4) Sürüm numarası
gradle = os.path.join(ROOT, 'android', 'app', 'build.gradle')
g = open(gradle, encoding='utf-8').read()
g = re.sub(r'versionCode\s+\d+', f'versionCode {RUN}', g)
g = re.sub(r'versionName\s+"[^"]*"', f'versionName "1.0.{RUN}"', g)
open(gradle, 'w', encoding='utf-8').write(g)
print(f'Tamam: ikonlar, açılış ekranı, tema ve sürüm 1.0.{RUN} ayarlandı.')
