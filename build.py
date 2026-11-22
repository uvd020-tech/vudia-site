#!/usr/bin/env python3
"""Generate the Vudia vendor site from data/site.json. No dependencies.

Run from the repository root:  python build.py
Writes: index.html, about/, apps/<slug>/, 404.html, robots.txt, sitemap.xml, llms.txt
"""
import datetime
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
SITE = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))
BASE = SITE["url"].rstrip("/")
TODAY = datetime.date.today().isoformat()

# Same bots as docs.vudia.site/robots.txt (checked 2026-11-22).
BOTS = [
    "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
    "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended",
    "Applebot-Extended", "Bingbot", "*",
]


def e(text):
    return html.escape(text, quote=True)


def jsonld(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1).replace("</", "<\\/")


def org():
    return {
        "@type": "Organization",
        "name": SITE["name"],
        "url": BASE + "/",
        "email": SITE["email"],
        "description": SITE["about"][0],
    }


def layout(title, description, path, body, blocks, og_type="website"):
    canonical = BASE + path
    scripts = "\n".join(
        '<script type="application/ld+json">\n%s\n</script>' % jsonld(dict({"@context": "https://schema.org"}, **b))
        for b in blocks
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{e(SITE['name'])}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="stylesheet" href="/assets/style.css">
{scripts}
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="site"><div class="wrap">
<a class="brand" href="/">{e(SITE['name'])}</a>
<nav class="main" aria-label="Main"><a href="/#apps">Apps</a><a href="/about/">About</a></nav>
</div></header>
<main id="content"><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">
<span>&copy; {e(SITE['name'])} &middot; <a href="mailto:{e(SITE['email'])}">{e(SITE['email'])}</a></span>
<span><a href="/about/">About</a> &middot; <a href="{e(SITE['marketplaceVendor'])}">Vudia on the Atlassian Marketplace</a></span>
</div></footer>
</body>
</html>
"""


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def app_url(a):
    return f"/apps/{a['slug']}/"


def app_summary():
    return "estimation, default values, project cost and time in status"


def home():
    cards = []
    for a in SITE["apps"]:
        cards.append(
            f"""<article class="card">
<h3><a href="{app_url(a)}">{e(a['name'])}</a></h3>
<p>{e(a['tagline'])}.</p>
<p class="links"><a href="{app_url(a)}">Details</a><a href="{e(a['listing'])}">Atlassian Marketplace</a><a href="{e(a['docsHome'])}">Documentation</a></p>
</article>"""
        )
    body = f"""<h1>{e(SITE['tagline'])}</h1>
<p class="lead">{e(SITE['about'][0])}</p>
<h2 id="apps">Apps</h2>
<div class="grid">
{chr(10).join(cards)}
</div>
<h2>About Vudia</h2>
<p>{e(SITE['about'][1])} All our apps are Jira Cloud apps built on Atlassian Forge and listed on the <a href="{e(SITE['marketplaceVendor'])}">Atlassian Marketplace</a>.</p>
<p>{e(SITE['about'][2])} Write to <a href="mailto:{e(SITE['email'])}">{e(SITE['email'])}</a>. <a href="/about/">More about Vudia</a>.</p>"""
    title = "Vudia — Apps for Jira on the Atlassian Marketplace"
    desc = f"{SITE['about'][0]} Apps for Jira Cloud: {app_summary()}."
    blocks = [
        org(),
        {"@type": "WebSite", "name": SITE["name"], "url": BASE + "/", "description": desc},
    ]
    write("index.html", layout(title, desc, "/", body, blocks))


def about():
    apps = "\n".join(
        f'<li><a href="{app_url(a)}">{e(a["name"])}</a>: {e(a["tagline"])}.</li>' for a in SITE["apps"]
    )
    policies = "\n".join(
        f'<li>{e(a["name"])}: <a href="{e(a["privacy"])}">privacy policy</a>, <a href="{e(a["security"])}">security policy</a></li>'
        for a in SITE["apps"]
    )
    paras = "\n".join(f"<p>{e(t)}</p>" for t in SITE["about"])
    body = f"""<h1>About Vudia</h1>
{paras}
<h2>Our apps</h2>
<ul class="plain">
{apps}
</ul>
<h2>Contact</h2>
<p>Support and feedback: <a href="mailto:{e(SITE['email'])}">{e(SITE['email'])}</a>. Hours: {e(SITE['hours'])}.</p>
<p>To report a security issue: <a href="mailto:{e(SITE['securityEmail'])}">{e(SITE['securityEmail'])}</a>.</p>
<h2>Policies</h2>
<ul class="plain">
{policies}
</ul>
<p class="muted">Vudia on the <a href="{e(SITE['marketplaceVendor'])}">Atlassian Marketplace</a>.</p>"""
    title = "About Vudia — contact, apps and policies"
    desc = f"{SITE['about'][0]} Contact, security contact and the privacy and security policy of every app."
    blocks = [
        org(),
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": SITE["name"], "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "About", "item": BASE + "/about/"},
        ]},
    ]
    write("about/index.html", layout(title, desc, "/about/", body, blocks))


def app_page(a):
    facts = "\n".join(f"<li>{e(f)}</li>" for f in a["facts"])
    aka = ""
    if a["alsoKnownAs"]:
        aka = f"<li>Also called: {e(', '.join(a['alsoKnownAs']))}</li>\n"
    docs = "\n".join(
        f'<div><dt><a href="{e(d["url"])}">{e(d["title"])}</a></dt><dd>{e(d["desc"])}</dd></div>'
        for d in a["docPages"]
    )
    body = f"""<p class="crumbs"><a href="/">{e(SITE['name'])}</a> / <a href="/#apps">Apps</a> / {e(a['name'])}</p>
<h1>{e(a['name'])}</h1>
<p class="lead">{e(a['tagline'])}.</p>
<p>{e(a['description'])}</p>
<p><a class="button" href="{e(a['listing'])}">View on Atlassian Marketplace</a><a class="button secondary" href="{e(a['docsHome'])}">Documentation</a></p>
<h2>At a glance</h2>
<ul class="plain">
{aka}{facts}
</ul>
<p class="muted">Pricing for larger teams is shown on the Marketplace listing.</p>
<h2>Documentation</h2>
<dl class="docs">
{docs}
</dl>
<h2>Policies</h2>
<ul class="plain">
<li><a href="{e(a['privacy'])}">Privacy policy</a></li>
<li><a href="{e(a['security'])}">Security policy</a></li>
</ul>
<h2>Questions</h2>
<p>Write to <a href="mailto:{e(SITE['email'])}">{e(SITE['email'])}</a>. To report a security issue: <a href="mailto:{e(SITE['securityEmail'])}">{e(SITE['securityEmail'])}</a>.</p>"""
    title = f"{a['name']} — {SITE['name']}"
    desc = a["tagline"] + "."
    app_ld = {
        "@type": "SoftwareApplication",
        "name": a["name"],
        "description": a["description"],
        "applicationCategory": "BusinessApplication",
        "applicationSuite": "Jira",
        "operatingSystem": "Jira Cloud (Atlassian Forge)",
        "url": a["listing"],
        "publisher": {"@type": "Organization", "name": SITE["name"], "url": BASE + "/", "email": SITE["email"]},
    }
    if a["alsoKnownAs"]:
        app_ld["alternateName"] = a["alsoKnownAs"]
    blocks = [
        org(),
        app_ld,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": SITE["name"], "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Apps", "item": BASE + "/#apps"},
            {"@type": "ListItem", "position": 3, "name": a["name"], "item": BASE + app_url(a)},
        ]},
    ]
    write(f"apps/{a['slug']}/index.html", layout(title, desc, app_url(a), body, blocks))


def not_found():
    body = """<h1>Page not found</h1>
<p class="lead">This page does not exist.</p>
<p><a href="/">Back to the Vudia home page</a></p>"""
    text = layout("Page not found — Vudia", "This page does not exist.", "/404.html", body, [])
    write("404.html", text.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1))


def robots():
    parts = [f"User-agent: {b}\nAllow: /\n" for b in BOTS]
    write("robots.txt", "\n".join(parts) + f"\nSitemap: {BASE}/sitemap.xml\n")


def sitemap():
    paths = ["/", "/about/"] + [app_url(a) for a in SITE["apps"]]
    urls = "\n".join(
        f"  <url>\n    <loc>{BASE}{p}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>" for p in paths
    )
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')


def llms():
    L = [f"# {SITE['name']}", "",
         f"> {SITE['about'][0]} Apps for Jira Cloud: {app_summary()}.", "",
         "Vudia apps are Jira Cloud apps built on Atlassian Forge and listed on the Atlassian Marketplace.",
         f"Vendor page on the Atlassian Marketplace: {SITE['marketplaceVendor']}",
         f"Support: {SITE['email']}", "", "## Apps", ""]
    for a in SITE["apps"]:
        aka = f" Also called: {', '.join(a['alsoKnownAs'])}." if a["alsoKnownAs"] else ""
        L.append(f"- [{a['name']}]({BASE}{app_url(a)}): {a['tagline']}.{aka}")
    L += ["", "## Atlassian Marketplace listings", ""]
    for a in SITE["apps"]:
        L.append(f"- [{a['name']} on the Atlassian Marketplace]({a['listing']}): {a['description']}")
    L += ["", "## Documentation", ""]
    for a in SITE["apps"]:
        L.append(f"- [{a['name']} documentation]({a['docsHome']}): User guide for {a['name']}.")
    L += ["", "## Company", "",
          f"- [About Vudia]({BASE}/about/): Who we are, how to contact us and where to report a security issue."]
    L += ["", "## Policies", ""]
    for a in SITE["apps"]:
        L.append(f"- [{a['name']} privacy policy]({a['privacy']}): What {a['name']} reads from Jira and what it stores.")
        L.append(f"- [{a['name']} security policy]({a['security']}): How {a['name']} is built and how to report a security issue.")
    L += ["", "## Sitemap", "",
          f"- [XML sitemap]({BASE}/sitemap.xml): Every page of vudia.site.", ""]
    write("llms.txt", "\n".join(L))


if __name__ == "__main__":
    home()
    about()
    for app in SITE["apps"]:
        app_page(app)
    not_found()
    robots()
    sitemap()
    llms()
    print("built", 2 + len(SITE["apps"]), "pages + 404, robots.txt, sitemap.xml, llms.txt")
