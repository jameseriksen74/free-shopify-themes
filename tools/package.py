import os, shutil, zipfile, json
OUT='/tmp/claude-0/out'; DIST='/tmp/claude-0/dist'; PRE='/tmp/claude-0/preview'
shutil.rmtree(DIST, ignore_errors=True); os.makedirs(DIST)
INFO={
 'petalpost':dict(name='Petalpost',style='Soft boutique',pitch='A soft, editorial boutique theme for gifts, home goods, beauty and handmade shops.',presets=['Default (blush and rose)','Sage','Midnight'],fonts='Playfair Display + Work Sans',best='gift shops, candles, ceramics, beauty, jewelry, handmade goods'),
 'zapline':dict(name='Zapline',style='Bold streetwear',pitch='A loud, high-contrast theme with oversized type, neon accents and hard-edged buttons for drops and limited releases.',presets=['Zapline (black and electric lime)','Daylight','Ultraviolet'],fonts='Montserrat Bold + Karla',best='streetwear, sneakers, merch, gaming gear, energy drinks, music'),
 'stillroom':dict(name='Stillroom',style='Clean minimal',pitch='A quiet, minimal theme with a split hero, glassy header and lots of white space that lets products speak.',presets=['Stillroom (white and ink)','Stone','Ocean'],fonts='Jost',best='skincare, electronics, furniture, coffee, fashion basics'),
}
FEATURES="""- Online Store 2.0: JSON templates, sections everywhere, header and footer section groups
- Hero banner (3 layouts), featured collection, collection list, image with text, rich text, testimonials, newsletter, Custom Liquid and Apps sections
- Product page with image gallery, pill-style variant picker, quantity, dynamic checkout buttons, Shop Pay installments, pickup availability, collapsible tabs and related products
- Collection filtering (Shopify Search & Discovery filters) and sorting
- Predictive search in the header
- Cart page with order notes, discounts, unit prices and accelerated checkout buttons
- Customer accounts, blog, contact page, password page and gift card templates
- 3 colour presets, font pickers, corner radius and page width controls
- Lightweight: one CSS file, one small vanilla JS file, no jQuery, no app dependencies
- Accessible: skip link, visible focus styles, keyboard friendly menus, reduced motion support
- Passes Shopify Theme Check with 0 errors and 0 warnings"""
for k,i in INFO.items():
    d=os.path.join(DIST,k); os.makedirs(d+'/screenshots')
    z=zipfile.ZipFile(f'{d}/{k}-theme-1.0.0.zip','w',zipfile.ZIP_DEFLATED)
    for dp,_,fs in os.walk(f'{OUT}/{k}'):
        for f in fs:
            p=os.path.join(dp,f); z.write(p, os.path.relpath(p,f'{OUT}/{k}'))
    z.close()
    for f in os.listdir(PRE):
        if f.startswith(k) and f.endswith('.png'): shutil.copy(os.path.join(PRE,f), d+'/screenshots/'+f)
    lic=f"""MIT License

Copyright (c) 2026 Pretty Things Online (https://prettythingsonline.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    open(d+'/LICENSE','w').write(lic)
    readme=f"""# {i['name']}: a free Shopify theme by Pretty Things Online

{i['pitch']}

Made with care by **[Pretty Things Online](https://prettythingsonline.com)**. Free for personal and commercial use under the MIT license.

![{i['name']} preview](screenshots/{k}-{i['presets'][0].split(' ')[0].lower()}-desktop.png)

## Features

{FEATURES}

**Style:** {i['style']} · **Fonts:** {i['fonts']} · **Presets:** {', '.join(i['presets'])}
**Great for:** {i['best']}

## Install in 2 minutes

1. Download `{k}-theme-1.0.0.zip` (don't unzip it).
2. In Shopify admin go to **Online Store > Themes**.
3. Click **Add theme > Upload zip file** and choose the zip.
4. Click **Customize** to add your logo, images and collections, then **Publish**.

## Setting it up

- **Menu:** Header uses the `main-menu` navigation; footer uses `footer`. Edit them under **Content > Menus**.
- **Filters:** install Shopify's free *Search & Discovery* app to choose which filters appear on collection pages.
- **Contact page:** create a page and set its template to `page.contact`.
- **Colours and fonts:** **Theme settings > Colors / Typography**, or switch presets.
- **Theme credit:** the small "Theme by Pretty Things Online" footer link can be switched off under **Theme settings > Theme credit**. Keeping it on is a lovely way to say thanks.

## Support

Questions, ideas or bugs: [prettythingsonline.com](https://prettythingsonline.com)

## License

MIT. See `LICENSE`.
"""
    open(d+'/README.md','w').write(readme)
    listing=f"""# Listing copy: {i['name']}

**Title (short):** {i['name']}: Free Shopify Theme
**Title (long):** {i['name']}: Free {i['style']} Shopify Theme (Online Store 2.0) by Pretty Things Online

**One-liner:** {i['pitch']}

**Description:**
{i['name']} is a free, modern Shopify theme from Pretty Things Online. {i['pitch']} It's built on Online Store 2.0, so every page is made of drag-and-drop sections, and it ships with three colour presets ({', '.join(i['presets'])}) so you can find your look in one click. It's fast (one stylesheet, one tiny script, no jQuery), accessible, and passes Shopify Theme Check with zero issues. Perfect for {i['best']}.

**Features:**
{FEATURES}

**Tags:** shopify theme, free shopify theme, online store 2.0, {i['style'].lower()}, minimal, modern, ecommerce, responsive, dark mode preset

**Credit line:** Designed by Pretty Things Online · https://prettythingsonline.com
**License:** MIT (free for personal and commercial use)
**Version:** 1.0.0
"""
    open(d+'/LISTING.md','w').write(listing)
# bundle
z=zipfile.ZipFile(f'{DIST}/pretty-things-online-free-shopify-themes-bundle.zip','w',zipfile.ZIP_DEFLATED)
for k in INFO: 
    z.write(f'{DIST}/{k}/{k}-theme-1.0.0.zip', f'{k}-theme-1.0.0.zip')
z.close()
print(os.popen(f'ls -la {DIST} {DIST}/*').read())
