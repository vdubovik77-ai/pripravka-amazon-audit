# Pripravka Amazon Audit

Static HTML audit page for Pripravka Amazon product cards with local package images, Polish OCR text, and Ukrainian translations.

Public page:
https://vdubovik77-ai.github.io/pripravka-amazon-audit/

## Project Files

- `index.html` - final public HTML page served by GitHub Pages.
- `assets/` - local product package images used by the page.
- `amazon_products.json` - structured product data and Amazon URLs.
- `build_product_cards.py` - current generator for the final product-card HTML.
- `build_amazon_audit.py` - helper script used during Amazon audit preparation.
- `pages/` - cached Amazon product HTML pages used for audit/reference.
- `contact-sheets/` - visual contact sheets for checking image-to-ASIN coverage.
- `audit.md` - audit notes, validation results, and correction log.

## Rebuild

From the repository root:

```bash
python3 build_product_cards.py
```

The generated `index.html` is the page published by GitHub Pages.
