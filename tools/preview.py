import json, base64, random, sys
OUT='/tmp/claude-0/out'
FONTS={'playfair_display':'Playfair Display','work_sans':'Work Sans','montserrat':'Montserrat','karla':'Karla','jost':'Jost'}
def font(h):
    fam,w=h.rsplit('_n',1); return FONTS[fam], int(w)*100
def art(seed, c1, c2, c3, w=800, h=1000):
    r=random.Random(seed)
    shapes=''
    kind=seed%4
    cx,cy=w/2,h*0.58
    if kind==0:
        shapes=f'<ellipse cx="{cx}" cy="{h*0.86}" rx="{w*0.32}" ry="{h*0.04}" fill="{c3}" opacity=".25"/><path d="M{cx-w*0.18} {h*0.85} C{cx-w*0.3} {h*0.55},{cx-w*0.08} {h*0.45},{cx-w*0.06} {h*0.3} L{cx+w*0.06} {h*0.3} C{cx+w*0.08} {h*0.45},{cx+w*0.3} {h*0.55},{cx+w*0.18} {h*0.85}Z" fill="{c3}"/>'
    elif kind==1:
        shapes=f'<circle cx="{cx}" cy="{cy}" r="{w*0.27}" fill="{c3}"/><circle cx="{cx+w*0.12}" cy="{cy-h*0.12}" r="{w*0.1}" fill="{c1}" opacity=".7"/>'
    elif kind==2:
        shapes=f'<rect x="{w*0.25}" y="{h*0.25}" width="{w*0.5}" height="{h*0.6}" rx="{w*0.25}" fill="{c3}"/><rect x="{w*0.4}" y="{h*0.17}" width="{w*0.2}" height="{h*0.1}" rx="8" fill="{c3}" opacity=".8"/>'
    else:
        shapes=f'<path d="M{w*0.2} {h*0.85} L{cx} {h*0.25} L{w*0.8} {h*0.85}Z" fill="{c3}"/><circle cx="{w*0.7}" cy="{h*0.3}" r="{w*0.08}" fill="{c1}"/>'
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="{w}" height="{h}" fill="url(#g)"/>{shapes}</svg>'
    return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
def mix(a,b,t):
    a=[int(a[i:i+2],16) for i in (1,3,5)]; b=[int(b[i:i+2],16) for i in (1,3,5)]
    return '#'+''.join('%02x'%round(x+(y-x)*t) for x,y in zip(a,b))
