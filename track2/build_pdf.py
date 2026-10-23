#!/usr/bin/env python3
"""Renderiza track2_report.md -> hysa_track2_report.pdf (Markdown -> HTML -> WeasyPrint).
Uso: python3 build_pdf.py            (desde track2/)  ·  requiere: markdown, weasyprint (en el venv)"""
import os, re, sys
import markdown
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "track2_report.md")
OUT  = os.path.join(HERE, "hysa_track2_report.pdf")

md = open(SRC, encoding="utf-8").read()
body = markdown.markdown(md, extensions=["tables", "sane_lists", "fenced_code", "attr_list"])

# imagen sola en un párrafo -> <figure> con epígrafe tomado del alt
def fig(m):
    alt, src = m.group(1), m.group(2)
    return f'<figure><img src="{src}" alt="{alt}"/><figcaption>{alt}</figcaption></figure>'
body = re.sub(r'<p><img alt="([^"]*)" src="([^"]*)" ?/?></p>', fig, body)

CSS = """
@page { size: A4; margin: 17mm 15mm 19mm 15mm;
  @top-right { content: "Track 2 — Drug Repurposing Report · PROBAND01"; font-size: 7.5pt; color: #7b8794; }
  @bottom-center { content: counter(page) " / " counter(pages); font-size: 8pt; color: #7b8794; } }
html { font-family: "DejaVu Sans", "Liberation Sans", Arial, sans-serif; font-size: 9.4pt; color: #1f2933; }
body { line-height: 1.42; }
h1 { font-size: 20pt; margin: 0 0 1pt; letter-spacing: -0.2pt; }
h3:first-of-type { font-size: 10.5pt; font-weight: 600; color: #52606d; margin: 0 0 10pt; }
h2 { font-size: 13.5pt; margin: 17pt 0 5pt; padding-bottom: 3pt; border-bottom: 1.4pt solid #cbd2d9; page-break-after: avoid; }
h3 { font-size: 10.8pt; margin: 11pt 0 3pt; page-break-after: avoid; }
p { margin: 4pt 0 5pt; orphans: 3; widows: 3; }
ul, ol { margin: 3pt 0 5pt 16pt; padding: 0; } li { margin: 1.5pt 0; }
hr { border: none; border-top: 0.8pt solid #e4e7eb; margin: 12pt 0; }
blockquote { margin: 7pt 0; padding: 5pt 9pt; background: #fff7e8; border-left: 3pt solid #d97706; color: #3e4c59; }
blockquote p { margin: 2pt 0; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.2pt; background: #f1f3f5; padding: 0 2pt; border-radius: 2pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 9pt; font-size: 7.9pt; line-height: 1.3; }
th { background: #eef1f4; text-align: left; font-weight: 700; }
th, td { border: 0.6pt solid #cbd2d9; padding: 2.6pt 4pt; vertical-align: top; }
tr { break-inside: avoid; }
table { break-inside: auto; }
figure { margin: 8pt 0 10pt; page-break-inside: avoid; text-align: center; }
figure img { max-width: 100%; max-height: 150mm; }
figcaption { font-size: 7.8pt; color: #52606d; margin-top: 3pt; font-style: italic; }
strong { font-weight: 700; } a { color: #0b69a3; text-decoration: none; }
"""
html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Track 2 — Drug Repurposing Report</title><style>{CSS}</style></head><body>{body}</body></html>'
open(os.path.join(HERE, "_report_preview.html"), "w", encoding="utf-8").write(html)
HTML(string=html, base_url=HERE).write_pdf(OUT)
print("OK ->", OUT)
