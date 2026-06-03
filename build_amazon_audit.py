from __future__ import annotations

import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
PAGES = ROOT / "pages"
DATA_PATH = ROOT / "amazon_products.json"
HTML_PATH = ROOT / "index.html"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    ),
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
}


GROUPS = [
    (
        "Exclusive Professional",
        [
            "https://www.amazon.pl/Pripravka-Przyprawa-Staropolsku-Professional-Czarnuszk%C4%85/dp/B0GWQ6SCNR?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Naturalna-Przyprawa-Exclusive-Professional/dp/B0GWQB6141?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Przyprawa-Szaszlyk%C3%B3w-Exclusive-Professional/dp/B0GWQ1VXWY?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Exclusive-Professional-Naturalna-Przyprawa/dp/B0GWQC4PNQ?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Przyprawa-Brazylijskim-Exclusive-Professional/dp/B0GWPYCVN6?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Kurkum%C4%85-Imbirem-Exclusive-Professional/dp/B0GWPWPTHT?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Ziola-Prowansalskie-Exclusive-Professional/dp/B0GQZLRBZM?ref_=ast_sto_dp",
        ],
    ),
    (
        "Grill & BBQ",
        [
            "https://www.amazon.pl/Pripravka-Naturalna-Przyprawa-Skrzydelka-Meksyka%C5%84skie/dp/B0GWQ9Z9SH?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Przyprawa-%C5%BBeberek-Grill-BBQ/dp/B0GWQ6QD2K?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Naturalna-Przyprawa-Grill-Sycylijska/dp/B0GWQFM1RN?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Naturalna-Przyprawa-Grill-Teksa%C5%84sku/dp/B0GWPZKXXT?ref_=ast_sto_dp",
        ],
    ),
    (
        "O-o-o, Jakie ziemniaki",
        [
            "https://www.amazon.pl/Pripravka-Przyprawa-Ziemniak%C3%B3w-ZIEMNIAKI-Ameryka%C5%84ska/dp/B0GWQ69PQ4?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Przyprawa-Ziemniak%C3%B3w-Grecku-Ziemniaki/dp/B0GWQ8F15V?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Przyprawa-Ziemniak%C3%B3w-Wloskie-Czosnek/dp/B0GWQ686KL?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Przyprawa-Ziemniak%C3%B3w-Meksyka%C5%84sku-Grillowania/dp/B0GWPZJZFN?ref_=ast_sto_dp",
        ],
    ),
    (
        "Przyprawy poddane obróbce parą",
        [
            "https://www.amazon.pl/Pripravka-Ziola-Grecji-Czosnkiem-Cytrynow%C4%85/dp/B0GR11MQT5?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Ziola-Wloch-Soli-Cukru/dp/B0GR11JSQ5?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Ziola-Francji-Rozmarynem-Sterylizacja/dp/B0GR19CRFR?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Mieszanka-Przyprawowa-Pieprzem-Kolorowym/dp/B0GR5XXM78?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Pieprz-Czosnkowy-Intensywna-Sterylizacja/dp/B0GR5XX6B3?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Pieprz-Ziolowy-Intensywna-Sterylizacja/dp/B0GR62J427?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Naturalna-Przyprawa-Czosnkiem-Bazyli%C4%85/dp/B0GR5P4VHT?ref_=ast_sto_dp",
            "https://www.amazon.pl/Przyprawa-kurczaka-grill-piekarnik-grillowania/dp/B0GWQ82XSS?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Naturalna-Przyprawa-Ziemniak%C3%B3w-Sterylizacja/dp/B0GR5PP3VK?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Przyprawa-Curry-Kurkum%C4%85-Imbirem/dp/B0GR5W67KS?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Przyprawa-Kurczaka-Staropolsku-Sterylizacja/dp/B0GR5VR6VT?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Przyprawa-Mi%C4%99sa-Mielonego-Sterylizacja/dp/B0GR5SDW21?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Naturalna-Przyprawa-Mi%C4%99sa-Wieprzowego/dp/B0GR5XJ3W7?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Naturalna-Przyprawa-Ryb-Sterylizowana/dp/B0GR5XCWP7?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Naturalna-Przyprawa-Szlachetnymi-Borowikami/dp/B0GR5SLL54?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Przyprawa-Gyrosa-Kebaba-Sterylizowana/dp/B0GR5ZBCSL?ref_=ast_sto_dp",
        ],
    ),
    (
        "Sosy WOK",
        [
            "https://www.amazon.pl/Pripravka-ASIAN-Czarnym-Pieprzem-Sojowym/dp/B0GR65447J?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-CHOW-MEIN-Imbirem-Sezamem/dp/B0GR5YXV1D?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-KUNG-Pieprzem-Syczua%C5%84skim-Czosnkiem/dp/B0GR5YXJT5?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Sos-THAI-Tamaryndowcem-Imbirem/dp/B0GR634TKQ?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Spicy-Pieprzem-Timut-Chili/dp/B0GWD3S8BM?ref_=ast_sto_dp",
        ],
    ),
    (
        "Ketchup",
        [
            "https://www.amazon.pl/Pripravka-Ketchup-%C5%81agodny-Bazyli%C4%85-250/dp/B0GR662B45?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Ketchup-Oryginalny-Oliwkami-250/dp/B0GR61BRTY?ref_=ast_sto_dp",
            "https://www.amazon.pl/Pripravka-Ketchup-Musem-Bananowym-200/dp/B0GR6DLCZF?ref_=ast_sto_dp",
        ],
    ),
]

