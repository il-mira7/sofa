#!/usr/bin/env python3
"""
Farfale Living Georgia — Multi-language Static Site Generator (SEO Optimized)
Generates physical HTML files for KA (Georgian), RU (Russian), and EN (English).
Includes ALL visual, atmospheric sections:
1. Hero with background video and trust badges
2. Sticky Categories bar & Catalog grid
3. Quality & Sofa Anatomy (3D exploded view with Georgian annotations)
4. Tactile Macro Gallery (seams, bouclé, corduroy close-ups)
5. Bespoke 4-Step Order Process
6. Real Customer Interiors / Instagram Showcase
7. Flagship Vake Showroom Showcase
8. FAQ Accordion with Schema.org FAQPage
9. Consultation & WhatsApp lead form
10. Product Quick-View Modal with photo gallery
11. Dedicated SEO Subpages: /tbilisi-showroom.html, /delivery-georgia.html, /products/*.html
"""

import os
import json
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://farfale.ge"
LASTMOD = date.today().isoformat()

# Load data
with open(os.path.join(BASE_DIR, 'data/site.json'), encoding='utf-8') as f:
    site_data = json.load(f)

with open(os.path.join(BASE_DIR, 'data/products.json'), encoding='utf-8') as f:
    products_raw = json.load(f)

with open(os.path.join(BASE_DIR, 'data/showrooms.json'), encoding='utf-8') as f:
    showrooms_data = json.load(f)

with open(os.path.join(BASE_DIR, 'data/portfolio.json'), encoding='utf-8') as f:
    portfolio_data = json.load(f)

with open(os.path.join(BASE_DIR, 'data/translations.json'), encoding='utf-8') as f:
    translations = json.load(f)

with open(os.path.join(BASE_DIR, 'data/blog.json'), encoding='utf-8') as f:
    blog_data = json.load(f)

products = products_raw['all']['products']
LANGS = ['ka', 'ru', 'en']

OG_LOCALES = {"ka": "ka_GE", "ru": "ru_RU", "en": "en_US"}

def favicon_links(depth=0):
    p = "../" * depth if depth > 0 else ""
    return (
        f'  <link rel="icon" href="{p}assets/icons/favicon-96.png" type="image/png" sizes="96x96">\n'
        f'  <link rel="icon" href="{p}assets/icons/favicon-48.png" type="image/png" sizes="48x48">\n'
        f'  <link rel="apple-touch-icon" href="{p}assets/icons/apple-touch-icon.png">'
    )

def social_meta(lang, title, desc, image_url, page_url):
    alts = "".join(
        f'\n  <meta property="og:locale:alternate" content="{OG_LOCALES[l]}">'
        for l in LANGS if l != lang
    )
    return (
        f'  <meta property="og:image" content="{image_url}">\n'
        f'  <meta property="og:url" content="{page_url}">\n'
        f'  <meta property="og:locale" content="{OG_LOCALES[lang]}">{alts}\n'
        f'  <meta name="twitter:card" content="summary_large_image">\n'
        f'  <meta name="twitter:title" content="{title}">\n'
        f'  <meta name="twitter:description" content="{desc}">\n'
        f'  <meta name="twitter:image" content="{image_url}">'
    )

