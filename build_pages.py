#!/usr/bin/env python3
"""Trapèze — template v2 generator (websites lane, t_2110cfeb, 2026-11-22).
Copy discipline: only facts verified on the card + the card's own press sources
(CultureMap roundup Nov 2026, the debut write-up, and the February opening piece —
both quote the owners directly). No phone, no prices, no reservation claims —
none published; unknown = omitted. Hours carry an explicit "hours are fluid —
see Instagram" hedge (press's own words); JSON-LD omits openingHours on purpose.
Output: public/*.html + sitemap.xml + robots.txt. Run before `railway up`."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(HERE, "public")
ORIGIN = "https://trapeze-bishop-arts-demo.up.railway.app"
BUILT = "2026-11-22"

NAP_LINE = "240 W 8th St, Dallas, TX 75208"
ADDRESS_HTML = "240 W 8th St<br>Dallas, TX 75208"
MAP_Q = "240+W+8th+St,+Dallas,+TX+75208"
LAT, LON = 32.7478874, -96.8263447  # OpenStreetMap building-level geocode — see geo.json
IG = "https://www.instagram.com/trapezeoakcliff/"
CM_DEBUT = "https://dallas.culturemap.com/news/restaurants-bars/trapeze-bohemian-bar-bishop-arts/"
CM_ROUND = "https://dallas.culturemap.com/news/restaurants-bars/where-to-eat-november-2026/"

# Press-published hours (CultureMap, at opening) — fluid by the owners' own admission
HOURS_SHORT = "Wed&ndash;Thu 4 pm &ndash; late &middot; Fri&ndash;Sun 4 pm &ndash; 2 am &middot; latest hours on Instagram"
HOURS_LINES = ("Wed &amp; Thu<br>4 pm &ndash; late<br><br>"
               "Fri &ndash; Sun<br>4 pm &ndash; 2 am<br><br>"
               "Mon &amp; Tue<br>closed for now")

# Hand-drawn trapeze-rig monogram (ropes + bar + star; stroke inherits color)
RIG = ('<svg class="rig" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
       '<circle cx="12" cy="3.1" r="1.15" fill="none" stroke="currentColor" stroke-width="1.1"/>'
       '<path d="M7.4 5.6 6.2 14.4M16.6 5.6l1.2 8.8" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>'
       '<path d="M4.9 14.6h14.2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
       '<path d="M12 17.4v2.2M10.2 18.5h3.6" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/></svg>')

WORDMARK = f'{RIG}<span>Trap&egrave;ze</span>'

HEADER = (f'<a class="skip" href="#main">Skip to content</a>\n'
          '<header class="site"><div class="wrap hdr">'
          f'<a class="wm" href="/">{WORDMARK}</a>'
          '<nav aria-label="Site"><ul>'
          '<li><a href="/menu">Menu</a></li>'
          '<li><a href="/french-dining-bishop-arts">Kitchen</a></li>'
          '<li><a href="/french-bar-bishop-arts">Bar</a></li>'
          '<li><a href="/visit">Visit</a></li>'
          '</ul></nav>'
          '<a class="btn sm" href="/contact">Send a note</a>'
          '</div></header>')

FOOTER = ('<footer class="site"><div class="wrap foottop">'
          f'<div><p class="fbrand">{WORDMARK}</p>'
          '<p class="ftag">French bohemian bar &amp; bistro &middot; Bishop Arts District</p>'
          '<div class="fnaps"><p class="ftown">Find us</p>'
          f'<address class="addr">{ADDRESS_HTML}</address>'
          f'<p class="fhrs">{HOURS_SHORT}</p>'
          '<p>Questions: <a href="/contact">send a note</a> &middot; <a href="' + IG + '" rel="noopener">Instagram</a></p></div></div>'
          '<nav aria-label="Footer"><ul>'
          '<li><a href="/menu">The board</a></li>'
          '<li><a href="/french-dining-bishop-arts">French plates</a></li>'
          '<li><a href="/french-bar-bishop-arts">Cognac, absinthe &amp; wine</a></li>'
          '<li><a href="/visit">Visit</a></li>'
          '<li><a href="/contact">Contact</a></li>'
          '<li><a href="/privacy">Privacy</a></li>'
          '</ul></nav>'
          '<p class="fpress">In the news:<br>'
          f'<a href="{CM_DEBUT}" rel="noopener">CultureMap: Trap&egrave;ze debuts in Bishop Arts</a><br>'
          f'<a href="{CM_ROUND}" rel="noopener">CultureMap: where to eat in Dallas, November</a></p>'
          '</div><div class="wrap"><p class="footline">'
          f'&copy; 2026 Trap&egrave;ze &middot; French bar &amp; bistro &middot; {NAP_LINE}'
          '</p></div></footer>')

def head(title, desc, path, og=True):
    canonical = ORIGIN + ("" if path == "/" else path)
    ogblock = ""
    if og:
        ogblock = (f'<meta property="og:type" content="website">\n'
                   '<meta property="og:site_name" content="Trapèze">\n' +
                   f'<meta property="og:title" content="{title}">\n'
                   f'<meta property="og:description" content="{desc}">\n'
                   f'<meta property="og:url" content="{canonical}">\n'
                   f'<meta property="og:image" content="{ORIGIN}/og.png">\n'
                   '<meta name="twitter:card" content="summary_large_image">\n'
                   f'<meta name="twitter:title" content="{title}">\n'
                   f'<meta name="twitter:description" content="{desc}">\n'
                   f'<meta name="twitter:image" content="{ORIGIN}/og.png">\n')
    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<!-- BUILT-{BUILT} -->\n'
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{title}</title>\n'
            f'<meta name="description" content="{desc}">\n'
            '<meta name="robots" content="noindex, nofollow">\n'
            f'<link rel="canonical" href="{canonical}">\n'
            + ogblock +
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
            '<link rel="stylesheet" href="/style.css">\n</head>')

def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + '\n</script>\n'

def page(title, desc, path, body, ldobj=None, og=True):
    return (head(title, desc, path, og) + (ldobj or "") + '<body>\n' + HEADER +
            '\n<main id="main">\n' + body + '\n</main>\n' + FOOTER + '\n</body>\n</html>\n')

def faq(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in items]}

def crumb(steps):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + p}
        for i, (n, p) in enumerate(steps)]}

# ---------------------------------------------------------------- HOME
REST_ND = {
    "@type": "Restaurant", "@id": ORIGIN + "/#restaurant", "name": "Trapèze",
    "description": ("French bohemian bar and bistro in a rebuilt Oak Cliff bungalow on the west end "
                    "of the Bishop Arts District, Dallas. Old-school French plates, an all-French wine "
                    "list, cognac, absinthe cocktails and aperitifs, music late. Opened 2026."),
    "url": ORIGIN + "/", "image": ORIGIN + "/og.png",
    "servesCuisine": ["French"],
    "address": {"@type": "PostalAddress", "streetAddress": "240 W 8th St",
                "addressLocality": "Dallas", "addressRegion": "TX",
                "postalCode": "75208", "addressCountry": "US"},
    "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON},
    "menu": ORIGIN + "/menu",
    "sameAs": [IG]}
# no telephone / no openingHours / no priceRange published — omitted, never faked

HOME_LDS = {"@graph": [
    {"@type": "WebSite", "@id": ORIGIN + "/#website", "name": "Trapèze", "url": ORIGIN + "/"},
    {"@type": "WebPage", "@id": ORIGIN + "/#webpage",
     "name": "Trapèze — French Bohemian Bar & Bistro, Bishop Arts, Dallas TX",
     "url": ORIGIN + "/", "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/#restaurant"}},
    REST_ND,
    faq([
        ("What is Trapèze?",
         "A French bohemian bar and bistro on the west end of the Bishop Arts District in Dallas — old-school French plates, an all-French wine list, cognac, absinthe cocktails and music late, in a rebuilt historic bungalow."),
        ("Who is behind it?",
         "Peter Novotny and Dan Murry, who also run Ruins and Armoury D.E. in Deep Ellum. The kitchen is directed by New York-bred chef Jeremy Spector, formerly of Balthazar and Gramercy Tavern."),
        ("When are you open?",
         "Wednesday and Thursday from 4 pm until late; Friday through Sunday 4 pm to 2 am; currently closed Mondays and Tuesdays. Hours have been fluid during the first months — the newest word is always on Instagram."),
        ("What kind of food do you serve?",
         "Old-school French classics — French onion soup, oysters with leeks, steak au poivre, a burger, duck confit poutine — cooked to represent the regions of France, with flavors from France's colonial empire, including Moroccan cooking."),
        ("Is there live music?",
         "Music is part of the whole idea — performers are announced on the bar's Instagram.")])] }

HOME = page(
    "Trap&egrave;ze — French Bohemian Bar &amp; Bistro, Bishop Arts, Dallas TX",
    "Trapèze is a French bohemian bar and bistro in a rebuilt Oak Cliff bungalow on the west end of Bishop Arts, Dallas: old-school French plates, all-French wine, cognac, absinthe, music late.",
    "/",
    f'''
<section class="band noir hero"><div class="wrap narrow center">
  <p class="eyebrow">Bishop Arts District &middot; Dallas &middot; opened 2026</p>
  <h1 class="big">Trap&egrave;ze</h1>
  <p class="signline">Bien mang&eacute;, bien bu &mdash; good food, good drink</p>
  <p class="lede">A French bohemian bar and bistro in a rebuilt Oak Cliff bungalow, at the west end
  of Bishop Arts. Old-school French plates. An all-French wine list. Cognac, absinthe,
  and music going late &mdash; a place built for losing track of time.</p>
  <div class="ctarow"><a class="btn gold" href="/menu">See what&rsquo;s on the board</a>
  <a class="btn ghost" href="/contact">Send a note</a></div>
</div></section>

<section class="band wine"><div class="wrap quote">
  <p class="qmark" aria-hidden="true">&ldquo;</p>
  <blockquote>A place where people can enjoy a great meal and drinks, listen to some
  music, and just lose track of time a little.</blockquote>
  <p class="attr">Owners Peter Novotny &amp; Dan Murry, to <a href="{CM_DEBUT}" rel="noopener">CultureMap</a></p>
</div></section>

<section class="band cream"><div class="wrap split">
  <div>
    <p class="eyebrow">The idea</p>
    <h2 class="sec">An old-fashioned bohemian artist&rsquo;s enclave</h2>
    <p class="bodycopy">Trap&egrave;ze isn&rsquo;t a themed room — it&rsquo;s modeled on the old
    French bohemian bars and cabarets, where the art was the evening. The owners wanted to make
    one in the neighborhood that already has French roots: Bishop Arts was home to
    La R&eacute;union, the French utopian colony settled here in the 1850s, and the district still
    throws a Bastille Day party.</p>
    <p class="bodycopy">&ldquo;We&rsquo;re trying to do a tribute to the French history of Oak
    Cliff and Bishop Arts,&rdquo; Novotny told CultureMap, &ldquo;and our goal is to capture the
    things we love about regional French cuisine and culture.&rdquo;</p>
    <p class="note">The same team runs <a href="https://www.ruinsdeepellum.com/" rel="noopener">Ruins</a>
    and <a href="https://armouryde.com/" rel="noopener">Armoury D.E.</a> in Deep Ellum.</p>
  </div>
  <aside class="infocard">
    <h3 class="infh">House card</h3>
    <dl class="factlist">
      <div><dt>Where</dt><dd>240 W 8th St<br>Bishop Arts District<br>Dallas, TX 75208</dd></div>
      <div><dt>Hours</dt><dd>{HOURS_LINES}</dd></div>
      <div><dt>On the list</dt><dd>All-French wine &middot; cognac<br>absinthe &middot; aperitifs</dd></div>
    </dl>
    <p class="bigm"><a href="/visit">Directions &amp; hours</a></p>
  </aside>
</div></section>

<section class="band paper"><div class="wrap narrow">
  <p class="eyebrow">The house</p>
  <h2 class="sec">Kept its old face. New bones.</h2>
  <p class="bodycopy">The bungalow on West 8th sits in a conservation district, so the rebuild had
  to honor the street it stands on — the exterior was rebuilt entirely, the original look
  preserved. Out front, a hand-worked sign by the sculptural sign-makers at Decotron reads
  <em>Bien Mang&eacute;, Bien Bu</em>: good food, good drink. Inside, the plan is colorful, a
  little quirky, and built for long nights. There&rsquo;s a patio, too.</p>
  <div class="ctarow"><a class="btn" href="/visit">Plan a night</a>
  <a class="btn ghost" href="{IG}" rel="noopener">Follow on Instagram</a></div>
</div></section>

<section class="band noir"><div class="wrap split">
  <div>
    <p class="eyebrow">The kitchen</p>
    <h2 class="sec light">Old-school French, cooked by a New York r&eacute;sum&eacute;</h2>
    <p class="bodycopy">Chef Jeremy Spector — Balthazar, Gramercy Tavern, his own New York
    kitchens — directs the menu. It runs through the regions of France, with flavors pulled from
    France&rsquo;s colonial empire, Morocco included. The opening list was short and confident:
    French onion soup, oysters with leeks, steak au poivre, a burger, duck confit poutine.</p>
    <div class="ctarow"><a class="btn gold" href="/french-dining-bishop-arts">The plates, in detail</a></div>
  </div>
  <div>
    <p class="eyebrow">The bar</p>
    <h2 class="sec light">A bar that never crosses the Atlantic</h2>
    <p class="bodycopy">Every wine on the list is French. Around it: an extensive cognac list,
    absinthe and Chartreuse cocktails in the classic French and New Orleans lines, French-Caribbean
    rhum agricoles, aperitifs and digestifs, and French — and French-adjacent — cider and beer.</p>
    <div class="ctarow"><a class="btn gold" href="/french-bar-bishop-arts">The bar, in detail</a></div>
  </div>
</div></section>

<section class="band cream"><div class="wrap narrow">
  <p class="eyebrow">New here?</p>
  <h2 class="sec">CultureMap found it for November</h2>
  <p class="bodycopy">&ldquo;Sultry new bar and bistro&rdquo; is now open on the west end of
  Bishop Arts, picked for CultureMap&rsquo;s November roundup of the city&rsquo;s openings —
  described, in the owners&rsquo; words, as a place to &ldquo;eat, drink, listen to music, and
  lose track of time.&rdquo;</p>
  <p class="note">Read the write-ups: <a href="{CM_DEBUT}" rel="noopener">the debut piece</a>
  and the <a href="{CM_ROUND}" rel="noopener">November openings roundup</a>. Night-by-night word,
  including live-music bills: <a href="{IG}" rel="noopener">@trapezeoakcliff</a>.</p>
  <div class="ctarow"><a class="btn" href="/contact">Ask us something</a>
  <a class="btn ghost" href="/menu">The board</a></div>
</div></section>
''',
    ld(HOME_LDS))

# ---------------------------------------------------------------- MENU HUB
MENU_LDS = {"@graph": [
    {"@type": "WebPage", "name": "The board — food and drink at Trapèze, Bishop Arts, Dallas TX",
     "url": ORIGIN + "/menu", "isPartOf": {"@id": ORIGIN + "/#website"}},
    crumb([("Home", "/"), ("Menu", "/menu")]),
    {"@type": "Menu", "name": "Trapèze — board (as reported by CultureMap)",
     "description": ("Old-school French plates and a Franco-focused bar. As reported by CultureMap at opening; "
                     "the kitchen has been widening the list since. Prices live at the table, not on this page."),
     "hasMenuSection": [
        {"@type": "MenuSection", "name": "From the kitchen", "description": "Regional French classics, as named by CultureMap.",
         "hasMenuItem": [
            {"@type": "MenuItem", "name": "French onion soup", "description": "The classic: onions cooked down, broth, a browned cheese cap."},
            {"@type": "MenuItem", "name": "Oysters with leeks", "description": "Hot oysters partnered with leeks, French Brasserie style."},
            {"@type": "MenuItem", "name": "Steak au poivre", "description": "Seared steak under crushed peppercorns with a cream pan sauce."},
            {"@type": "MenuItem", "name": "Burger", "description": "On the list among the classics."},
            {"@type": "MenuItem", "name": "Duck confit poutine", "description": "Fries and cheese curds under duck confit and gravy — Quebec's snack, rethought."}]},
        {"@type": "MenuSection", "name": "From the bar", "description": "The Franco-focused bar program, as reported by CultureMap.",
         "hasMenuItem": [
            {"@type": "MenuItem", "name": "All-French wine list", "description": "Every bottle is from France."},
            {"@type": "MenuItem", "name": "Cognac", "description": "An extensive list of the spirit."},
            {"@type": "MenuItem", "name": "Absinthe & Chartreuse cocktails", "description": "Classic French and New Orleans-lines builds."},
            {"@type": "MenuItem", "name": "Rhum agricole", "description": "French-Caribbean rums distilled from pressed cane juice."},
            {"@type": "MenuItem", "name": "Aperitifs & digestifs", "description": "The before and the after."},
            {"@type": "MenuItem", "name": "French cider & beer", "description": "French and 'French-adjacent' pours."}]}]},
    faq([
        ("How much is dinner?",
         "Prices live at the table, not on this site — so the board can move with the market without a web edit."),
        ("Is the menu long?",
         "It opened short and confident, and the owners said the full list and brunch were coming right after opening. Tonight's board is the live answer — Instagram carries the newest word."),
        ("What's the one thing to try?",
         "The duck confit poutine: French cooking wearing Quebec's favorite snack. Or the plate everyone orders at a French brasserie — steak au poivre."),
        ("Do you have vegetarian options?",
         "The board moves; ask the floor. French onion soup is already vegetable-forward before the cheese goes on.")])] }

MENU = page(
    "The Board: Old-School French Plates &amp; Franco Cocktails — Trap&egrave;ze, Bishop Arts, Dallas TX",
    "Trapèze's board: French onion soup, oysters with leeks, steak au poivre, a burger, duck confit poutine — plus all-French wine, cognac, absinthe cocktails and aperitifs. Bishop Arts, Dallas.",
    "/menu",
    '''
<section class="band noir herol"><div class="wrap">
  <p class="eyebrow">The board</p>
  <h1>Short list. Long night.</h1>
  <p class="lede">The kitchen opened with a handful of old-school French plates and has been
  widening it since — the bar, meanwhile, never leaves France. What follows is the board as
  CultureMap reported it at opening. Tonight&rsquo;s printed menu is the live answer, and
  it lives at the table.</p>
</div></section>

<section class="band cream"><div class="wrap boardgrid">
  <div class="group">
    <p class="eyebrow">From the kitchen</p>
    <h2 class="sec">The plates named at opening</h2>
    <ul class="plist">
      <li><span class="pname">French onion soup</span> <span class="pdash">&mdash;</span>
      onions cooked down, good broth, a browned cap of cheese. The barometer of any French
      brasserie.</li>
      <li><span class="pname">Oysters with leeks</span> <span class="pdash">&mdash;</span> hot
      oysters paired with leeks, the Marais-style move on the half shell.</li>
      <li><span class="pname">Steak au poivre</span> <span class="pdash">&mdash;</span> seared
      steak under crushed peppercorns, cream pan sauce poured over.</li>
      <li><span class="pname">A burger</span> <span class="pdash">&mdash;</span> sitting on the
      list among the classics, the way Paris menus have always done.</li>
      <li><span class="pname">Duck confit poutine</span> <span class="pdash">&mdash;</span> fries,
      cheese curds, gravy, and the duck on top: Quebec&rsquo;s late-night snack, rethought by a
      French kitchen.</li>
    </ul>
    <p class="bigm"><a href="/french-dining-bishop-arts">The kitchen, in detail</a></p>
  </div>
  <div class="group">
    <p class="eyebrow">From the bar</p>
    <h2 class="sec">France, from the first pour</h2>
    <ul class="plist">
      <li><span class="pname">All-French wine</span> <span class="pdash">&mdash;</span> every
      bottle on the list is from France. The list doesn&rsquo;t cross the border.</li>
      <li><span class="pname">Cognac</span> <span class="pdash">&mdash;</span> an extensive list
      of France&rsquo;s brandy, poured neat.</li>
      <li><span class="pname">Absinthe &amp; Chartreuse</span> <span class="pdash">&mdash;</span>
      cocktails built on the old French lines, with a New Orleans vein running through them.</li>
      <li><span class="pname">Rhum agricole</span> <span class="pdash">&mdash;</span> rums from
      the French Caribbean, distilled from pressed cane juice, not molasses.</li>
      <li><span class="pname">Aperitifs &amp; digestifs</span> <span class="pdash">&mdash;</span>
      the before and the after — both taken seriously here.</li>
      <li><span class="pname">Cider &amp; beer</span> <span class="pdash">&mdash;</span> French
      and &ldquo;French-adjacent,&rdquo; for when a bottle of something big is too much ceremony.</li>
    </ul>
    <p class="bigm"><a href="/french-bar-bishop-arts">The bar, in detail</a></p>
  </div>
</div></section>

<section class="band paper"><div class="wrap narrow center">
  <p class="eyebrow">The honest note</p>
  <h2 class="sec">Prices live at the table</h2>
  <p class="bodycopy">This page keeps the named plates and pours — what the press reported at
  opening. Numbers, specials, and whatever brunch the kitchen has been building live on the
  printed board and the floor. Follow <a href="''' + IG + '''" rel="noopener">Instagram</a>
  for the newest version.</p>
  <div class="ctarow center"><a class="btn" href="/visit">Hours &amp; directions</a>
  <a class="btn ghost" href="/contact">Ask about tonight</a></div>
</div></section>
''',
    ld(MENU_LDS))

# ---------------------------------------------------------------- KITCHEN DETAIL
KIT_LDS = {"@graph": [
    {"@type": "WebPage", "name": "French bistro plates in Bishop Arts — Trapèze, Dallas TX",
     "url": ORIGIN + "/french-dining-bishop-arts", "isPartOf": {"@id": ORIGIN + "/#website"}},
    crumb([("Home", "/"), ("Menu", "/menu"), ("Kitchen", "/french-dining-bishop-arts")]),
    {"@type": "Service", "name": "Old-school French bistro dining",
     "serviceType": "Restaurant dining", "areaServed": {"@type": "City", "name": "Dallas"},
     "provider": {"@id": ORIGIN + "/#restaurant"}},
    faq([
        ("Who cooks?",
         "Chef Jeremy Spector directs the culinary program — New York-bred, with stints at Balthazar and Gramercy Tavern and his own New York restaurants behind him."),
        ("How French is the food, really?",
         "The menu is built to represent the regions of France, plus flavors from France's colonial empire — Moroccan cooking is part of the story, per the owners."),
        ("What was on the menu when you opened?",
         "A short list CultureMap named at opening: French onion soup, oysters with leeks, steak au poivre, a burger, and duck confit poutine. The full menu and brunch were promised right behind it — ask the floor what's live tonight."),
        ("Is the burger a joke plate?",
         "Not at all — Paris brasseries have printed a burger next to the classics for a century. Here it sits in the same company."),
        ("Where do I eat this?",
         "At 240 W 8th St, in the rebuilt bungalow at the west end of Bishop Arts. Wed–Thu from 4 pm, Fri–Sun 4 pm to 2 am; latest hours on Instagram.")])] }

KIT = page(
    "French Bistro Plates &amp; a New York Chef — Trap&egrave;ze, Bishop Arts, Dallas TX",
    "Steak au poivre, French onion soup, oysters with leeks, duck confit poutine at Trapèze: regional French cooking directed by chef Jeremy Spector (Balthazar, Gramercy Tavern). Bishop Arts, Dallas.",
    "/french-dining-bishop-arts",
    '''
<section class="band noir herol"><div class="wrap">
  <p class="eyebrow">The kitchen &middot; Bishop Arts</p>
  <h1>Dinner, the old French way</h1>
  <p class="lede">Not bistro as a costume — bistro as a set of convictions: good broth, real
  butter, pepper put in by hand, and a kitchen that has cooked in the rooms that made those
  rules. Chef Jeremy Spector runs it.</p>
</div></section>

<section class="band cream"><div class="wrap plate">
  <h2 class="pname bigname">French onion soup</h2>
  <p class="tagline">The barometer &middot; onions, broth, a browned cheese cap</p>
  <p class="bodycopy">Every city has a barometer of whether its French kitchen takes itself
  seriously, and it&rsquo;s served in a crock. Onions cooked down until sweet, real broth, a
  lid of browned cheese that takes a spoon to break. The opening list starts here, which says
  what the kitchen is for.</p>
</div></section>

<section class="band paper"><div class="wrap plate">
  <h2 class="pname bigname">Oysters with leeks &middot; steak au poivre</h2>
  <p class="tagline">The brasserie double header</p>
  <p class="bodycopy">Hot oysters partnered with leeks is the Marais order — shellfish treated
  like a course, not a platter. And steak au poivre is the plate a French kitchen is judged
  on: seared steak under a crust of crushed peppercorns, cream pan sauce finished in the
  pan, pepper put in by hand so the crust has texture. A burger rides along with them,
  French-menus style.</p>
</div></section>

<section class="band wine"><div class="wrap plate">
  <h2 class="pname bigname light">Duck confit poutine</h2>
  <p class="tagline">French technique &middot; Quebec&rsquo;s great snack</p>
  <p class="bodycopy">Fries, cheese curds, gravy — the Montreal late-night plate — with duck
  confit on top instead of whatever came to hand. It&rsquo;s the plate that tells you how this
  kitchen thinks: technique from France, appetite from anywhere the night goes.</p>
</div></section>

<section class="band cream"><div class="wrap narrow">
  <p class="eyebrow">Behind the pass</p>
  <h2 class="sec">The chef, and the wider map</h2>
  <p class="bodycopy">The owners brought in Jeremy Spector — New York-bred, Balthazar,
  Gramercy Tavern, his own New York restaurants — to direct the whole program. Per CultureMap,
  the menu represents the regions of France, with flavors from France&rsquo;s once-vast colonial
  empire, Moroccan cooking among them. The five plates named at opening are the short version;
  the full list — brunch included — was promised right behind them.</p>
  <p class="note">What&rsquo;s actually live tonight moves with the kitchen. The floor and
  <a href="''' + IG + '''" rel="noopener">Instagram</a> are the live answer; prices live at the
  table, never on this site.</p>
  <div class="ctarow"><a class="btn" href="/french-bar-bishop-arts">Follow it to the bar</a>
  <a class="btn ghost" href="/visit">Hours &amp; directions</a></div>
</div></section>
''',
    ld(KIT_LDS))

# ---------------------------------------------------------------- BAR DETAIL
BAR_LDS = {"@graph": [
    {"@type": "WebPage", "name": "The French bar at Trapèze — cognac, absinthe, all-French wine, Bishop Arts, Dallas TX",
     "url": ORIGIN + "/french-bar-bishop-arts", "isPartOf": {"@id": ORIGIN + "/#website"}},
    crumb([("Home", "/"), ("Menu", "/menu"), ("Bar", "/french-bar-bishop-arts")]),
    {"@type": "Service", "name": "French bar program: cognac, absinthe cocktails, aperitifs, all-French wine",
     "serviceType": "Bar", "areaServed": {"@type": "City", "name": "Dallas"},
     "provider": {"@id": ORIGIN + "/#restaurant"}},
    faq([
        ("Is the wine list really all French?",
         "Yes — CultureMap reports an all-French selection of wines. The list doesn't cross the border."),
        ("What do you mix with?",
         "France and its empire: absinthe and Chartreuse in classic French and New Orleans-lines builds, an extensive cognac list, and French-Caribbean rhum agricoles."),
        ("What's an aperitif?",
         "The drink before dinner that starts the evening — this bar takes the before and the after (the digestif) seriously, as French bars do."),
        ("What is rhum agricole?",
         "Rum distilled from pressed sugar-cane juice rather than molasses, made in the French Caribbean — grassier and more peppery than molasses rums."),
        ("I just want a beer. Is that allowed?",
         "French — and 'French-adjacent' — cider and beer are on the list. Ceremony optional."),
        ("Is there music at the bar?",
         "Music is core to the concept. Performers are announced on Instagram.")])] }

BAR = page(
    "French Bar: Cognac, Absinthe &amp; All-French Wine — Trap&egrave;ze, Bishop Arts, Dallas TX",
    "Trapèze's Franco-focused bar in Bishop Arts, Dallas: an all-French wine list, extensive cognac, absinthe and Chartreuse cocktails, rhum agricole, aperitifs, digestifs, French cider and beer.",
    "/french-bar-bishop-arts",
    '''
<section class="band wine herol"><div class="wrap">
  <p class="eyebrow">The bar &middot; Bishop Arts</p>
  <h1>A bar that never crosses the Atlantic</h1>
  <p class="lede">The wine list is entirely French — full stop. Around it sits everything France
  distills, ferments, and pours: cognac, absinthe, Chartreuse, rhum agricole from the French
  Caribbean, cider, beer, and the rituals of the aperitif and the digestif.</p>
</div></section>

<section class="band noir"><div class="wrap split">
  <div>
    <p class="eyebrow">The deep end</p>
    <h2 class="sec light">Cognac, put first</h2>
    <p class="bodycopy">An extensive cognac list is a statement in any American city — it says
    the bar expects you to slow down. Two Deep Ellum bar veterans built this program, and it
    shows: the spirit France brandies gets the shelf space, poured neat, ordered by house if
    you want a tour.</p>
  </div>
  <div>
    <p class="eyebrow">The green end</p>
    <h2 class="sec light">Absinthe &amp; Chartreuse, in the old lines</h2>
    <p class="bodycopy">Cocktails are built on classic French and New Orleans-esque lines with
    French spirits and liqueurs at the center — absinthe and Chartreuse doing the work they did
    in the cabaret bars this room is modeled on.</p>
  </div>
</div></section>

<section class="band cream"><div class="wrap split">
  <div>
    <p class="eyebrow">The islands</p>
    <h2 class="sec">Rhum agricole</h2>
    <p class="bodycopy">France&rsquo;s Caribbean departments distill rum from pressed cane juice,
    not molasses — grassier, peppery, more itself. The bar carries those rhums agricoles, the
    bottles the Atlantic French world actually drinks.</p>
  </div>
  <div>
    <p class="eyebrow">The ceremonies</p>
    <h2 class="sec">Aperitif before, digestif after</h2>
    <p class="bodycopy">A solid menu of aperitifs and digestifs — the drink that opens the
    evening and the one that closes it, treated as real courses of a night rather than
    add-ons. Come early; the first hour is its own reason to come.</p>
  </div>
</div></section>

<section class="band paper"><div class="wrap narrow">
  <p class="eyebrow">Without the ceremony</p>
  <h2 class="sec">Wine, cider, or a beer — fine</h2>
  <p class="bodycopy">Every bottle of wine is French; the cider and beer are French and
  &ldquo;French-adjacent.&rdquo; You can do the whole cognac pilgrimage or just order a glass
  of something cold. The bar is the living half of the cabaret idea &mdash; and performers
  get announced on <a href="''' + IG + '''" rel="noopener">Instagram</a>, the same place the
  hours and the bill for any given night get posted.</p>
  <div class="ctarow"><a class="btn" href="/french-dining-bishop-arts">What the kitchen is cooking</a>
  <a class="btn ghost" href="/visit">Hours &amp; directions</a></div>
</div></section>
''',
    ld(BAR_LDS))

# ---------------------------------------------------------------- VISIT
VISIT_LDS = {"@graph": [
    {"@type": "WebPage", "name": "Visit Trapèze — 240 W 8th St, Bishop Arts, Dallas TX",
     "url": ORIGIN + "/visit", "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/#restaurant"}},
    crumb([("Home", "/"), ("Visit", "/visit")]),
    faq([
        ("Where is Trapèze?",
         "240 W 8th Street, at the west end of the Bishop Arts District in Oak Cliff, Dallas, TX 75208 — a rebuilt historic bungalow."),
        ("What are the hours?",
         "Wednesday and Thursday 4 pm until late; Friday through Sunday 4 pm to 2 am; currently closed Mondays and Tuesdays. Hours have been fluid in the first months — the newest word is always on Instagram."),
        ("Do you take reservations?",
         "Not posted anywhere official — if you want a table for a specific night, the contact form is the way to ask, and the owners answer there."),
        ("Where do I park?",
         "Bishop Arts is a walk-around neighborhood: park on the surrounding blocks and stroll in."),
        ("Is there a patio?",
         "Yes — the patio came together as the bar opened."),
        ("How do I know who's playing?",
         "Live-music performers are announced on the bar's Instagram — that's also where hour changes get posted.")])] }

VISIT = page(
    "Visit Trap&egrave;ze: 240 W 8th St, Bishop Arts &mdash; Dallas TX",
    "Visit Trapèze at 240 W 8th St, Bishop Arts District, Dallas TX 75208. Wed–Thu 4 pm–late, Fri–Sun 4 pm–2 am (latest hours on Instagram). Directions, map, and how to reach the owners.",
    "/visit",
    f'''
<section class="band noir herol"><div class="wrap">
  <p class="eyebrow">Visit</p>
  <h1>The west end of Bishop Arts</h1>
  <p class="lede">A rebuilt bungalow on West 8th Street, where Oak Cliff&rsquo;s old French
  chapter started and the district&rsquo;s newest night happens. Come hungry, come early,
  or come just after the kitchen closes.</p>
</div></section>

<section class="band cream"><div class="wrap cardgrid">
  <div class="infocard"><h3 class="infh">Address</h3>
    <address class="addr">{ADDRESS_HTML}</address>
    <p class="note">Bishop Arts District, Oak Cliff.</p>
    <p class="bigm"><a href="https://www.google.com/maps/dir/?api=1&amp;destination={MAP_Q}" rel="noopener">Get directions</a></p></div>
  <div class="infocard"><h3 class="infh">Hours</h3>
    <dl class="factlist">
      <div><dt>Wed &amp; Thu</dt><dd>4 pm &ndash; late</dd></div>
      <div><dt>Fri &ndash; Sun</dt><dd>4 pm &ndash; 2 am</dd></div>
      <div><dt>Mon &amp; Tue</dt><dd>closed for now</dd></div>
    </dl>
    <p class="note">Hours have been fluid &mdash; updates land on
    <a href="{IG}" rel="noopener">Instagram</a>.</p></div>
  <div class="infocard"><h3 class="infh">Ask the owners</h3>
    <p class="note">The <a href="/contact">contact form</a> reaches the people who run the
    place &mdash; tables, nights, anything worth asking about.</p>
    <p class="note">Night bills, music, and hour changes:
    <a href="{IG}" rel="noopener">@trapezeoakcliff</a>.</p></div>
</div></section>

<section class="band paper"><div class="wrap">
  <div class="mapcell"><iframe src="https://www.google.com/maps?q={MAP_Q}&amp;output=embed"
    title="Map: Trapèze, 240 W 8th St, Dallas, TX 75208" loading="lazy"></iframe></div>
  <p class="fineprint">Map: 240 W 8th St, Dallas, TX 75208 &mdash; west end of the Bishop Arts District.</p>
</div></section>

<section class="band wine"><div class="wrap narrow center">
  <h2 class="sec light">Before you come</h2>
  <p class="secsub">See the board &mdash; the plates, the pours, and what duck confit does to
  a poutine.</p>
  <div class="ctarow"><a class="btn gold" href="/menu">See the board</a>
  <a class="btn ghost" href="/contact">Send a note</a></div>
</div></section>
''',
    ld(VISIT_LDS))

# ---------------------------------------------------------------- CONTACT
CONTACT_LDS = {"@graph": [
    {"@type": "WebPage", "name": "Contact Trapèze — Bishop Arts, Dallas TX", "url": ORIGIN + "/contact",
     "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/#restaurant"}},
    crumb([("Home", "/"), ("Contact", "/contact")])]}

CONTACT = page(
    "Contact Trap&egrave;ze — Bishop Arts, Dallas TX",
    "Ask Trapèze anything: a table for a specific night, the full menu, music nights, or hours. The form reaches the owners directly.",
    "/contact",
    f'''
<section class="band noir herol"><div class="wrap">
  <p class="eyebrow">Contact</p>
  <h1>Send the owners a note</h1>
  <p class="lede">A table for a particular night, what brunch looks like, who&rsquo;s playing,
  a question nobody thinks to ask at the bar &mdash; this form reaches the people who run the
  place, and notes get read in the order they arrive.</p>
</div></section>

<section class="band paper"><div class="wrap contactgrid">
  <div class="formside"><form class="cform" method="post" action="/contact" accept-charset="utf-8">
    <h2 class="infh">Leave a note</h2>
    <div class="fields">
      <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="f-phone">Phone <span class="opt">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field full"><label for="f-email">Email <span class="opt">(optional &mdash; so we can answer)</span></label><input id="f-email" name="email" type="email" autocomplete="email"></div>
      <div class="field full"><label for="f-msg">Your message</label><textarea id="f-msg" name="message" required></textarea></div>
    </div>
    <p class="formnote">Notes are read in the order they arrive.</p>
    <button class="btn full" type="submit">Send it</button>
  </form></div>
  <aside class="infocard"><h3 class="infh">Other ways</h3>
    <address class="addr">{ADDRESS_HTML}</address>
    <p class="note">Hours: Wed&ndash;Thu 4 pm &ndash; late &middot; Fri&ndash;Sun 4 pm &ndash; 2 am
    &middot; latest word on Instagram.</p>
    <p class="note">Instagram: <a href="{IG}" rel="noopener">@trapezeoakcliff</a></p>
    <p class="note">Seen in: <a href="{CM_DEBUT}" rel="noopener">CultureMap</a></p>
  </aside>
</div></section>
''',
    ld(CONTACT_LDS))

# ---------------------------------------------------------------- PRIVACY
PRIVACY_LDS = {"@graph": [
    {"@type": "WebPage", "name": "Privacy — Trapèze, Bishop Arts, Dallas TX", "url": ORIGIN + "/privacy",
     "isPartOf": {"@id": ORIGIN + "/#website"}},
    crumb([("Home", "/"), ("Privacy", "/privacy")])]}

PRIVACY = page(
    "Privacy — Trap&egrave;ze, Bishop Arts, Dallas TX",
    "How the Trapèze website handles the contact form: what it collects, what it doesn't, and who reads it.",
    "/privacy",
    f'''
<section class="band noir herol"><div class="wrap">
  <p class="eyebrow">Privacy</p>
  <h1>What this site does with your information</h1>
</div></section>

<section class="band paper"><div class="wrap narrow">
  <h2 class="sec">The contact form</h2>
  <p class="bodycopy">The form asks for a name and a message, and optionally a phone number and
  an email address. Those details go to Trap&egrave;ze so the owners can answer you
  &mdash; nothing else. Notes are kept only as long as it takes to reply and settle whatever
  you asked about.</p>
  <h2 class="sec">No cookies, no trackers</h2>
  <p class="bodycopy">This site sets no cookies, runs no advertising pixels and loads no
  third-party scripts. There is no analytics software watching your visit and nothing to opt
  out of.</p>
  <h2 class="sec">The map</h2>
  <p class="bodycopy">The Visit page embeds a Google Maps view. When that map loads, Google
  receives the standard request data of your browser (including its IP address), under
  Google&rsquo;s own privacy terms. Every other page loads without contacting Google.</p>
  <h2 class="sec">Questions about your note</h2>
  <p class="bodycopy">Ask through the <a href="/contact">contact form</a> to see, correct or
  delete what a note contains. We will honor it.</p>
  <p class="note">Postal address: {NAP_LINE}.</p>
</div></section>
''',
    ld(PRIVACY_LDS))

# ---------------------------------------------------------------- 404 / THANKS
THANKS = page(
    "Thank You — Trap&egrave;ze, Bishop Arts",
    "Your note has reached Trapèze. The owners read what arrives in order and answer.",
    "/thanks",
    '''
<section class="band wine herol"><div class="wrap narrow center">
  <p class="eyebrow">Note received</p>
  <h1>Your message is in.</h1>
  <p class="lede">The owners read every note and answer in the order they arrive. Night bills
  and hour changes land on Instagram first.</p>
  <div class="ctarow center"><a class="btn" href="/">Back to the front page</a>
  <a class="btn ghost" href="/menu">See the board</a></div>
</div></section>
'''.replace("&eacute;", "é"), None, og=False)

E404 = page(
    "Page Not Found — Trap&egrave;ze, Bishop Arts",
    "That page isn't here. The board, the plates, the bar and the visit page are one click away.",
    "/404",
    '''
<section class="band cream herol"><div class="wrap narrow center">
  <p class="eyebrow">404</p>
  <h1>Nothing serving at that address.</h1>
  <p class="lede">Wrong page, right bar. Try one of these:</p>
  <div class="ctarow center"><a class="btn" href="/">Front page</a>
  <a class="btn ghost" href="/menu">The board</a>
  <a class="btn ghost" href="/contact">Contact</a></div>
</div></section>
''', None, og=False)

# ---------------------------------------------------------------- sitemap / robots
PAGES_SITEMAP = ["/", "/menu", "/french-dining-bishop-arts", "/french-bar-bishop-arts",
                 "/visit", "/contact", "/privacy"]
sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
for pp in PAGES_SITEMAP:
    sitemap += f'<url><loc>{ORIGIN}/</loc><lastmod>{BUILT}</lastmod></url>\n' if pp == "/" else f'<url><loc>{ORIGIN}{pp}</loc><lastmod>{BUILT}</lastmod></url>\n'
sitemap += "</urlset>\n"

robots = f"""User-agent: *
Disallow: /thanks
Disallow: /404

Sitemap: {ORIGIN}/sitemap.xml
"""

FILES = {"index.html": HOME, "menu.html": MENU, "french-dining-bishop-arts.html": KIT,
         "french-bar-bishop-arts.html": BAR, "visit.html": VISIT,
         "contact.html": CONTACT, "privacy.html": PRIVACY, "thanks.html": THANKS, "404.html": E404,
         "sitemap.xml": sitemap, "robots.txt": robots}

os.makedirs(PUBLIC, exist_ok=True)
for name, content in FILES.items():
    with open(os.path.join(PUBLIC, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name, len(content.encode("utf-8")), "bytes")