TERM_MAP = [
    ("Pripravka", "Pripravka"),
    ("Exclusive Professional", "Exclusive Professional"),
    ("Grill BBQ", "Grill BBQ"),
    ("Grill & BBQ", "Grill & BBQ"),
    ("Przyprawa", "приправа"),
    ("Naturalna", "натуральна"),
    ("Mieszanka Przyprawowa", "суміш спецій"),
    ("Mieszanka", "суміш"),
    ("Ziola", "трави"),
    ("Zioła", "трави"),
    ("Prowansalskie", "прованські"),
    ("Grecji", "Греції"),
    ("Wloch", "Італії"),
    ("Włoch", "Італії"),
    ("Francji", "Франції"),
    ("Kurczaka", "курки"),
    ("kurczaka", "курки"),
    ("Staropolsku", "по-старопольськи"),
    ("Czarnuszką", "чорнушкою"),
    ("Czarnym Pieprzem", "чорним перцем"),
    ("Pieprzem Kolorowym", "кольоровим перцем"),
    ("Pieprzem Syczuańskim", "сичуанським перцем"),
    ("Pieprzem Timut", "перцем тімут"),
    ("Pieprz Czosnkowy", "часниковий перець"),
    ("Pieprz Ziolowy", "трав'яний перець"),
    ("Czosnkiem", "часником"),
    ("Czosnkową", "часниковою"),
    ("Bazylią", "базиліком"),
    ("Cytrynową", "лимонною"),
    ("Rozmarynem", "розмарином"),
    ("Majeranek", "майоран"),
    ("Chili", "чилі"),
    ("Imbirem", "імбиром"),
    ("Kurkuma", "куркума"),
    ("Kurkumą", "куркумою"),
    ("Curry", "карі"),
    ("Szaszlyków", "шашликів"),
    ("Szaszłyków", "шашликів"),
    ("Brazylijskim", "бразильським"),
    ("Skrzydelka", "крильця"),
    ("Skrzydełka", "крильця"),
    ("Meksykańskie", "мексиканські"),
    ("Żeberek", "реберець"),
    ("Zeberek", "реберець"),
    ("Sycylijska", "сицилійська"),
    ("Teksańsku", "по-техаськи"),
    ("Ziemniaków", "картоплі"),
    ("ZIEMNIAKI", "картопля"),
    ("Amerykańska", "американська"),
    ("Grecku", "по-грецьки"),
    ("Wloskie", "італійські"),
    ("Włoskie", "італійські"),
    ("Meksykańsku", "по-мексиканськи"),
    ("Grillowania", "грилювання"),
    ("Sterylizacja", "стерилізація"),
    ("Sterylizowana", "стерилізована"),
    ("Ryb", "риби"),
    ("Mięsa Mielonego", "фаршу"),
    ("Mięsa Wieprzowego", "свинини"),
    ("Szlachetnymi Borowikami", "добірними білими грибами"),
    ("Gyrosa Kebaba", "гіроса та кебаба"),
    ("ASIAN", "ASIAN"),
    ("CHOW MEIN", "CHOW MEIN"),
    ("KUNG", "KUNG"),
    ("THAI", "THAI"),
    ("Tamaryndowcem", "тамариндом"),
    ("Sezamem", "кунжутом"),
    ("Sojowym", "соєвим"),
    ("Ketchup", "кетчуп"),
    ("Łagodny", "лагідний"),
    ("Oryginalny", "оригінальний"),
    ("Oliwkami", "оливками"),
    ("Musem Bananowym", "банановим мусом"),
    ("Soli", "солі"),
    ("Cukru", "цукру"),
]