def format_date(iso, lang):
    months = {
        "ka": ["იან", "თებ", "მარ", "აპრ", "მაი", "ივნ", "ივლ", "აგვ", "სექ", "ოქტ", "ნოე", "დეკ"],
        "ru": ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"],
        "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    }
    y, m, d = iso.split("-")
    m = int(m)
    if lang == "en":
        return f"{months[lang][m-1]} {int(d)}, {y}"
    return f"{int(d)} {months[lang][m-1]} {y}"

def get_i18n(val, lang, default=""):
    if isinstance(val, dict):
        return val.get(lang, val.get("ru", default))
    return val if val is not None else default

def get_hreflang_tags(page_path):
    lines = []
    for l in LANGS:
        url = f"{DOMAIN}/{l}/{page_path}" if page_path else f"{DOMAIN}/{l}/"
        lines.append(f'  <link rel="alternate" hreflang="{l}" href="{url}">')
    default_url = f"{DOMAIN}/ka/{page_path}" if page_path else f"{DOMAIN}/ka/"
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="{default_url}">')
    return "\n".join(lines)

def get_header(lang, current_page="", depth=0):
    t = translations[lang]
    prefix = "../" * depth if depth > 0 else ""
    home_url = f"{prefix}{lang}/index.html" if depth > 0 else f"{lang}/index.html"
    if depth == 0 and lang == "ru":
        home_url = "index.html"
    
    def get_lang_url(target_lang):
        if depth == 0:
            return f"{target_lang}/index.html"
        return f"{prefix}{target_lang}/{current_page}" if current_page else f"{prefix}{target_lang}/index.html"

    lang_links = []
    for l in ['KA', 'RU', 'EN']:
        code = l.lower()
        if code == lang:
            lang_links.append(f'<span class="lang-opt active">{l}</span>')
        else:
            lang_links.append(f'<a href="{get_lang_url(code)}" class="lang-opt">{l}</a>')
    lang_switcher = '<span class="lang-sep">/</span>'.join(lang_links)

    wa_phone = site_data['contacts']['phoneRaw']
    wa_text = "გამარჯობა! დივნის შეკვეთა მინდა" if lang == 'ka' else ("Hello! I would like to inquire about a custom sofa" if lang == 'en' else "Здравствуйте! Хочу получить консультацию по диванам")

    showroom_url = f"{prefix}{lang}/tbilisi-showroom.html" if depth > 0 else f"{lang}/tbilisi-showroom.html"
    delivery_url = f"{prefix}{lang}/delivery-georgia.html" if depth > 0 else f"{lang}/delivery-georgia.html"

    return f"""
  <!-- Top Announcement Bar -->
  <div class="top-bar">
    <div class="container top-bar__inner">
      <span class="top-bar__text">{t['topBar']}</span>
      <div class="top-bar__links">
        <a href="{showroom_url}" class="top-bar__link">{t['nav']['showroom']}</a>
        <span class="top-bar__sep">•</span>
        <a href="{delivery_url}" class="top-bar__link">{t['nav']['delivery']}</a>
        <span class="top-bar__sep">•</span>
        <a href="https://wa.me/{wa_phone}?text={wa_text}" target="_blank" rel="noopener" class="top-bar__link">WhatsApp</a>
      </div>
    </div>
  </div>

  <!-- Header -->
  <header class="header" id="header">
    <div class="header__main">
      <div class="container header__inner">
        <div class="header__left">
          <a href="{home_url}" class="logo" aria-label="Farfale">
            <img src="{prefix}assets/images/logo/farfale-logo.jpg" alt="Farfale" class="logo__img">
          </a>
          <nav class="header__desktop-menu" aria-label="Navigation">
            <a href="{home_url}#catalog" class="nav-link">{t['nav']['catalog']}</a>
            <a href="{home_url}#quality" class="nav-link">{t['nav']['quality']}</a>
            <a href="{home_url}#process" class="nav-link">{t['nav']['process']}</a>
            <a href="{home_url}#portfolio" class="nav-link">{t['nav']['portfolio']}</a>
            <a href="{showroom_url}" class="nav-link">{t['nav']['showroom']}</a>
            <a href="{delivery_url}" class="nav-link">{t['nav']['delivery']}</a>
            <a href="{home_url}#contacts" class="nav-link">{t['nav']['contacts']}</a>
          </nav>
        </div>

        <div class="header__actions">
          <div class="lang-switch">
            {lang_switcher}
          </div>
          <a href="https://wa.me/{wa_phone}?text={wa_text}" target="_blank" rel="noopener" class="header__social-btn btn--wa-head">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
            </svg>
            <span>WhatsApp</span>
          </a>
          <button class="burger-btn" id="mobileDrawerBtn" aria-label="Open menu" type="button">
            <span class="burger-line"></span>
            <span class="burger-line"></span>
            <span class="burger-line"></span>
          </button>
        </div>
      </div>
    </div>
  </header>

  <!-- Mobile Menu Drawer -->
  <div class="mobile-menu" id="mobileDrawer">
    <div class="mobile-menu__backdrop" id="closeDrawerBackdrop"></div>
    <div class="mobile-menu__content">
      <div class="mobile-menu__top">
        <a href="{home_url}" class="logo" aria-label="Farfale">
          <img src="{prefix}assets/images/logo/farfale-logo.jpg" alt="Farfale" class="logo__img">
        </a>
        <button class="close-btn" id="closeDrawerBtn" aria-label="Close menu">&times;</button>
      </div>

      <div class="lang-switch" style="margin-bottom: 24px; font-size: 0.95rem;">
        {lang_switcher}
      </div>

      <nav class="mobile-menu__nav">
        <a href="{home_url}#catalog" class="mobile-nav-link">{t['nav']['catalog']}</a>
        <a href="{home_url}#quality" class="mobile-nav-link">{t['nav']['quality']}</a>
        <a href="{home_url}#process" class="mobile-nav-link">{t['nav']['process']}</a>
        <a href="{home_url}#portfolio" class="mobile-nav-link">{t['nav']['portfolio']}</a>
        <a href="{showroom_url}" class="mobile-nav-link" style="color: #bda27e; font-weight: 600;">{t['nav']['showroom']}</a>
        <a href="{delivery_url}" class="mobile-nav-link">{t['nav']['delivery']}</a>
        <a href="{home_url}#contacts" class="mobile-nav-link">{t['nav']['contacts']}</a>
      </nav>

      <div class="mobile-menu__footer">
        <div style="font-size: 0.85rem; color: #666; margin-bottom: 12px; line-height: 1.4;">
          <strong>{t.get('footerAddress', {}).get('main', 'ვაკე, თბილისი, ნ. ბერძენიშვილის ქუჩა 2')}</strong><br>
          <span style="color: #999;">{t.get('footerAddress', {}).get('sub', 'Vake, Tbilisi N. Berdzenishvili 2')}</span>
        </div>
        <a href="https://wa.me/{wa_phone}?text={wa_text}" target="_blank" rel="noopener" class="btn btn--whatsapp btn--full" style="text-align: center; justify-content: center;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
          </svg>
          WhatsApp
        </a>
      </div>
    </div>
  </div>
  <script>
    (function() {{
      const b = document.getElementById('mobileDrawerBtn');
      const d = document.getElementById('mobileDrawer');
      const c = document.getElementById('closeDrawerBtn');
      const bk = document.getElementById('closeDrawerBackdrop');
      if (b && d) {{
        b.onclick = () => {{ d.classList.add('open'); document.body.style.overflow = 'hidden'; }};
        if (c) c.onclick = () => {{ d.classList.remove('open'); document.body.style.overflow = ''; }};
        if (bk) bk.onclick = () => {{ d.classList.remove('open'); document.body.style.overflow = ''; }};
        d.querySelectorAll('.mobile-nav-link').forEach(l => {{
          l.onclick = () => {{ d.classList.remove('open'); document.body.style.overflow = ''; }};
        }});
      }}
    }})();
  </script>
"""

def get_footer(lang, depth=0):
    t = translations[lang]
    prefix = "../" * depth if depth > 0 else ""
    home_url = f"{prefix}{lang}/index.html" if depth > 0 else f"{lang}/index.html"
    showroom_url = f"{prefix}{lang}/tbilisi-showroom.html" if depth > 0 else f"{lang}/tbilisi-showroom.html"
    delivery_url = f"{prefix}{lang}/delivery-georgia.html" if depth > 0 else f"{lang}/delivery-georgia.html"
    prod_prefix = f"{prefix}{lang}/products" if depth > 0 else f"{lang}/products"
    
    addr_main = t.get('footerAddress', {}).get('main', 'Тбилиси, Ваке, ул. Н. Бердзенишвили 2')
    addr_sub = t.get('footerAddress', {}).get('sub', 'ვაკე, თბილისი, ნ. ბერძენიშვილის ქუჩა 2')

    return f"""
  <!-- Footer -->
  <footer class="footer" id="contacts">
    <div class="container footer__inner">
      <div class="footer__col footer__col--brand">
        <span class="footer__brand-title">farfale</span>
        <p class="footer__slogan">Cool & Comfy. Style Comfort Durability.<br>Custom-Made Sofas Crafted for Your Space.</p>
        <div class="footer__address-line">
          <strong>{addr_main}</strong><br>
          <span style="font-size: 0.85rem; color: #888;">{addr_sub}</span>
        </div>
        <div class="footer__socials">
          <a href="https://www.instagram.com/farfale.ge" target="_blank" rel="noopener" class="footer__soc-link">Instagram</a>
          <a href="{site_data['contacts']['whatsapp']}" target="_blank" rel="noopener" class="footer__soc-link">WhatsApp</a>
          <a href="{site_data['contacts']['telegram']}" target="_blank" rel="noopener" class="footer__soc-link">Telegram</a>
        </div>
      </div>

      <div class="footer__col">
        <h4 class="footer__heading">{t['nav']['catalog']}</h4>
        <ul class="footer__links">
          <li><a href="{prod_prefix}/cloud.html">Cloud Lounge</a></li>
          <li><a href="{prod_prefix}/curve.html">Curve Organic</a></li>
          <li><a href="{prod_prefix}/nordic.html">Nordic Minimal</a></li>
          <li><a href="{prod_prefix}/bellini.html">Bellini Tufted</a></li>
          <li><a href="{prod_prefix}/daybed.html">Daybed Slumber</a></li>
        </ul>
      </div>

      <div class="footer__col">
        <h4 class="footer__heading">{t['nav']['showroom']} & SEO</h4>
        <ul class="footer__links">
          <li><a href="{showroom_url}">{t['nav']['showroom']}</a></li>
          <li><a href="{delivery_url}">{t['nav']['delivery']}</a></li>
          <li><a href="{home_url}#quality">{t['nav']['quality']}</a></li>
          <li><a href="{home_url}#portfolio">{t['nav']['portfolio']}</a></li>
          <li><a href="{home_url}#process">{t['nav']['process']}</a></li>
        </ul>
      </div>

      <div class="footer__col footer__col--contacts">
        <h4 class="footer__heading">{t['nav']['contacts']}</h4>
        <p class="footer__contact-item">
          <strong>{site_data['contacts']['phone']}</strong>
        </p>
        <p class="footer__contact-item">
          <a href="mailto:{site_data['contacts']['email']}" style="color: inherit;">{site_data['contacts']['email']}</a>
        </p>
        <p class="footer__contact-item">
          {site_data['contacts']['hoursWeekdays']}
        </p>
        <p class="footer__contact-item">
          {site_data['contacts']['address']}
        </p>
      </div>
    </div>

    <div class="footer__bottom">
      <div class="container footer__bottom-inner">
        <span>© 2026 Farfale Living Georgia. All rights reserved.</span>
        <span>Custom-made sofas & soft furniture in Tbilisi, Georgia</span>
      </div>
    </div>
  </footer>
"""

def generate_homepage(lang, depth=1):
    t = translations[lang]
    prefix = "../" * depth if depth > 0 else ""
    curr_url = f"{DOMAIN}/{lang}/" if depth > 0 else f"{DOMAIN}/"
    hreflangs = get_hreflang_tags("")

    # FAQ Schema
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["a"]
                }
            } for item in t["faq"]["items"]
        ]
    }

    # LocalBusiness Schema
    local_schema = {
        "@context": "https://schema.org",
        "@type": "FurnitureStore",
        "name": "Farfale Living Georgia",
        "image": f"{DOMAIN}/assets/images/hero/hero-poster.webp",
        "logo": f"{DOMAIN}/assets/icons/favicon-512.png",
        "telephone": site_data['contacts']['phoneRaw'],
        "email": site_data['contacts']['email'],
        "url": curr_url,
        "priceRange": "3600 - 15000 GEL",
        "currenciesAccepted": "GEL",
        "sameAs": [
            site_data['contacts']['instagram'],
            site_data['contacts']['telegram'],
            site_data['contacts']['whatsapp']
        ],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "N. Berdzenishvili 2",
            "addressLocality": "Tbilisi",
            "addressRegion": "Vake",
            "postalCode": "0179",
            "addressCountry": "GE"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 41.7118,
            "longitude": 44.7578
        },
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                "opens": "11:00",
                "closes": "20:00"
            }
        ]
    }

    # Product cards
    cards_html = []
    for p in products:
        p_url = f"{prefix}{lang}/products/{p['slug']}.html" if depth > 0 else f"{lang}/products/{p['slug']}.html"
        cat_name = get_i18n(p['categoryName'], lang)
        badge = get_i18n(p['badge'], lang)
        tagline = get_i18n(p['tagline'], lang)
        price_gel = get_i18n(p['price_formatted_gel'], lang)
        lead_time = get_i18n(p['lead_time'], lang)
        cards_html.append(f"""
        <a href="{p_url}" class="product-card">
          <div class="product-card__img-box">
            <img src="{prefix}{p['images'][0]}" alt="{p['title']}" class="product-card__img" loading="lazy">
            <span class="product-card__tag-badge">{badge}</span>
            <span class="product-card__quick-btn">
              {t['hero']['ctaModels']} →
            </span>
          </div>
          <div class="product-card__info">
            <div class="product-card__header-line">
              <h3 class="product-card__title">{p['title']}</h3>
              <span class="product-card__cat-label">{cat_name}</span>
            </div>
            <p class="product-card__tagline-short">{tagline}</p>
            <div class="product-card__meta">
              <span class="product-card__price">{price_gel}</span>
              <span class="product-card__badge">{lead_time}</span>
            </div>
          </div>
        </a>
        """)

    # Portfolio cards (Real interiors)
    portfolio_cards_html = []
    for proj in portfolio_data['projects']:
        proj_title = get_i18n(proj['title'], lang)
        proj_model = get_i18n(proj['model'], lang)
        proj_loc = get_i18n(proj['location'], lang)
        portfolio_cards_html.append(f"""
        <div class="portfolio-card">
          <img src="{prefix}{proj['image']}" alt="{proj_title} — {proj_model}" loading="lazy">
          <div class="portfolio-card__overlay">
            <span class="portfolio-card__tag">{proj_loc}</span>
            <h3 class="portfolio-card__title">{proj_title}</h3>
            <p class="portfolio-card__meta">{proj_model}</p>
          </div>
        </div>
        """)

    # Journal cards (own news, cases & guides — GEO content)
    journal_cards_html = []
    for item in blog_data[:6]:
        j_title = get_i18n(item['title'], lang)
        j_descr = get_i18n(item['descr'], lang)
        journal_cards_html.append(f"""
        <article style="background: #ffffff; border: 1px solid var(--color-border); border-radius: var(--radius-lg); overflow: hidden;">
          <img src="{prefix}{item['image']}" alt="{j_title}" style="width: 100%; height: 200px; object-fit: cover; display: block;" loading="lazy">
          <div style="padding: 20px 22px;">
            <time datetime="{item['date']}" style="font-size: 0.78rem; letter-spacing: 0.6px; text-transform: uppercase; color: var(--color-text-muted);">{format_date(item['date'], lang)}</time>
            <h3 style="margin: 10px 0; font-size: 1.05rem; line-height: 1.35;">{j_title}</h3>
            <p style="font-size: 0.9rem; line-height: 1.6; color: var(--color-text-muted); margin: 0;">{j_descr}</p>
          </div>
        </article>
        """)

    # FAQ HTML
    faq_items_html = []
    for item in t["faq"]["items"]:
        faq_items_html.append(f"""
          <div class="faq-item">
            <button class="faq-question" type="button">
              <span>{item['q']}</span>
              <span class="faq-icon">+</span>
            </button>
            <div class="faq-answer">
              <p>{item['a']}</p>
            </div>
          </div>
        """)

    showroom_url = f"{prefix}{lang}/tbilisi-showroom.html" if depth > 0 else f"{lang}/tbilisi-showroom.html"

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t['siteTitle']}</title>
  <meta name="description" content="{t['siteDesc']}">
  <meta name="keywords" content="{t['siteKeywords']}">
  <link rel="canonical" href="{curr_url}">
{hreflangs}
  <meta name="geo.region" content="GE">
  <meta name="geo.placename" content="Tbilisi, Vake">
  <meta name="geo.position" content="41.7118;44.7578">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{t['siteTitle']}">
  <meta property="og:description" content="{t['siteDesc']}">
{social_meta(lang, t['siteTitle'], t['siteDesc'], f"{DOMAIN}/assets/images/hero/hero-poster.webp", curr_url)}
{favicon_links(depth)}
  <link rel="preload" as="image" href="{prefix}assets/images/hero/hero-poster.webp" fetchpriority="high">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}styles/main.css">
  <script type="application/ld+json">
{json.dumps(local_schema, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
{json.dumps(faq_schema, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
{get_header(lang, "", depth=depth)}

  <!-- 1. Hero Section -->
  <section class="hero" id="hero">
    <div class="hero__video-wrapper">
      <video class="hero__video" autoplay loop muted playsinline preload="metadata" poster="{prefix}assets/images/hero/hero-poster.webp">
        <source src="{prefix}assets/images/hero/hero-video.mp4" type="video/mp4">
      </video>
      <div class="hero__overlay"></div>
    </div>
    <div class="container hero__content">
      <span class="hero__badge">{t['hero']['badge']}</span>
      <h1 class="hero__title">{t['hero']['title']}</h1>
      <p class="hero__subtitle">{t['hero']['subtitle']}</p>
      <div class="hero__actions">
        <a href="#catalog" class="btn btn--hero">{t['hero']['ctaModels']}</a>
        <a href="{showroom_url}" class="btn btn--outline-hero">{t['hero']['ctaShowroom']}</a>
        <a href="https://wa.me/{site_data['contacts']['phoneRaw']}?text={t['hero']['ctaWhatsApp']}" target="_blank" rel="noopener" class="btn btn--whatsapp-hero">
          {t['hero']['ctaWhatsApp']}
        </a>
      </div>
      <div class="hero__stats">
        <div class="hero__stat-item">
          <strong>5 {t['hero']['statWarranty'].split()[1] if len(t['hero']['statWarranty'].split())>1 else ''}</strong>
          <span>{t['hero']['statWarranty']}</span>
        </div>
        <div class="hero__stat-item">
          <strong>{t['hero']['statTime']}</strong>
          <span>{t['hero']['statCustom']}</span>
        </div>
        <div class="hero__stat-item">
          <strong>100+</strong>
          <span>{t['hero']['statFabrics']}</span>
        </div>
        <div class="hero__stat-item">
          <strong>Vake</strong>
          <span>Berdzenishvili 2</span>
        </div>
      </div>
    </div>
  </section>

  <!-- 2. Catalog Section -->
  <section class="section catalog-section" id="catalog">
    <div class="container">
      <div class="section-header">
        <div>
          <h2 class="section-title">{t['nav']['catalog']}</h2>
          <span class="section-count">{len(products)} {t['hero']['ctaModels'].lower()}</span>
        </div>
        <div class="catalog-controls">
          <span class="catalog-hint">{t['hero']['statTime']} • GEL (₾)</span>
        </div>
      </div>
      <div class="products-grid">
        {"".join(cards_html)}
      </div>
    </div>
  </section>

  <!-- 3. Quality & Sofa Anatomy Section -->
  <section class="quality-section" id="quality">
    <div class="container">
      <div class="section-header" style="text-align: center; margin-bottom: 56px;">
        <span class="consult-tag" style="margin: 0 auto 12px auto;">{t['quality']['badge']}</span>
        <h2 class="section-title" style="font-size: 2.2rem;">{t['quality']['title']}</h2>
        <p class="section-subtitle" style="max-width: 720px; margin: 12px auto 0 auto; color: var(--color-text-muted);">
          {t['quality']['subtitle']}
        </p>
      </div>

      <div class="quality-grid">
        <div class="quality-scheme__box">
          <img src="{prefix}assets/images/quality/anatomy-sofa-ge.webp" alt="{t['quality']['title']}" class="quality-scheme__img" loading="lazy">
          <div class="quality-scheme__caption">
            <span>{t['quality']['schemeCaption']}</span>
          </div>
        </div>

        <div class="quality-features">
          <div class="quality-feature-card">
            <span class="quality-feature-num">01</span>
            <div class="quality-feature-body">
              <h3>{t['quality']['f1Title']}</h3>
              <p>{t['quality']['f1Desc']}</p>
            </div>
          </div>
          <div class="quality-feature-card">
            <span class="quality-feature-num">02</span>
            <div class="quality-feature-body">
              <h3>{t['quality']['f2Title']}</h3>
              <p>{t['quality']['f2Desc']}</p>
            </div>
          </div>
          <div class="quality-feature-card">
            <span class="quality-feature-num">03</span>
            <div class="quality-feature-body">
              <h3>{t['quality']['f3Title']}</h3>
              <p>{t['quality']['f3Desc']}</p>
            </div>
          </div>
          <div class="quality-feature-card">
            <span class="quality-feature-num">04</span>
            <div class="quality-feature-body">
              <h3>{t['quality']['f4Title']}</h3>
              <p>{t['quality']['f4Desc']}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 4. Tactile Macro Gallery (Close-ups of textures & seams) -->
      <div class="tactile-heading">
        <h3>{t['tactile']['title']}</h3>
        <p>{t['tactile']['subtitle']}</p>
      </div>
      <div class="tactile-grid">
        <div class="tactile-item">
          <img src="{prefix}assets/images/quality/texture-touch-01.webp" alt="{t['tactile']['t1']}" loading="lazy">
          <span class="tactile-label">{t['tactile']['t1']}</span>
        </div>
        <div class="tactile-item">
          <img src="{prefix}assets/images/quality/texture-touch-02.webp" alt="{t['tactile']['t2']}" loading="lazy">
          <span class="tactile-label">{t['tactile']['t2']}</span>
        </div>
        <div class="tactile-item">
          <img src="{prefix}assets/images/quality/texture-craft-01.webp" alt="{t['tactile']['t3']}" loading="lazy">
          <span class="tactile-label">{t['tactile']['t3']}</span>
        </div>
        <div class="tactile-item">
          <img src="{prefix}assets/images/quality/texture-craft-04.webp" alt="{t['tactile']['t4']}" loading="lazy">
          <span class="tactile-label">{t['tactile']['t4']}</span>
        </div>
      </div>

    </div>
  </section>

  <!-- 5. How to Order Process -->
  <section class="process-section" id="process">
    <div class="container">
      <div class="section-header" style="text-align: center;">
        <span class="consult-tag" style="margin: 0 auto 12px auto;">{t['process']['badge']}</span>
        <h2 class="section-title">{t['process']['title']}</h2>
        <p class="section-subtitle" style="color: var(--color-text-muted);">{t['process']['subtitle']}</p>
      </div>
      <div class="process-grid">
        <div class="process-card">
          <div class="process-step-num">01</div>
          <h3>{t['process']['s1Title']}</h3>
          <p>{t['process']['s1Desc']}</p>
        </div>
        <div class="process-card">
          <div class="process-step-num">02</div>
          <h3>{t['process']['s2Title']}</h3>
          <p>{t['process']['s2Desc']}</p>
        </div>
        <div class="process-card">
          <div class="process-step-num">03</div>
          <h3>{t['process']['s3Title']}</h3>
          <p>{t['process']['s3Desc']}</p>
        </div>
        <div class="process-card">
          <div class="process-step-num">04</div>
          <h3>{t['process']['s4Title']}</h3>
          <p>{t['process']['s4Desc']}</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 6. Real Customer Interiors / Instagram Showcase -->
  <section class="portfolio-section" id="portfolio">
    <div class="container">
      <div class="portfolio-header">
        <div>
          <span class="consult-tag">{t['portfolio']['badge']}</span>
          <h2 class="section-title">{t['portfolio']['title']}</h2>
          <p class="section-subtitle" style="color: var(--color-text-muted);">
            {t['portfolio']['subtitle']}
          </p>
        </div>
        <a href="https://www.instagram.com/farfale.ge" target="_blank" rel="noopener" class="portfolio-insta-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
          {t['portfolio']['btn']}
        </a>
      </div>
      <div class="portfolio-grid">
        {"".join(portfolio_cards_html)}
      </div>
    </div>
  </section>

  <!-- 6.5 Journal: own news, cases & guides (GEO content) -->
  <section class="section" id="journal">
    <div class="container">
      <div class="section-header" style="text-align: center; margin-bottom: 40px;">
        <span class="consult-tag" style="margin: 0 auto 12px auto;">{t['journal']['badge']}</span>
        <h2 class="section-title">{t['journal']['title']}</h2>
        <p class="section-subtitle" style="color: var(--color-text-muted);">{t['journal']['subtitle']}</p>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px;">
        {"".join(journal_cards_html)}
      </div>
    </div>
  </section>

  <!-- 7. Flagship Showroom Showcase on Homepage -->
  <section class="section showrooms-section" id="showrooms">
    <div class="container">
      <div class="section-header" style="text-align: center; margin-bottom: 40px;">
        <span class="consult-tag" style="margin: 0 auto 12px auto;">{t['showroomPage']['h1']}</span>
        <h2 class="section-title">{t['showroomPage']['title']}</h2>
        <p class="section-subtitle" style="color: var(--color-text-muted);">
          {t['showroomPage']['address']} • {t['showroomPage']['hours']}
        </p>
      </div>

      <div class="showroom-flagship">
        <div class="showroom-flagship__grid">
          <div class="showroom-flagship__gallery">
            <div class="showroom-main-photo">
              <img src="{prefix}assets/images/showroom/showroom-street.webp" alt="Showroom Farfale Vake" id="homeShImg">
            </div>
            <div class="showroom-thumbs">
              <div class="showroom-thumb-box active" onclick="switchHomeShImg(this, '{prefix}assets/images/showroom/showroom-street.webp')"><img src="{prefix}assets/images/showroom/showroom-street.webp" alt="Showroom exterior"></div>
              <div class="showroom-thumb-box" onclick="switchHomeShImg(this, '{prefix}assets/images/showroom/showroom-comfort.webp')"><img src="{prefix}assets/images/showroom/showroom-comfort.webp" alt="Showroom comfort"></div>
              <div class="showroom-thumb-box" onclick="switchHomeShImg(this, '{prefix}assets/images/showroom/showroom-interior.webp')"><img src="{prefix}assets/images/showroom/showroom-interior.webp" alt="Showroom interior"></div>
              <div class="showroom-thumb-box" onclick="switchHomeShImg(this, '{prefix}assets/images/showroom/showroom-pov.webp')"><img src="{prefix}assets/images/showroom/showroom-pov.webp" alt="Showroom POV"></div>
            </div>
          </div>
          <div class="showroom-flagship__info">
            <span class="showroom-badge">Vake • Tbilisi</span>
            <h3 class="showroom-title">{t['showroomPage']['h1']}</h3>
            <div class="showroom-address-box">
              <div><strong>{t['showroomPage']['address']}</strong></div>
            </div>
            <p class="showroom-desc">{t['showroomPage']['desc']}</p>
            <div class="showroom-details-list">
              <div class="detail-row"><span>🕒</span> <div>{t['showroomPage']['hours']}</div></div>
              <div class="detail-row"><span>🚗</span> <div>{t['showroomPage']['parking']}</div></div>
              <div class="detail-row"><span>🚇</span> <div>{t['showroomPage']['metro']}</div></div>
            </div>
            <div class="showroom-actions">
              <a href="https://wa.me/{site_data['contacts']['phoneRaw']}?text={t['showroomPage']['ctaVisit']}" target="_blank" rel="noopener" class="btn btn--whatsapp">
                {t['showroomPage']['ctaVisit']}
              </a>
              <a href="{showroom_url}" class="btn btn--outline">
                {t['nav']['showroom']} →
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 8. FAQ Section with Schema.org -->
  <section class="faq-section" id="faq">
    <div class="container">
      <div class="section-header" style="text-align: center;">
        <span class="consult-tag" style="margin: 0 auto 12px auto;">FAQ</span>
        <h2 class="section-title">{t['faq']['title']}</h2>
        <p class="section-subtitle" style="color: var(--color-text-muted);">{t['faq']['subtitle']}</p>
      </div>
      <div class="faq-list">
        {"".join(faq_items_html)}
      </div>
    </div>
  </section>

  <!-- 9. Consultation Form -->
  <section class="consult-section" id="consultation">
    <div class="container consult-section__inner">
      <div class="consult-content">
        <span class="consult-tag">{t['consult']['badge']}</span>
        <h2 class="consult-title">{t['consult']['title']}</h2>
        <p class="consult-desc">{t['consult']['desc']}</p>
        <form class="consult-form" onsubmit="event.preventDefault(); window.open('https://wa.me/{site_data['contacts']['phoneRaw']}?text=' + encodeURIComponent('{t['consult']['title']}: ' + this.name.value + ' ' + this.phone.value), '_blank');">
          <div class="form-row">
            <input type="text" name="name" class="form-input" placeholder="{t['consult']['namePlaceholder']}" required>
            <input type="tel" name="phone" class="form-input" placeholder="{t['consult']['phonePlaceholder']}" required>
            <button type="submit" class="btn btn--primary btn--submit">{t['consult']['submitBtn']}</button>
          </div>
          <div class="consult-disclaimer">
            <a href="https://wa.me/{site_data['contacts']['phoneRaw']}" target="_blank" rel="noopener" class="btn--wa-inline">
              {t['consult']['waDirect']}
            </a>
          </div>
        </form>
      </div>
      <div class="consult-image-box">
        <img src="{prefix}assets/images/portfolio/interior-01.webp" alt="Farfale Sofa" class="consult-img" loading="lazy">
      </div>
    </div>
  </section>

{get_footer(lang, depth=depth)}

  <script>
    document.querySelectorAll('.faq-question').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const item = btn.parentElement;
        item.classList.toggle('open');
      }});
    }});

    function switchHomeShImg(box, src) {{
      document.getElementById('homeShImg').src = src;
      box.parentElement.querySelectorAll('.showroom-thumb-box').forEach(b => b.classList.remove('active'));
      box.classList.add('active');
    }}
  </script>
