#!/usr/bin/env python3
"""Turn the two legal markdown files into pages on ije.life.

The markdown on the Desktop is the source of truth. Editing HTML by hand
means the site and the document you send a lawyer drift apart, and the one
people can read is the one that is wrong.

  python3 build-legal.py           # writes site/terms/ and site/privacy/

Requires: pip install markdown
"""
import os
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.expanduser("~/Desktop")

DOCS = [
    ("Ije - Terms and Conditions.md", "terms", "Terms &amp; Conditions",
     "The agreement between you and Ije when you apply or pay for a seat."),
    ("Ije - Privacy Policy.md", "privacy", "Privacy Policy",
     "What we collect when you apply to Ije, why, and what rights you have over it."),
]

# Lifted from index.html so the legal pages read as the same website. Same
# palette, same Outfit, same wobbly-radius button. Deliberately narrower
# measure than the landing page: this is long prose, not a pitch.
TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%2310322e'/%3E%3Ctext x='32' y='42' font-family='Helvetica,Arial,sans-serif' font-size='26' font-weight='bold' letter-spacing='-1' fill='%23c6d94e' text-anchor='middle'%3Eije%3C/text%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ije &middot; {title}</title>
<meta name="description" content="{blurb}">
<meta name="robots" content="index,follow">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{{
    --ground:#f4f3ef; --surface:#eae9e3; --ink:#191a1c; --ink-soft:#5b5d60;
    --green:#10322e; --green-soft:#17453e; --green-mid:#2e6f61; --lime:#c6d94e;
  }}
  *{{margin:0;padding:0;box-sizing:border-box}}
  html{{scroll-behavior:smooth}}
  body{{background:var(--ground);color:var(--ink);font-family:Outfit,sans-serif;
    font-size:17px;line-height:1.7;-webkit-font-smoothing:antialiased}}
  a{{color:var(--green);text-decoration:underline;text-underline-offset:3px}}
  a:hover{{color:var(--green-mid)}}
  a:focus-visible{{outline:3px solid var(--green);outline-offset:4px;border-radius:6px}}
  .wrap{{max-width:720px;margin:0 auto;padding:0 26px}}

  header{{background:var(--green);color:var(--ground);padding:26px 0 60px}}
  header .wrap{{display:flex;flex-direction:column;gap:34px}}
  .home{{color:var(--lime);text-decoration:none;font-weight:700;letter-spacing:-.5px;
    font-size:20px;align-self:flex-start}}
  .home:hover{{color:var(--ground)}}
  header h1{{font-size:clamp(34px,7vw,52px);line-height:1.05;letter-spacing:-1.5px;font-weight:800}}
  header p{{color:#cfd8d3;max-width:46ch}}

  main{{padding:0 0 90px}}
  .card{{background:var(--surface);margin-top:-34px;border-radius:26px 22px 26px 22px;
    padding:44px 40px 48px}}
  .card p{{margin:0 0 20px}}
  .card p:last-child{{margin-bottom:0}}
  .card strong{{font-weight:700}}
  .card em{{color:var(--ink-soft);font-style:normal;font-size:15px}}
  .card h1{{display:none}}

  .back{{display:inline-flex;align-items:center;justify-content:center;min-height:54px;
    margin-top:34px;background:var(--green);color:#f4f3ef;text-decoration:none;
    font-weight:600;font-size:18px;padding:15px 34px;border-radius:34px 30px 32px 28px;
    transition:transform .18s ease,background .18s ease}}
  .back:hover{{background:var(--green-soft);transform:translateY(-2px);color:#f4f3ef}}

  .other{{margin-top:30px;color:var(--ink-soft);font-size:16px}}

  footer{{border-top:1px solid #dcdad3;padding:26px 0 40px;color:var(--ink-soft);font-size:15px;
    display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}}

  @media(max-width:620px){{
    .card{{padding:34px 24px 38px;border-radius:22px}}
    header{{padding-bottom:52px}}
  }}
</style>
</head>
<body>

<header>
  <div class="wrap">
    <a class="home" href="/">IJE&reg;</a>
    <div>
      <h1>{title}</h1>
      <p>{blurb}</p>
    </div>
  </div>
</header>

<main class="wrap">
  <article class="card">
{body}
  </article>
  <p class="other">{other}</p>
  <a class="back" href="/">Back to Ije</a>
</main>

<div class="wrap">
  <footer>
    <span>IJE&reg;</span>
    <span>Lagos, for now.</span>
  </footer>
</div>

</body>
</html>
"""

OTHER = {
    "terms": 'Also worth reading: our <a href="/privacy">Privacy Policy</a>, which forms part of these terms.',
    "privacy": 'Also worth reading: our <a href="/terms">Terms &amp; Conditions</a>.',
}

def build():
    for filename, slug, title, blurb in DOCS:
        path = os.path.join(SRC, filename)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        body = markdown.markdown(text)
        # hello@ije.life appears a dozen times in each document and is the only
        # way to exercise a right under either. Make every one of them clickable.
        body = body.replace("hello@ije.life",
                            '<a href="mailto:hello@ije.life">hello@ije.life</a>')
        body = "\n".join("    " + line for line in body.splitlines())
        out_dir = os.path.join(HERE, slug)
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, "index.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(TEMPLATE.format(title=title, blurb=blurb, body=body,
                                    other=OTHER[slug]))
        print(f"{filename}  ->  site/{slug}/index.html  ({len(body):,} bytes)")

if __name__ == "__main__":
    build()