def request_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read()


def clean_text(value: str) -> str:
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def asin_from_url(url: str) -> str:
    match = re.search(r"/dp/([A-Z0-9]{10})", url)
    return match.group(1) if match else ""


def slug_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path.strip("/").split("/dp/")[0]
    return urllib.parse.unquote(path)


def parse_page(raw: str, fallback_url: str) -> dict[str, str]:
    title = ""
    image = ""
    match = re.search(r'id="productTitle"[^>]*>(.*?)</span>', raw, re.S)
    if match:
        title = clean_text(match.group(1))
    if not title:
        match = re.search(r"<title>(.*?)</title>", raw, re.S)
        if match:
            title = clean_text(match.group(1).replace("Amazon.pl", ""))
    match = re.search(r'data-old-hires="([^"]+)"', raw)
    if match:
        image = html.unescape(match.group(1))
    if not image:
        match = re.search(r'"hiRes":"([^"]+)"', raw)
        if match:
            image = match.group(1).replace("\\/", "/")
    if not image:
        match = re.search(r'id="landingImage"[^>]+src="([^"]+)"', raw)
        if match:
            image = html.unescape(match.group(1))
    if not image:
        candidates = sorted(set(re.findall(r'https://m\.media-amazon\.com/images/I/[^"\\< ]+?\.jpg', raw)))
        preferred = [item for item in candidates if "_AC_SL1000_" in item or "_SL1000_" in item]
        if preferred:
            image = preferred[0]
        elif candidates:
            image = max(candidates, key=len)
    return {
        "title": title or slug_from_url(fallback_url).replace("-", " "),
        "image_url": image,
    }


def translate_title(title: str, slug: str) -> str:
    text = title or slug.replace("-", " ")
    for source, target in sorted(TERM_MAP, key=lambda item: len(item[0]), reverse=True):
        text = re.sub(re.escape(source), target, text, flags=re.I)
    text = re.sub(r"\b\d+\s?g\b", lambda m: m.group(0).replace("g", " г"), text, flags=re.I)
    text = re.sub(r"\b250\b", "250 г", text)
    text = re.sub(r"\s+", " ", text).strip(" -–,")
    return text


def expected_terms(title: str, category: str) -> list[str]:
    terms = ["Pripravka"]
    if "Exclusive" in category or "Exclusive" in title:
        terms.append("Exclusive")
    if "Grill" in category or "BBQ" in title:
        terms.append("Grill")
    if "Ketchup" in category or "Ketchup" in title:
        terms.append("Ketchup")
    if "Sosy" in category or re.search(r"ASIAN|CHOW|KUNG|THAI|Sos", title, re.I):
        terms.append("sos/WOK")
    return terms


def download_image(url: str, asin: str) -> str:
    if not url:
        return ""
    suffix = ".jpg"
    path = ASSETS / f"{asin}{suffix}"
    if path.exists() and path.stat().st_size > 1000:
        return f"assets/{path.name}"
    try:
        path.write_bytes(request_bytes(url))
        return f"assets/{path.name}"
    except Exception:
        return ""