</body>
</html>
"""
    return html

def generate_showroom_page(lang):
    t = translations[lang]
    sp = t['showroomPage']
    curr_url = f"{DOMAIN}/{lang}/tbilisi-showroom.html"
    hreflangs = get_hreflang_tags("tbilisi-showroom.html")

    local_schema = {
        "@context": "https://schema.org",
        "@type": "FurnitureStore",
        "name": f"Farfale Living Showroom — {sp['h1']}",
        "image": f"{DOMAIN}/assets/images/showroom/showroom-street.webp",
        "logo": f"{DOMAIN}/assets/icons/favicon-512.png",
        "telephone": site_data['contacts']['phoneRaw'],
        "email": site_data['contacts']['email'],
        "url": curr_url,
        "sameAs": [
            site_data['contacts']['instagram'],
            site_data['contacts']['telegram'],
            site_data['contacts']['whatsapp']
        ],
        "hasMap": site_data['contacts']['mapUrl'],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "N. Berdzenishvili 2",
            "addressLocality": "Tbilisi",
            "addressRegion": "Vake",
            "postalCode": "0179",
            "addressCountry": "GE"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 41.7118,
            "longitude": 44.7578
        },
        "openingHours": "Mo-Su 11:00-20:00"
    }

    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Farfale",
                "item": f"{DOMAIN}/{lang}/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": sp['h1'],
                "item": curr_url
            }
        ]
    }

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{sp['title']}</title>
  <meta name="description" content="{sp['desc']}">
  <link rel="canonical" href="{curr_url}">
{hreflangs}
  <meta property="og:title" content="{sp['title']}">
  <meta property="og:description" content="{sp['desc']}">
{social_meta(lang, sp['title'], sp['desc'], f"{DOMAIN}/assets/images/showroom/showroom-street.webp", curr_url)}
{favicon_links(1)}
  <link rel="stylesheet" href="../styles/main.css">
  <script type="application/ld+json">
{json.dumps(local_schema, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
{json.dumps(breadcrumb_schema, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
{get_header(lang, "tbilisi-showroom.html", depth=1)}

  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <div class="container">
      <ol class="breadcrumbs__list">
        <li class="breadcrumbs__item"><a href="index.html">Farfale</a></li>
        <li class="breadcrumbs__sep">/</li>
        <li class="breadcrumbs__item active">{t['nav']['showroom']}</li>
      </ol>
    </div>
  </nav>

  <section class="section">
    <div class="container">
      <div class="showroom-flagship">
        <div class="showroom-flagship__grid">
          <div class="showroom-flagship__gallery">
            <div class="showroom-main-photo">
              <img src="../assets/images/showroom/showroom-street.webp" alt="Showroom Farfale Vake" id="shMainImg">
            </div>
            <div class="showroom-thumbs">
              <div class="showroom-thumb-box active" onclick="switchPageShImg(this, '../assets/images/showroom/showroom-street.webp')"><img src="../assets/images/showroom/showroom-street.webp" alt="Showroom exterior"></div>
              <div class="showroom-thumb-box" onclick="switchPageShImg(this, '../assets/images/showroom/showroom-comfort.webp')"><img src="../assets/images/showroom/showroom-comfort.webp" alt="Showroom comfort"></div>
              <div class="showroom-thumb-box" onclick="switchPageShImg(this, '../assets/images/showroom/showroom-interior.webp')"><img src="../assets/images/showroom/showroom-interior.webp" alt="Showroom interior"></div>
              <div class="showroom-thumb-box" onclick="switchPageShImg(this, '../assets/images/showroom/showroom-pov.webp')"><img src="../assets/images/showroom/showroom-pov.webp" alt="Showroom POV"></div>
            </div>
          </div>
          <div class="showroom-flagship__info">
            <span class="showroom-badge">Vake • Tbilisi</span>
            <h1 class="showroom-title">{sp['h1']}</h1>
            <div class="showroom-address-box">
              <div><strong>{sp['address']}</strong></div>
            </div>
            <p class="showroom-desc">{sp['desc']}</p>
            <div class="showroom-details-list">
              <div class="detail-row"><span>🕒</span> <div>{sp['hours']}</div></div>
              <div class="detail-row"><span>🚗</span> <div>{sp['parking']}</div></div>
              <div class="detail-row"><span>🚇</span> <div>{sp['metro']}</div></div>
            </div>
            <div class="showroom-actions">
              <a href="https://wa.me/{site_data['contacts']['phoneRaw']}?text={sp['ctaVisit']}" target="_blank" rel="noopener" class="btn btn--whatsapp">
                {sp['ctaVisit']}
              </a>
              <a href="{site_data['contacts']['mapUrl']}" target="_blank" rel="noopener" class="btn btn--outline">
                {sp['ctaMap']}
              </a>
            </div>
          </div>
        </div>
      </div>

      <div style="margin-top: 48px; border-radius: var(--radius-lg); overflow: hidden; border: 1px solid var(--color-border);">
        <iframe src="https://www.google.com/maps?q=N.%20Berdzenishvili%202%2C%20Tbilisi%2C%20Georgia&z=16&output=embed" width="100%" height="380" style="border: 0; display: block;" loading="lazy" title="Farfale — {sp['address']}" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
    </div>
  </section>

{get_footer(lang, depth=1)}

  <script>
    function switchPageShImg(box, src) {{
      document.getElementById('shMainImg').src = src;
      box.parentElement.querySelectorAll('.showroom-thumb-box').forEach(b => b.classList.remove('active'));
      box.classList.add('active');
    }}
  </script>
</body>
</html>
"""
    return html

