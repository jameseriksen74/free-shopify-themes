import json, shutil, os, re, sys
SRC='/tmp/claude-0/petalpost'
OUT='/tmp/claude-0/out'
LOOKS = {
 'zapline': {
  'name':'Zapline',
  'colors': dict(color_background='#0E0E10', color_surface='#1A1A1F', color_text='#F2F2EE', color_accent='#D4FF3A', color_accent_text='#0E0E10', color_secondary='#7B61FF', color_sale='#FF5C39'),
  'presets': {
    'Zapline': dict(color_background='#0E0E10', color_surface='#1A1A1F', color_text='#F2F2EE', color_accent='#D4FF3A', color_accent_text='#0E0E10', color_secondary='#7B61FF', color_sale='#FF5C39'),
    'Daylight': dict(color_background='#F1F0EA', color_surface='#E3E1D8', color_text='#0E0E10', color_accent='#0E0E10', color_accent_text='#D4FF3A', color_secondary='#7B61FF', color_sale='#E8401C'),
    'Ultraviolet': dict(color_background='#120B24', color_surface='#1E1438', color_text='#F4F0FF', color_accent='#FF4FD8', color_accent_text='#120B24', color_secondary='#3AF2FF', color_sale='#FFB23A'),
  },
  'fonts': ('montserrat_n7','karla_n4'),
  'layout': dict(corner_radius=0, button_radius=0, page_width=1400),
  'hero_layout':'center',
  'tagline':'Loud, fast and fearless',
  'hero_heading':'Built to stand out',
  'eyebrow':'Drop 01',
  'css': '''
/* ---- Zapline look ---- */
h1, h2, h3, .h1, .h2, .h3, .display, .site-header__wordmark, .mobile-nav__link, .collection-card__title { text-transform: uppercase; letter-spacing: -0.025em; }
.display { font-size: calc(clamp(5rem, 9vw, 13rem) * var(--font-heading-scale)); line-height: .9; }
.eyebrow { color: var(--color-accent); letter-spacing: .3em; }
.announcement { background: var(--color-accent); color: var(--color-accent-text); font-weight: 700; text-transform: uppercase; letter-spacing: .2em; overflow: hidden; }
.announcement__inner { animation: zap-slide 14s linear infinite; white-space: nowrap; }
@keyframes zap-slide { from { transform: translateX(30%); } to { transform: translateX(-30%); } }
.site-header { border-bottom-width: 2px; border-color: var(--color-text); }
.site-nav__link { text-transform: uppercase; letter-spacing: .12em; font-size: 1.25rem; font-weight: 700; }
.button { text-transform: uppercase; font-weight: 700; letter-spacing: .14em; box-shadow: 4px 4px 0 var(--color-text); border: 2px solid var(--color-text); }
.button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0 var(--color-text); }
.button--outline { box-shadow: none; }
.hero__box { background: none; backdrop-filter: none; max-width: 110rem; }
.hero__media::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 30%, color-mix(in srgb, var(--color-background) 85%, transparent)); }
.media-frame, .card { border: 2px solid var(--color-text); }
.product-card__title { text-transform: uppercase; letter-spacing: .08em; font-size: 1.3rem; font-weight: 700; }
.badge { border-radius: 0; background: var(--color-accent); color: var(--color-accent-text); font-weight: 700; }
.pill { border-radius: 0; text-transform: uppercase; letter-spacing: .1em; font-size: 1.2rem; border-width: 2px; }
.quote__text { text-transform: uppercase; font-size: 2.4rem; line-height: 1.1; }
.newsletter { background: var(--color-accent); color: var(--color-accent-text); }
.newsletter .field { background: transparent; border: 2px solid var(--color-accent-text); color: var(--color-accent-text); }
.newsletter .field::placeholder { color: var(--color-accent-text); opacity: .7; }
.newsletter .button { background: var(--color-accent-text); color: var(--color-accent); border-color: var(--color-accent-text); box-shadow: none; }
.site-footer { border-top: 2px solid var(--color-text); }
@media (min-width: 990px) {
  .site-header__inner { grid-template-columns: auto 1fr auto; }
  .site-header__brand { grid-column: 1; text-align: left; }
  .site-nav { grid-column: 2; }
  .site-nav__list { justify-content: center; }
}
'''},
 'stillroom': {
  'name':'Stillroom',
  'colors': dict(color_background='#FFFFFF', color_surface='#F4F4F2', color_text='#141414', color_accent='#141414', color_accent_text='#FFFFFF', color_secondary='#3D5AFE', color_sale='#D93B30'),
  'presets': {
    'Stillroom': dict(color_background='#FFFFFF', color_surface='#F4F4F2', color_text='#141414', color_accent='#141414', color_accent_text='#FFFFFF', color_secondary='#3D5AFE', color_sale='#D93B30'),
    'Stone': dict(color_background='#F2EFEA', color_surface='#E6E1D9', color_text='#22201C', color_accent='#22201C', color_accent_text='#F2EFEA', color_secondary='#A5835C', color_sale='#B0412E'),
    'Ocean': dict(color_background='#F5F8FA', color_surface='#E5EDF2', color_text='#0F2233', color_accent='#1F5EFF', color_accent_text='#FFFFFF', color_secondary='#0FB5A6', color_sale='#E0453A'),
  },
  'fonts': ('jost_n4','jost_n4'),
  'layout': dict(corner_radius=4, button_radius=4, page_width=1440),
  'hero_layout':'split',
  'tagline':'Quiet design, clear focus',
  'hero_heading':'Less, but better',
  'eyebrow':'The essentials',
  'css': '''
/* ---- Stillroom look ---- */
body { letter-spacing: 0; }
h1, h2, h3, .h1, .h2, .h3, .display { font-weight: 400; letter-spacing: -0.035em; }
.display { font-size: calc(clamp(4.4rem, 7vw, 9.6rem) * var(--font-heading-scale)); line-height: .95; }
.eyebrow { display: inline-flex; align-items: center; gap: .8rem; letter-spacing: .14em; font-size: 1.1rem; }
.eyebrow::before { content: ""; width: .8rem; height: .8rem; border-radius: 50%; background: var(--color-secondary); }
.announcement { background: var(--color-surface); color: var(--color-text); font-size: 1.2rem; }
.site-header { background: color-mix(in srgb, var(--color-background) 80%, transparent); backdrop-filter: saturate(1.6) blur(14px); }
.site-nav__link { font-size: 1.4rem; color: var(--color-text-soft); }
.site-nav__link:hover, .site-nav__link[aria-current="page"] { color: var(--color-text); text-decoration: none; }
.button { letter-spacing: .02em; font-size: 1.45rem; }
.button:hover { box-shadow: none; opacity: .88; transform: none; }
.hero--split { background: var(--color-surface); }
@media (min-width: 990px) { .hero--split .hero__box { border: 0; background: none; backdrop-filter: none; } }
.hero__box { background: color-mix(in srgb, var(--color-background) 70%, transparent); backdrop-filter: blur(20px) saturate(1.4); border: 1px solid color-mix(in srgb, var(--color-text) 10%, transparent); }
.product-card__info { display: flex; justify-content: space-between; gap: 1.2rem; align-items: baseline; }
.product-card__info .price { flex-shrink: 0; }
.product-card__title { font-size: 1.45rem; }
.product-grid { gap: 4rem 1.2rem; }
.card { border: 1px solid var(--color-border); background: var(--color-background); }
.quote { background: var(--color-surface); border: 0; }
.quote__text { font-size: 2rem; letter-spacing: -0.01em; }
.collection-card__title { font-family: var(--font-body-family); font-size: 1.6rem; justify-content: space-between; }
.newsletter { background: var(--color-text); color: var(--color-background); }
.newsletter .field { background: transparent; color: var(--color-background); border-color: color-mix(in srgb, var(--color-background) 40%, transparent); }
.newsletter .button { background: var(--color-background); color: var(--color-text); border-color: var(--color-background); }
.site-footer { background: var(--color-surface); border-top: 0; }
@media (min-width: 990px) {
  .site-header__inner { grid-template-columns: auto 1fr auto; }
  .site-header__brand { grid-column: 1; text-align: left; }
  .site-nav { grid-column: 2; }
  .site-nav__list { justify-content: center; gap: 3.6rem; }
}
'''},
}