def collect() -> list[dict[str, object]]:
    ASSETS.mkdir(parents=True, exist_ok=True)
    PAGES.mkdir(parents=True, exist_ok=True)
    products: list[dict[str, object]] = []
    for category, urls in GROUPS:
        for url in urls:
            asin = asin_from_url(url)
            page_path = PAGES / f"{asin}.html"
            raw = ""
            status = "ok"
            try:
                if page_path.exists() and page_path.stat().st_size > 1000:
                    raw = page_path.read_text(encoding="utf-8", errors="ignore")
                else:
                    raw_bytes = request_bytes(url)
                    page_path.write_bytes(raw_bytes)
                    raw = raw_bytes.decode("utf-8", errors="ignore")
                    time.sleep(0.4)
            except Exception as exc:
                status = f"fetch_error: {exc}"
            parsed = parse_page(raw, url) if raw else {"title": slug_from_url(url).replace("-", " "), "image_url": ""}
            image_path = download_image(parsed["image_url"], asin)
            title = parsed["title"]
            slug = slug_from_url(url)
            products.append(
                {
                    "category": category,
                    "asin": asin,
                    "url": url,
                    "slug": slug,
                    "title": title,
                    "ua_title": translate_title(title, slug),
                    "image_url": parsed["image_url"],
                    "image_path": image_path,
                    "expected_terms": expected_terms(title, category),
                    "fetch_status": status,
                }
            )
    DATA_PATH.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
    return products


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def render(products: list[dict[str, object]]) -> None:
    categories = []
    for category, _urls in GROUPS:
        items = [item for item in products if item["category"] == category]
        categories.append((category, items))

    cards_html = []
    for category, items in categories:
        cards_html.append(
            f'<section class="series" data-series="{esc(category)}">'
            f'<div class="series-head"><h2>{esc(category)}</h2><span>{len(items)} produktów</span></div>'
            '<div class="cards">'
        )
        for item in items:
            image = item.get("image_path") or ""
            image_html = (
                f'<img src="{esc(image)}" alt="{esc(item["title"])}" />'
                if image
                else '<div class="missing-image">Brak obrazu</div>'
            )
            terms = "".join(f"<span>{esc(term)}</span>" for term in item["expected_terms"])
            audit = [
                ("ASIN", bool(item["asin"]), item["asin"]),
                ("Amazon title", bool(item["title"]), "title pobrany"),
                ("Image", bool(image), "image downloaded" if image else "needs manual check"),
                ("Brand", "Pripravka" in str(item["title"]), "Pripravka in title"),
                ("Series", True, item["category"]),
            ]
            audit_html = "".join(
                f'<li class="{"ok" if ok else "warn"}"><strong>{esc(name)}</strong><span>{esc(text)}</span></li>'
                for name, ok, text in audit
            )
            cards_html.append(
                f"""
                <article class="card" data-asin="{esc(item['asin'])}" data-category="{esc(item['category'])}">
                  <div class="media">{image_html}</div>
                  <div class="content">
                    <div class="meta">
                      <span class="asin">{esc(item['asin'])}</span>
                      <span class="category">{esc(item['category'])}</span>
                    </div>
                    <h3 class="editable">{esc(item['title'])}</h3>
                    <div class="translation">
                      <span>Український переклад назви</span>
                      <p class="editable">{esc(item['ua_title'])}</p>
                    </div>
                    <div class="terms" aria-label="Ключові сигнали">{terms}</div>
                    <ul class="card-audit">{audit_html}</ul>
                    <div class="review-grid">
                      <label>Аудит Amazon-картки<textarea class="editable">Перевірити відповідність title, фото, серії, ASIN і ключових слів у назві. Дані title/image взяті зі сторінки Amazon.</textarea></label>
                      <label>Аудит перекладу<textarea class="editable">Переклад сформовано для швидкої перевірки. Ручно звірити кулінарні терміни та смакові варіанти.</textarea></label>
                    </div>
                    <a class="button" href="{esc(item['url'])}">Amazon</a>
                  </div>
                </article>
                """
            )
        cards_html.append("</div></section>")

    total = len(products)
    images = sum(1 for item in products if item.get("image_path"))
    html_doc = f"""<!doctype html>
<html lang="uk">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Pripravka Amazon Audit</title>
    <style>
      :root {{
        --ink: #171614;
        --muted: #645d53;
        --line: #ddd6c9;
        --paper: #fbfaf6;
        --panel: #fff;
        --black: #151515;
        --gold: #d6a51f;
        --green: #4f6f52;
        --red: #b94632;
        --ok: #247348;
        --warn: #a86612;
        --shadow: 0 16px 38px rgba(33, 28, 20, 0.11);
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: Arial, "Arial Unicode MS", system-ui, sans-serif;
        background: var(--paper);
        color: var(--ink);
      }}
      a {{ color: inherit; }}
      .top-strip {{ height: 12px; background: linear-gradient(90deg, var(--gold), var(--red), var(--green)); }}
      .page {{ width: min(1500px, calc(100% - 38px)); margin: 0 auto; padding: 26px 0 50px; }}
      header {{ display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 20px; align-items: end; margin-bottom: 18px; }}
      h1 {{ margin: 0; font-size: clamp(34px, 4vw, 58px); line-height: 1; letter-spacing: 0; }}
      .lead {{ max-width: 940px; margin: 10px 0 0; color: var(--muted); font-size: 18px; line-height: 1.45; }}
      .source {{ display: grid; gap: 7px; min-width: 300px; padding: 14px 16px; border: 1px solid var(--line); border-radius: 8px; background: var(--panel); color: var(--muted); font-size: 14px; }}
      .source strong {{ color: var(--ink); }}
      .controls {{ position: sticky; top: 0; z-index: 5; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 18px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: rgba(255,255,255,.94); box-shadow: 0 8px 20px rgba(31,26,18,.08); backdrop-filter: blur(10px); }}
      button, .button {{ display: inline-flex; align-items: center; justify-content: center; min-height: 42px; padding: 0 14px; border: 1px solid var(--black); border-radius: 8px; background: var(--black); color: #fff; font: inherit; font-size: 14px; font-weight: 800; text-decoration: none; cursor: pointer; }}
      button.secondary {{ border-color: var(--line); background: #fff; color: var(--ink); }}
      .status {{ margin-left: auto; color: var(--muted); font-size: 14px; font-weight: 800; }}
      .summary {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 10px; margin-bottom: 18px; }}
      .summary div {{ padding: 14px; border: 1px solid var(--line); border-radius: 8px; background: #fff; }}
      .summary span {{ display: block; color: var(--muted); font-size: 12px; font-weight: 900; text-transform: uppercase; }}
      .summary strong {{ display: block; margin-top: 4px; font-size: 28px; line-height: 1; }}
      .audit-panel {{ display: grid; gap: 8px; margin-bottom: 18px; padding: 14px 16px; border: 1px solid var(--line); border-radius: 8px; background: #fff; }}
      .audit-panel h2 {{ margin: 0; font-size: 20px; }}
      .audit-list {{ display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 8px; margin: 0; padding: 0; list-style: none; }}
      .audit-list li {{ padding: 10px 12px; border: 1px solid var(--line); border-radius: 8px; background: #faf8f2; color: var(--muted); font-size: 14px; }}
      .ok strong {{ color: var(--ok); }}
      .warn strong {{ color: var(--warn); }}
      .series {{ margin-top: 22px; }}
      .series-head {{ display: flex; gap: 12px; align-items: baseline; justify-content: space-between; margin-bottom: 10px; }}
      .series-head h2 {{ margin: 0; font-size: 28px; }}
      .series-head span {{ color: var(--muted); font-weight: 800; }}
      .cards {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 14px; }}
      .card {{ display: grid; grid-template-columns: 240px minmax(0,1fr); overflow: hidden; border: 1px solid var(--line); border-radius: 8px; background: var(--panel); box-shadow: var(--shadow); }}
      .media {{ display: grid; place-items: center; min-height: 260px; padding: 18px; border-right: 1px solid var(--line); background: linear-gradient(180deg, #fff, #f3efe8); }}
      .media img {{ width: 100%; max-height: 250px; object-fit: contain; mix-blend-mode: multiply; }}
      .missing-image {{ display: grid; place-items: center; width: 100%; min-height: 180px; border: 1px dashed var(--line); border-radius: 8px; color: var(--muted); font-weight: 800; }}
      .content {{ display: grid; gap: 12px; padding: 16px; }}
      .meta {{ display: flex; flex-wrap: wrap; gap: 8px; }}
      .meta span, .terms span {{ display: inline-flex; align-items: center; min-height: 28px; padding: 5px 9px; border-radius: 999px; font-size: 12px; font-weight: 900; }}
      .asin {{ background: var(--black); color: #fff; }}
      .category, .terms span {{ border: 1px solid var(--line); background: #faf8f2; color: var(--ink); }}
      h3 {{ margin: 0; font-size: 19px; line-height: 1.25; letter-spacing: 0; }}
      .translation {{ padding: 11px 12px; border: 1px solid var(--line); border-radius: 8px; background: #fcfaf5; }}
      .translation span, label {{ display: block; margin-bottom: 6px; color: var(--muted); font-size: 11px; font-weight: 900; text-transform: uppercase; }}
      .translation p {{ margin: 0; line-height: 1.35; }}
      .terms {{ display: flex; flex-wrap: wrap; gap: 6px; }}
      .card-audit {{ display: grid; grid-template-columns: repeat(5, minmax(0,1fr)); gap: 6px; margin: 0; padding: 0; list-style: none; }}
      .card-audit li {{ min-height: 54px; padding: 8px; border: 1px solid var(--line); border-radius: 8px; background: #fff; }}
      .card-audit strong, .card-audit span {{ display: block; font-size: 12px; line-height: 1.2; }}
      .card-audit span {{ margin-top: 4px; color: var(--muted); }}
      .review-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 8px; }}
      textarea {{ width: 100%; min-height: 82px; resize: vertical; padding: 10px; border: 1px solid var(--line); border-radius: 8px; font: inherit; color: var(--ink); background: #fff; }}
      body.editing .editable {{ outline: 2px dashed rgba(214,165,31,.75); outline-offset: 3px; }}
      body.editing [contenteditable="true"]:focus, body.editing textarea:focus {{ outline: 3px solid var(--gold); background: #fffdf4; }}
      footer {{ margin-top: 24px; color: var(--muted); font-size: 13px; line-height: 1.45; }}
      @media (max-width: 1100px) {{ header, .cards, .summary {{ grid-template-columns: 1fr; }} .source {{ min-width: 0; }} }}
      @media (max-width: 680px) {{ .page {{ width: min(100% - 28px, 760px); }} .controls {{ position: static; }} .status {{ flex-basis: 100%; margin-left: 0; }} .card {{ grid-template-columns: 1fr; }} .media {{ border-right: 0; border-bottom: 1px solid var(--line); }} .card-audit, .review-grid, .audit-list {{ grid-template-columns: 1fr; }} }}
    </style>
  </head>
  <body>
    <div class="top-strip" aria-hidden="true"></div>
    <main class="page">
      <header>
        <div>
          <h1>Pripravka Amazon Audit</h1>
          <p class="lead">Окремий ресурс для перевірки Amazon-карток Pripravka: title, ASIN, фото, серія, переклад українською і ручні поля аудиту.</p>
        </div>
        <aside class="source">
          <strong>Źródło: Amazon.pl</strong>
          <span>Перевірено: 2026-06-03</span>
          <span>Товарів у списку: {total}</span>
          <span>Фото завантажено: {images}</span>
        </aside>
      </header>
      <section class="controls">
        <button id="editToggle" type="button">Увімкнути редагування</button>
        <button class="secondary" id="runAudit" type="button">Провести аудит</button>
        <button class="secondary" id="exportHtml" type="button">Експортувати HTML</button>
        <button class="secondary" id="resetEdits" type="button">Скинути правки</button>
        <button class="secondary" type="button" onclick="window.print()">Друк / PDF</button>
        <span class="status" id="status">Режим перегляду</span>
      </section>
      <section class="summary">
        <div><span>Amazon URLs</span><strong>{total}</strong></div>
        <div><span>Images</span><strong>{images}</strong></div>
        <div><span>Series</span><strong>{len(categories)}</strong></div>
        <div><span>Editable fields</span><strong id="editableCount">0</strong></div>
      </section>
      <section class="audit-panel">
        <h2>Загальний аудит</h2>
        <ul class="audit-list" id="auditList"></ul>
      </section>
      {''.join(cards_html)}
      <footer>Дані title/image отримані зі сторінок Amazon.pl. Поля аудиту та перекладу редагуються у браузері, зміни зберігаються у localStorage; кнопка експорту створює автономний HTML із поточними правками.</footer>
    </main>
    <script>
      const storageKey = "pripravka-amazon-audit-v1";
      const editableNodes = [...document.querySelectorAll(".editable")];
      const statusNode = document.querySelector("#status");
      const editToggle = document.querySelector("#editToggle");
      const editableCount = document.querySelector("#editableCount");
      editableCount.textContent = editableNodes.length;

      function setEditing(enabled) {{
        document.body.classList.toggle("editing", enabled);
        editableNodes.forEach((node) => {{
          if (node.tagName === "TEXTAREA") {{
            node.readOnly = !enabled;
          }} else {{
            node.contentEditable = String(enabled);
            node.spellcheck = true;
          }}
        }});
        editToggle.textContent = enabled ? "Вимкнути редагування" : "Увімкнути редагування";
        statusNode.textContent = enabled ? "Режим редагування" : "Режим перегляду";
      }}

      function saveEdits() {{
        const payload = editableNodes.map((node) => node.tagName === "TEXTAREA" ? node.value : node.innerHTML);
        localStorage.setItem(storageKey, JSON.stringify(payload));
        statusNode.textContent = document.body.classList.contains("editing") ? "Правки збережено" : "Режим перегляду";
      }}

      function loadEdits() {{
        const raw = localStorage.getItem(storageKey);
        if (!raw) return;
        try {{
          const payload = JSON.parse(raw);
          editableNodes.forEach((node, index) => {{
            if (typeof payload[index] !== "string") return;
            if (node.tagName === "TEXTAREA") node.value = payload[index];
            else node.innerHTML = payload[index];
          }});
        }} catch {{
          localStorage.removeItem(storageKey);
        }}
      }}

      function hasCyrillic(text) {{ return /[А-Яа-яІіЇїЄєҐґ]/.test(text); }}

      function audit() {{
        const cards = [...document.querySelectorAll(".card")];
        const images = [...document.images];
        const loadedImages = images.filter((img) => img.complete && img.naturalWidth > 0);
        const titles = [...document.querySelectorAll(".card h3")];
        const uaTitles = [...document.querySelectorAll(".translation p")];
        const emptyEditable = editableNodes.filter((node) => (node.tagName === "TEXTAREA" ? node.value : node.textContent).trim().length === 0);
        const missingPripravka = titles.filter((node) => !/Pripravka/i.test(node.textContent));
        const missingUa = uaTitles.filter((node) => !hasCyrillic(node.textContent));
        const items = [
          ["Amazon URLs", cards.length === {total}, `Знайдено ${{cards.length}} з {total} карток.`],
          ["Images", loadedImages.length === images.length && images.length === {images}, `Завантажено ${{loadedImages.length}} з ${{images.length}} локальних фото.`],
          ["Titles", titles.length === {total} && missingPripravka.length === 0, `Title-полів: ${{titles.length}}; без Pripravka: ${{missingPripravka.length}}.`],
          ["UA translation", uaTitles.length === {total} && missingUa.length === 0, `Українських перекладів: ${{uaTitles.length}}; без кирилиці: ${{missingUa.length}}.`],
          ["Editable fields", editableNodes.length > {total}, `Редагованих полів: ${{editableNodes.length}}.`],
          ["Empty fields", emptyEditable.length === 0, `Порожніх редагованих полів: ${{emptyEditable.length}}.`],
        ];
        document.querySelector("#auditList").innerHTML = items
          .map(([name, ok, text]) => `<li class="${{ok ? "ok" : "warn"}}"><strong>${{ok ? "OK" : "Увага"}} - ${{name}}</strong><span>${{text}}</span></li>`)
          .join("");
        statusNode.textContent = items.every(([, ok]) => ok) ? "Аудит пройдено" : "Аудит має попередження";
      }}

      function exportHtml() {{
        const clone = document.documentElement.cloneNode(true);
        clone.querySelectorAll("[contenteditable]").forEach((node) => node.removeAttribute("contenteditable"));
        clone.querySelector("body").classList.remove("editing");
        const blob = new Blob(["<!doctype html>\\n" + clone.outerHTML], {{ type: "text/html;charset=utf-8" }});
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "pripravka-amazon-audit-edited.html";
        link.click();
        URL.revokeObjectURL(link.href);
      }}

      loadEdits();
      setEditing(false);
      audit();
      window.addEventListener("load", audit);
      document.querySelectorAll("img").forEach((img) => img.addEventListener("load", audit));
      document.querySelector("#runAudit").addEventListener("click", audit);
      document.querySelector("#exportHtml").addEventListener("click", exportHtml);
      document.querySelector("#resetEdits").addEventListener("click", () => {{ localStorage.removeItem(storageKey); location.reload(); }});
      editToggle.addEventListener("click", () => setEditing(!document.body.classList.contains("editing")));
      editableNodes.forEach((node) => node.addEventListener("input", saveEdits));
    </script>
  </body>
</html>
"""
    HTML_PATH.write_text(html_doc, encoding="utf-8")


def main() -> None:
    products = collect()
    render(products)
    print(f"products={len(products)}")
    print(f"images={sum(1 for item in products if item.get('image_path'))}")
    print(HTML_PATH)


if __name__ == "__main__":
    main()