def generate_delivery_page(lang):
    t = translations[lang]
    dp = t['deliveryPage']
    curr_url = f"{DOMAIN}/{lang}/delivery-georgia.html"
    hreflangs = get_hreflang_tags("delivery-georgia.html")

    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Farfale",
                "item": f"{DOMAIN}/{lang}/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": dp['h1'],
                "item": curr_url
            }
        ]
    }

    zones_html = []
    for z in dp['zones']:
        zones_html.append(f"""
          <div class="delivery-zone-card">
            <h3 class="delivery-zone-city">{z['city']}</h3>
            <span class="delivery-zone-time">{z['time']}</span>
            <p class="delivery-zone-desc">{z['details']}</p>
          </div>
        """)

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{dp['title']}</title>
  <meta name="description" content="{dp['desc']}">
  <link rel="canonical" href="{curr_url}">
{hreflangs}
  <meta property="og:title" content="{dp['title']}">
  <meta property="og:description" content="{dp['desc']}">
{social_meta(lang, dp['title'], dp['desc'], f"{DOMAIN}/assets/images/hero/hero-poster.webp", curr_url)}
{favicon_links(1)}
  <link rel="stylesheet" href="../styles/main.css">
  <script type="application/ld+json">
{json.dumps(breadcrumb_schema, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
{get_header(lang, "delivery-georgia.html", depth=1)}

  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <div class="container">
      <ol class="breadcrumbs__list">
        <li class="breadcrumbs__item"><a href="index.html">Farfale</a></li>
        <li class="breadcrumbs__sep">/</li>
        <li class="breadcrumbs__item active">{t['nav']['delivery']}</li>
      </ol>
    </div>
  </nav>

  <section class="section">
    <div class="container">
      <div class="section-header" style="text-align: center; max-width: 800px; margin: 0 auto 48px auto;">
        <span class="consult-tag">{t['nav']['delivery']}</span>
        <h1 class="section-title">{dp['h1']}</h1>
        <p class="section-subtitle" style="color: var(--color-text-muted); margin-top: 12px;">{dp['intro']}</p>
      </div>

      <div class="delivery-zones-grid">
        {"".join(zones_html)}
      </div>

      <div class="consult-section" style="margin-top: 60px; border-radius: var(--radius-lg);">
        <div class="consult-content" style="max-width: 700px; margin: 0 auto; text-align: center;">
          <h2 class="consult-title" style="margin-bottom: 12px;">{t['consult']['title']}</h2>
          <p class="consult-desc">{t['consult']['desc']}</p>
          <a href="https://wa.me/{site_data['contacts']['phoneRaw']}?text={dp['title']}" target="_blank" rel="noopener" class="btn btn--whatsapp" style="margin-top: 16px;">
            {t['consult']['waDirect']}
          </a>
        </div>
      </div>
    </div>
  </section>

{get_footer(lang, depth=1)}
</body>
</html>
"""
    return html

def generate_product_page(lang, product):
    t = translations[lang]
    slug = product['slug']
    curr_url = f"{DOMAIN}/{lang}/products/{slug}.html"
    hreflangs = get_hreflang_tags(f"products/{slug}.html")

    cat_name = get_i18n(product['categoryName'], lang)
    badge = get_i18n(product['badge'], lang)
    tagline = get_i18n(product['tagline'], lang)
    price_gel = get_i18n(product['price_formatted_gel'], lang)
    lead_time = get_i18n(product['lead_time'], lang)
    warranty = get_i18n(product['warranty'], lang)
    desc = get_i18n(product['description'], lang)
    features = get_i18n(product['features'], lang)
    dimensions = get_i18n(product['dimensions_standard'], lang)
    fabrics = get_i18n(product['popular_fabrics'], lang)

    prod_t = t.get('productPage', {})
    spec_dim_label = prod_t.get('specDimensions', 'Размеры:')
    spec_warr_label = prod_t.get('specWarranty', 'Гарантия:')
    spec_sh_label = prod_t.get('specShowroom', 'Шоурум:')
    brand_tag = prod_t.get('brandTag', 'FARFALE LIVING • GEORGIA')
    warr_val = prod_t.get('warrantyVal', f'{warranty} официальная гарантия')
    sh_val = prod_t.get('showroomVal', 'Vake, N. Berdzenishvili 2')
    fabrics_label = prod_t.get('fabricsLabel', 'Популярные ткани:')

    product_schema = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": f"Farfale {product['title']}",
        "sku": f"FARF-{slug.upper()}",
        "image": [f"{DOMAIN}/{img}" for img in product['images'][:3]],
        "description": desc,
        "brand": {
            "@type": "Brand",
            "name": "Farfale"
        },
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "GEL",
            "lowPrice": product['price_from_gel'],
            "highPrice": int(product['price_from_gel'] * 2.2),
            "offerCount": 10,
            "offers": {
                "@type": "Offer",
                "url": curr_url,
                "price": product['price_from_gel'],
                "priceCurrency": "GEL",
                "availability": "https://schema.org/PreOrder",
                "itemCondition": "https://schema.org/NewCondition",
                "seller": {
                    "@type": "Organization",
                    "name": "Farfale Living Georgia"
                }
            }
        }
    }

    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Farfale",
                "item": f"{DOMAIN}/{lang}/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": t['nav']['catalog'],
                "item": f"{DOMAIN}/{lang}/#catalog"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": product['title'],
                "item": curr_url
            }
        ]
    }

    thumbs_html = []
    for i, img in enumerate(product['images']):
        active_cls = " active" if i == 0 else ""
        thumbs_html.append(f"""
          <img src="../../{img}" alt="{product['title']} {i+1}" class="modal__thumb{active_cls}" onclick="switchProdImg(this, '../../{img}')">
        """)

    wa_msg = f"გამარჯობა! მაინტერესებს დივანი {product['title']} ჩემი ზომებით" if lang == 'ka' else (f"Hello! I am interested in {product['title']} sofa custom sizes" if lang == 'en' else f"Здравствуйте! Хочу рассчитать стоимость дивана {product['title']} под мои размеры")

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{product['title']} — {t['siteTitle']}</title>
  <meta name="description" content="{desc[:160]}">
  <link rel="canonical" href="{curr_url}">
{hreflangs}
  <meta property="og:title" content="{product['title']} | Farfale Living">
  <meta property="og:description" content="{desc[:160]}">
{social_meta(lang, product['title'], desc[:160], f"{DOMAIN}/{product['images'][0]}", curr_url)}
{favicon_links(2)}
  <link rel="stylesheet" href="../../styles/main.css">
  <script type="application/ld+json">
{json.dumps(product_schema, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
{json.dumps(breadcrumb_schema, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
{get_header(lang, f"products/{slug}.html", depth=2)}

  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <div class="container">
      <ol class="breadcrumbs__list">
        <li class="breadcrumbs__item"><a href="../index.html">Farfale</a></li>
        <li class="breadcrumbs__sep">/</li>
        <li class="breadcrumbs__item"><a href="../index.html#catalog">{t['nav']['catalog']}</a></li>
        <li class="breadcrumbs__sep">/</li>
        <li class="breadcrumbs__item active">{product['title']}</li>
      </ol>
    </div>
  </nav>

  <section class="section">
    <div class="container">
      <div class="modal__grid" style="background: #ffffff; border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: 48px;">
        <div class="modal__gallery">
          <div class="modal__main-box">
            <img src="../../{product['images'][0]}" alt="{product['title']}" class="modal__main-img" id="pMainImg">
            <span class="modal__badge-tag">{badge}</span>
          </div>
          <div class="modal__thumbs" style="margin-top: 16px;">
            {"".join(thumbs_html)}
          </div>
        </div>

        <div class="modal__details">
          <span class="modal__brand">{brand_tag}</span>
          <h1 class="modal__title" style="font-size: 2.2rem;">{product['title']}</h1>
          <p class="modal__tagline">{tagline}</p>
          <div class="modal__price-wrap">
            <span class="modal__price">{price_gel}</span>
            <span class="modal__production-time">{lead_time}</span>
          </div>
          <p class="modal__desc">{desc}</p>
          <ul class="modal__features">
            {''.join([f'<li><span class="feat-bullet">✓</span> {feat}</li>' for feat in features])}
          </ul>
          <div class="modal__fabrics-tag">
            <strong>{fabrics_label}</strong> {', '.join(fabrics)}
          </div>
          <div class="modal__specs">
            <div class="spec-item"><span class="spec-label">{spec_dim_label}</span> <span class="spec-val">{dimensions}</span></div>
            <div class="spec-item"><span class="spec-label">{spec_warr_label}</span> <span class="spec-val">{warr_val}</span></div>
            <div class="spec-item"><span class="spec-label">{spec_sh_label}</span> <span class="spec-val">{sh_val}</span></div>
          </div>
          <div class="modal__actions">
            <a href="https://wa.me/{site_data['contacts']['phoneRaw']}?text={wa_msg}" target="_blank" rel="noopener" class="btn btn--whatsapp btn--full">
              {t['hero']['ctaWhatsApp']}
            </a>
            <a href="../tbilisi-showroom.html" class="btn btn--outline btn--full">
              {t['hero']['ctaShowroom']}
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>

{get_footer(lang, depth=2)}

  <script>
    function switchProdImg(thumb, src) {{
      document.getElementById('pMainImg').src = src;
      document.querySelectorAll('.modal__thumb').forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');
    }}
  </script>
</body>
</html>
"""
    return html

def generate_root_redirect():
    return f"""<!DOCTYPE html>
<html lang="ka">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Farfale — Cool &amp; Comfy | farfale.ge</title>
  <link rel="canonical" href="{DOMAIN}/ka/">
  <link rel="alternate" hreflang="ka" href="{DOMAIN}/ka/">
  <link rel="alternate" hreflang="ru" href="{DOMAIN}/ru/">
  <link rel="alternate" hreflang="en" href="{DOMAIN}/en/">
  <link rel="alternate" hreflang="x-default" href="{DOMAIN}/ka/">
  <meta http-equiv="refresh" content="0; url=ka/">
{favicon_links(0)}
</head>
<body>
  <p style="font-family: sans-serif; text-align: center; margin-top: 20vh;">
    <a href="ka/">Farfale — farfale.ge</a>
  </p>
  <script>
    window.location.replace('ka/');
  </script>
</body>
</html>
"""

def generate_404():
    links = "\n".join(
        f'      <a href="/{l}/" data-lang-link="{l}" style="display: inline-block; margin: 0 14px; padding: 14px 34px; '
        f'border: 1px solid #bda27e; border-radius: 999px; color: #6d5c43; text-decoration: none; '
        f'font-size: 0.95rem; letter-spacing: 1px;">{name}</a>'
        for l, name in [("ka", "ქართული"), ("ru", "Русский"), ("en", "English")]
    )
    return f"""<!DOCTYPE html>
<html lang="ka">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>404 — Farfale | farfale.ge</title>
  <meta name="robots" content="noindex">
{favicon_links(0)}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
</head>
<body style="margin: 0; font-family: 'Montserrat', sans-serif; background: #f4f1ec; color: #3d3833; text-align: center;">
  <div style="max-width: 640px; margin: 0 auto; padding: 18vh 24px 0;">
    <img src="/assets/icons/favicon-192.png" data-farfale-icon alt="Farfale" style="width: 72px; height: 72px; border-radius: 16px;">
    <h1 style="font-size: 4rem; margin: 24px 0 8px; color: #bda27e; font-weight: 300;">404</h1>
    <p style="font-size: 1.05rem; margin: 0 0 8px;">გვერდი ვერ მოიძებნა / Page not found / Страница не найдена</p>
    <p style="font-size: 0.9rem; color: #8a8378; margin: 0 0 40px;">farfale.ge — Cool &amp; Comfy • Vake, Tbilisi</p>
    <nav>
{links}
    </nav>
  </div>
  <script>
    // The custom 404 is served for any URL: rebase language links and the icon
    // onto the deploy subpath (e.g. /sofa/ on GitHub Pages project sites).
    (function() {{
      var seg = location.pathname.split('/').filter(Boolean);
      var base = seg.length > 1 ? '/' + seg[0] : '';
      document.querySelectorAll('[data-lang-link]').forEach(function(a) {{
        a.setAttribute('href', base + '/' + a.getAttribute('data-lang-link') + '/');
      }});
      var icon = document.querySelector('[data-farfale-icon]');
      if (icon) icon.src = base + '/assets/icons/favicon-192.png';
    }})();
  </script>
</body>
</html>
"""

def generate_sitemap(all_urls):
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    
    for path in all_urls:
        for lang in LANGS:
            loc = f"{DOMAIN}/{lang}/{path}" if path else f"{DOMAIN}/{lang}/"
            xml.append('  <url>')
            xml.append(f'    <loc>{loc}</loc>')
            xml.append(f'    <lastmod>{LASTMOD}</lastmod>')
            xml.append('    <changefreq>weekly</changefreq>')
            xml.append('    <priority>0.9</priority>' if path else '    <priority>1.0</priority>')
            for alt_lang in LANGS:
                alt_loc = f"{DOMAIN}/{alt_lang}/{path}" if path else f"{DOMAIN}/{alt_lang}/"
                xml.append(f'    <xhtml:link rel="alternate" hreflang="{alt_lang}" href="{alt_loc}"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}/ka/{path if path else ""}"/>')
            xml.append('  </url>')
            
    xml.append('</urlset>')
    return "\n".join(xml)

def main():
    print("Rebuilding full multi-language static site with all atmospheric sections...")
    
    sitemap_paths = ["", "tbilisi-showroom.html", "delivery-georgia.html"]
    for p in products:
        sitemap_paths.append(f"products/{p['slug']}.html")

    # Generate each language
    for lang in LANGS:
        lang_dir = os.path.join(BASE_DIR, lang)
        prod_dir = os.path.join(lang_dir, "products")
        os.makedirs(prod_dir, exist_ok=True)

        # 1. Homepage with ALL sections
        with open(os.path.join(lang_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(generate_homepage(lang, depth=1))

        # 2. Showroom page
        with open(os.path.join(lang_dir, "tbilisi-showroom.html"), "w", encoding="utf-8") as f:
            f.write(generate_showroom_page(lang))

        # 3. Delivery page
        with open(os.path.join(lang_dir, "delivery-georgia.html"), "w", encoding="utf-8") as f:
            f.write(generate_delivery_page(lang))

        # 4. Product pages
        for p in products:
            with open(os.path.join(prod_dir, f"{p['slug']}.html"), "w", encoding="utf-8") as f:
                f.write(generate_product_page(lang, p))

    # Root index.html: instant redirect to the Georgian homepage (default language)
    with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_root_redirect())

    # 404 page
    with open(os.path.join(BASE_DIR, "404.html"), "w", encoding="utf-8") as f:
        f.write(generate_404())

    # Sitemap
    with open(os.path.join(BASE_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(generate_sitemap(sitemap_paths))

    print("Successfully built all pages with full visual sections restored!")

if __name__ == "__main__":
    main()