def page(key, preset=None):
    sch=json.load(open(f'{OUT}/{key}/config/settings_schema.json'))
    data=json.load(open(f'{OUT}/{key}/config/settings_data.json'))
    d={}
    for g in sch[1:]:
        for s in g.get('settings',[]):
            if 'id' in s and 'default' in s: d[s['id']]=s['default']
    pname=preset or data['current']
    d.update(data['presets'][pname])
    idx=json.load(open(f'{OUT}/{key}/templates/index.json'))
    hero=idx['sections']['hero']['settings']
    hf,hw=font(d['type_heading_font']); bf,bw=font(d['type_body_font'])
    css=open(f'{OUT}/{key}/assets/base.css').read()
    bg,su,tx,ac,sec=d['color_background'],d['color_surface'],d['color_text'],d['color_accent'],d['color_secondary']
    name=sch[0]['theme_name']
    def img(i,w=800,h=1000):
        pal=[(mix(su,ac,.25),mix(su,sec,.45),mix(ac,tx,.15)),(mix(su,sec,.35),mix(bg,su,.5),mix(sec,tx,.25)),(mix(bg,ac,.15),mix(su,ac,.5),mix(bg,tx,.1)),(mix(su,tx,.1),mix(su,sec,.25),ac)]
        p=pal[i%4]; return art(i,p[0],p[1],p[2],w,h)
    prods=[('Linen Bloom Vase','$48.00',None),('Soft Glow Candle','$32.00','$40.00'),('Ceramic Pebble Set','$64.00',None),('Dewdrop Tumbler','$22.00',None)]
    cards=''.join(f'''<li><div class="product-card is-visible"><a class="product-card__link" href="#"><div class="product-card__media media-frame media-frame--portrait"><img class="cover product-card__image" src="{img(i)}" alt="">{'<span class="badge badge--sale product-card__badge">Sale</span>' if c else ''}</div><div class="product-card__info"><h3 class="product-card__title">{t}</h3><div class="price{' price--sale' if c else ''}"><span class="price__current">{p}</span>{f'<s class="price__compare">{c}</s>' if c else ''}</div></div></a></div></li>''' for i,(t,p,c) in enumerate(prods))
    cols=''.join(f'<li><a href="#" class="collection-card"><div class="media-frame media-frame--portrait"><img class="cover" src="{img(i+5)}" alt=""></div><span class="collection-card__title">{t} <svg class="icon icon--small" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></a></li>' for i,t in enumerate(['Home','Gifts','Wellness']))
    fonts='&'.join(f'family={f.replace(" ","+")}:wght@{";".join(sorted({str(w),"700"}))}' for f,w in {(hf,hw),(bf,bw)})
    html=f'''<!doctype html><html class="js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet">
<style>:root{{--font-heading-family:"{hf}",serif;--font-heading-style:normal;--font-heading-weight:{hw};--font-body-family:"{bf}",sans-serif;--font-body-style:normal;--font-body-weight:{bw};--font-body-scale:1;--font-heading-scale:1;
--color-background:{bg};--color-surface:{su};--color-text:{tx};--color-text-soft:color-mix(in srgb,{tx} 68%,transparent);--color-accent:{ac};--color-accent-text:{d['color_accent_text']};--color-secondary:{sec};--color-border:color-mix(in srgb,{tx} 14%,transparent);--color-sale:{d['color_sale']};--page-width:{d['page_width']}px;--radius:{d['corner_radius']}px;--radius-button:{d['button_radius']}px}}
{css}</style></head><body>
<div class="announcement"><div class="page-width announcement__inner"><p>Free shipping on orders over $50</p></div></div>
<header class="site-header"><div class="page-width site-header__inner">
<details class="mobile-nav"><summary class="icon-button"><svg class="icon" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M3 7h18M3 12h18M3 17h12"/></svg></summary></details>
<div class="site-header__brand"><a class="site-header__logo" href="#"><span class="site-header__wordmark">{name}</span></a></div>
<nav class="site-nav"><ul class="site-nav__list" role="list"><li><a class="site-nav__link" href="#">Shop</a></li><li><a class="site-nav__link" href="#">New in</a></li><li><a class="site-nav__link" href="#">Gifts</a></li><li><a class="site-nav__link" href="#">Journal</a></li></ul></nav>
<div class="site-header__icons"><a class="icon-button" href="#"><svg class="icon" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></svg></a><a class="icon-button header-account" href="#"><svg class="icon" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="8.5" r="4"/><path d="M4.5 20.5c1.4-3.6 4.2-5.5 7.5-5.5s6.1 1.9 7.5 5.5"/></svg></a><a class="icon-button" href="#"><svg class="icon" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M5 8h14l-1.2 12.2a1 1 0 0 1-1 .8H7.2a1 1 0 0 1-1-.8L5 8Z"/><path d="M9 10V6.5a3 3 0 0 1 6 0V10"/></svg><span class="header-cart__count">2</span></a></div>
</div></header>
<main class="main">
<div class="section hero hero--large hero--{hero.get('layout','left')}"><div class="hero__media"><img class="hero__image" src="{img(1,1600,1000)}" alt=""></div><div class="hero__content page-width"><div class="hero__box"><p class="eyebrow">{hero.get('eyebrow','New season')}</p><h2 class="hero__heading display">{hero.get('heading','Little luxuries, made to keep')}</h2><div class="hero__text rte">{hero.get('text','<p>Thoughtfully chosen pieces for everyday joy.</p>')}</div><a class="button button--large" href="#">Shop the collection</a></div></div></div>
<div class="section"><div class="page-width"><div class="section-header"><h2 class="h2">Fresh picks</h2><a class="link-arrow" href="#">View all</a></div><ul class="product-grid product-grid--4" role="list">{cards}</ul></div></div>
<div class="section"><div class="page-width"><div class="section-header"><h2 class="h2">Shop by mood</h2></div><ul class="collection-grid" role="list">{cols}</ul></div></div>
<div class="section"><div class="page-width image-text"><div class="image-text__media media-frame"><img class="cover" src="{img(2,1000,1250)}" alt=""></div><div class="image-text__content"><p class="eyebrow">Our story</p><h2 class="h2">Made slowly, chosen carefully</h2><div class="rte"><p>Share the story behind your brand, your makers or your materials.</p></div><a class="button button--outline" href="#">Read more</a></div></div></div>
<div class="section"><div class="page-width"><div class="section-header section-header--center"><h2 class="h2">Kind words</h2></div><ul class="quotes" role="list"><li class="quote card"><blockquote><p class="quote__text">Beautifully packed and even prettier in person.</p><footer class="quote__author">A happy customer</footer></blockquote></li><li class="quote card"><blockquote><p class="quote__text">My new favourite little shop. Everything feels considered.</p><footer class="quote__author">Repeat customer</footer></blockquote></li><li class="quote card"><blockquote><p class="quote__text">Arrived fast and wrapped like a gift.</p><footer class="quote__author">Verified buyer</footer></blockquote></li></ul></div></div>
</main>
<div class="section newsletter"><div class="page-width newsletter__inner"><h2 class="h2">Join the list</h2><div class="rte newsletter__text"><p>New arrivals, little stories and the occasional treat.</p></div><form class="newsletter__form"><div class="inline-field"><input class="field" type="email" placeholder="Email address"><button class="button" type="button">Subscribe</button></div></form></div></div>
<footer class="site-footer"><div class="page-width"><div class="site-footer__grid"><div><h2 class="site-footer__heading">About us</h2><p>Tell customers what makes your shop special.</p></div><div><h2 class="site-footer__heading">Shop</h2><ul class="site-footer__links" role="list"><li><a href="#">Search</a></li><li><a href="#">Shipping</a></li><li><a href="#">Contact</a></li></ul></div></div>
<div class="site-footer__bottom"><p>&copy; 2026 Your Store &middot; Powered by Shopify</p><p class="site-footer__credit">Theme by <a href="https://prettythingsonline.com">Pretty Things Online</a></p></div></div></footer>
</body></html>'''
    fn=f'/tmp/claude-0/preview/{key}{"-"+preset.lower().replace(" ","-") if preset else ""}.html'
    open(fn,'w').write(html); return fn
for k in ['petalpost','zapline','stillroom']:
    data=json.load(open(f'{OUT}/{k}/config/settings_data.json'))
    for p in data['presets']: print(page(k,p))
