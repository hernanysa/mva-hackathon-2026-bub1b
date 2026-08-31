#!/usr/bin/env python3
"""Figura resumen: las 2 variantes bialelicas sobre la proteina BUBR1 (BUB1B, 1050 aa)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

L = 1050
# dominios BUBR1 (UniProt O60566, aprox)
DOMS = [
    (26, 43,   "KEN1",            "#c7d8e6"),
    (150, 350, "Mad3/BUB1 hom.",  "#a9c7e0"),
    (407, 431, "GLEBS\n(BUB3)",   "#7fb2d6"),
    (766, 1040,"dominio quinasa", "#4a90c4"),
]
VARS = [
    (737,  "p.Leu737Ter\nc.2210T>G  (rs759242053)\nnonsense · ClinVar Patogénica\ngnomAD 8e-5", "#b23b3b"),
    (1002, "p.Asn1002Lys\nc.3006T>G  (novel)\nmissense · SIFT/PolyPhen/AlphaMissense dañino\nausente de gnomAD", "#7a3ea8"),
]

fig, ax = plt.subplots(figsize=(12, 4.2))
ax.set_xlim(-30, L + 30)
ax.set_ylim(-2.6, 3.2)
ax.axis("off")

# backbone
ax.add_patch(Rectangle((0, -0.28), L, 0.56, fc="#e9e9ec", ec="#8a8a8a", lw=1))
for a, b, name, col in DOMS:
    ax.add_patch(Rectangle((a, -0.28), b - a, 0.56, fc=col, ec="#3a6f96", lw=0.8))
    ax.text((a + b) / 2, 0, name, ha="center", va="center", fontsize=8, color="#10314a")
for x in (0, 200, 400, 600, 800, 1000, L):
    ax.plot([x, x], [-0.28, -0.42], color="#8a8a8a", lw=0.8)
    ax.text(x, -0.62, str(x), ha="center", va="top", fontsize=7, color="#555")
ax.text(L / 2, -1.25, "BUBR1  ·  BUB1B  ·  NM_001211.6 / ENST00000287598.11  ·  1050 aa",
        ha="center", fontsize=8.5, style="italic", color="#333")

# lollipops
for pos, label, col in VARS:
    ax.plot([pos, pos], [0.28, 1.7], color=col, lw=1.6)
    ax.plot(pos, 1.7, "o", ms=13, color=col)
    ax.text(pos, 1.95, label, ha="center", va="bottom", fontsize=8, color=col)

ax.text(-30, 2.95, "Probando WGS_EX2312012 — heterocigota compuesta en BUB1B → MVA1",
        fontsize=11, fontweight="bold", color="#1a1a1a")
ax.annotate("trunca el dominio quinasa completo", xy=(737, 0.28), xytext=(690, -1.9),
            fontsize=7.5, color="#b23b3b", ha="center",
            arrowprops=dict(arrowstyle="->", color="#b23b3b", lw=0.9))
ax.annotate("residuo dentro del dominio quinasa", xy=(1002, 0.28), xytext=(1002, -1.9),
            fontsize=7.5, color="#7a3ea8", ha="center",
            arrowprops=dict(arrowstyle="->", color="#7a3ea8", lw=0.9))

fig.tight_layout()
fig.savefig("analisis/out/figura_bub1b.png", dpi=140, bbox_inches="tight")
print("-> analisis/out/figura_bub1b.png")