def build(key, cfg):
    dst=os.path.join(OUT,key)
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(SRC,dst)
    name=cfg['name']
    # text replacements
    for dp,_,fs in os.walk(dst):
        for f in fs:
            p=os.path.join(dp,f); s=open(p).read()
            s2=s.replace('Petalpost theme by','%s theme by'%name).replace('Petalpost is a free theme','%s is a free theme'%name).replace('"theme_name": "Petalpost"','"theme_name": "%s"'%name)
            if s2!=s: open(p,'w').write(s2)
    # schema defaults
    sp=os.path.join(dst,'config/settings_schema.json'); sch=json.load(open(sp))
    for grp in sch[1:]:
        for st in grp.get('settings',[]):
            i=st.get('id')
            if i in cfg['colors']: st['default']=cfg['colors'][i]
            if i=='type_heading_font': st['default']=cfg['fonts'][0]
            if i=='type_body_font': st['default']=cfg['fonts'][1]
            if i in cfg['layout']: st['default']=cfg['layout'][i]
    json.dump(sch,open(sp,'w'),indent=2)
    first=list(cfg['presets'])[0]
    presets={k:dict(v,type_heading_font=cfg['fonts'][0],type_body_font=cfg['fonts'][1],**cfg['layout']) for k,v in cfg['presets'].items()}
    json.dump({'current':first,'presets':presets},open(os.path.join(dst,'config/settings_data.json'),'w'),indent=2)
    # hero defaults
    ip=os.path.join(dst,'templates/index.json'); idx=json.load(open(ip))
    idx['sections']['hero']['settings']=dict(layout=cfg['hero_layout'],heading=cfg['hero_heading'],eyebrow=cfg['eyebrow'],text='<p>%s.</p>'%cfg['tagline'])
    json.dump(idx,open(ip,'w'),indent=2)
    with open(os.path.join(dst,'assets/base.css'),'a') as f: f.write(cfg['css'])

def petal():
    dst=os.path.join(OUT,'petalpost')
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(SRC,dst)
    for dp,_,fs in os.walk(dst):
        for f in fs:
            p=os.path.join(dp,f); s=open(p).read()
            s2=s.replace('window.posyStrings','window.themeStrings')
            if s2!=s: open(p,'w').write(s2)

os.makedirs(OUT,exist_ok=True)
petal()
for k,c in LOOKS.items(): build(k,c)
print('built', os.listdir(OUT))
