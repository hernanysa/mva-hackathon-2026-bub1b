#!/usr/bin/env python3
"""Figuras del report de Track 2. Genera track2/figures/:
  fig1_mechanism.svg   — un defecto, dos ejes, dónde está el espacio farmacológico (SVG a mano)
  fig2_druggability.png— C10: checkpoint = esencial y sin fármacos; dianas río abajo = drogadas (datos c10_opentargets.json)
  fig3_signature.png   — C4: volcano de GSE277997 (BubR1 hipomórfico, corazón) con los genes de los dos ejes
  fig4_convergence.png — matriz candidato × línea de evidencia
Datos: repurposing/c10_opentargets.json, repurposing/data/c4_geo/GSE277997_H_v_WT.csv.gz
"""
import os, json, gzip, csv, math
from xml.sax.saxutils import escape
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "..", "investigacion", "repurposing")
OUT = os.path.join(HERE, "figures"); os.makedirs(OUT, exist_ok=True)

# paleta (daltonismo-segura, tipo Okabe-Ito) — mismos roles en todas las figuras
TEAL, ORANGE, RED, GREY, INK, BLUE, PURPLE = "#009E73", "#E69F00", "#D55E00", "#9AA0A6", "#1F2933", "#0072B2", "#8E5BA8"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#5F6B76",
                     "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK, "ytick.color": INK,
                     "axes.spines.top": False, "axes.spines.right": False})

# ======================================================= FIG 1 — SVG a mano
def fig1():
    W, H = 920, 600
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="DejaVu Sans, Arial, sans-serif" font-size="13">',
           '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
           '<path d="M0,0 L10,5 L0,10 z" fill="#5F6B76"/></marker></defs>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    def box(x, y, w, h, lines, fill, stroke, bold=False, color=INK, fs=13, fs2=None):
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
        n = len(lines); lh = fs + 4
        y0 = y + h/2 - (n-1)*lh/2 + fs/2 - 2
        for i, t in enumerate(lines):
            wt = ' font-weight="700"' if (bold and i == 0) else ''
            f_ = fs2 if (fs2 and i > 0) else fs
            svg.append(f'<text x="{x+w/2}" y="{y0+i*lh}" text-anchor="middle" fill="{color}" font-size="{f_}"{wt}>{escape(t)}</text>')
    def arrow(x1, y1, x2, y2, dashed=False, col="#5F6B76"):
        d = ' stroke-dasharray="5 4"' if dashed else ''
        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="1.8"{d} marker-end="url(#a)"/>')
    def label(x, y, t, col="#5F6B76", anchor="middle", fs=11.5, italic=True):
        st = ' font-style="italic"' if italic else ''
        svg.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{col}" font-size="{fs}"{st}>{escape(t)}</text>')

    svg.append(f'<text x="{W/2}" y="26" text-anchor="middle" font-size="15" font-weight="700" fill="{INK}">'
               'One defect, two consequences, two therapeutic axes</text>')
    # raíz y BUBR1
    box(250, 44, 420, 52, ["BUB1B biallelic loss of function", "L737* (null)  +  N1002K (hypomorph)"], "#EEF1F4", "#5F6B76", bold=True)
    arrow(460, 96, 460, 124)
    box(240, 126, 440, 56, ["BUBR1 deficient — checkpoint complex weakened", "(spindle-assembly checkpoint)"], "#EEF1F4", "#5F6B76", bold=True, fs=12.5)
    arrow(380, 182, 232, 224); arrow(540, 182, 688, 224)
    # eje 1 (izquierda)
    box(40, 226, 380, 54, ["AXIS 1 — chromosome missegregation", "mosaic aneuploidy"], "#E3F4EE", TEAL, bold=True)
    arrow(230, 280, 230, 306)
    box(40, 308, 380, 54, ["Tumour predisposition", "reported: rhabdomyosarcoma · Wilms tumour"], "#F3FAF7", TEAL)
    arrow(230, 362, 230, 388)
    box(40, 390, 380, 66, ["Aneuploid cells depend on AMPK / proteostasis", "→ exploit the metabolic & proteotoxic stress"], "#F3FAF7", TEAL)
    arrow(230, 456, 230, 478)
    box(40, 480, 380, 62, ["METFORMIN", "AMPK · precedent in Fanconi anaemia (6–35 y)"], "#009E73", "#007a5a", bold=True, color="#ffffff", fs=13.5, fs2=11.5)
    # eje 2 (derecha)
    box(500, 226, 380, 54, ["AXIS 2 — BUBR1 insufficiency", "accelerated senescence (p21 / p15 / p16, SASP)"], "#FDF1D6", ORANGE, bold=True)
    arrow(690, 280, 690, 306)
    box(500, 308, 380, 54, ["Progeroid features", "IUGR · failure to thrive · muscle atrophy"], "#FEF8EA", ORANGE)
    arrow(690, 362, 690, 388)
    box(500, 390, 380, 66, ["Senescent cells accumulate — proof of concept", "in the BubR1 hypomorph mouse (Baker 2011)", "→ senolysis"], "#FEF8EA", ORANGE, fs=12.5)
    arrow(690, 456, 690, 478)
    box(500, 480, 380, 62, ["FISETIN", "adult regimen · no paediatric trial"], "#E69F00", "#b87f00", bold=True, color="#1F2933", fs=13.5, fs2=11.5)
    # NR upstream
    box(716, 120, 168, 62, ["NR  (adjuvant)", "NAD⁺ → SIRT2 → BUBR1"], "#EAF1FA", BLUE, bold=True, fs=11.5)
    arrow(716, 151, 682, 151, dashed=True, col=BLUE)
    label(800, 202, "raises residual BUBR1? (pre-clinical)", col=BLUE, fs=10.5)
    # checkpoint no es diana
    box(20, 118, 214, 76, ["The checkpoint is not a target", "pan-essential · 0 drugs", "(Open Targets / DepMap)"], "#FBE9E1", RED, bold=True, fs=11.5)
    arrow(234, 156, 238, 156, col=RED)
    # vigilancia
    box(110, 560, 700, 28, ["Tumour surveillance: renal ultrasound every 3 months, birth to age 7 (all MVA types) — independent of all agents"],
        "#F5F6F8", "#B8BFC7", fs=11)
    svg.append('</svg>')
    open(os.path.join(OUT, "fig1_mechanism.svg"), "w", encoding="utf-8").write("\n".join(svg))
    print("fig1_mechanism.svg")

# ======================================================= FIG 2 — druggability (C10)
def fig2():
    d = json.load(open(os.path.join(REPO, "c10_opentargets.json")))
    dis = [r for r in d["disease_side"] if r["sym"] in ("BUB1B", "BUB1", "MAD2L1", "CDC20", "TTK", "AURKB")]
    dis.sort(key=lambda r: r["dep_median"])      # más esencial arriba
    EN = {"PRKAA1": "AMPK-α1 · metformin", "PRKAA2": "AMPK-α2 · metformin", "MTOR": "rapamycin",
          "BCL2": "navitoclax", "BCL2L1": "BCL-xL · navitoclax", "HSP90AA1": "17-AAG (control)",
          "NAMPT": "NAD⁺ salvage · NR", "PTGS2": "COX-2 · aspirin", "SIRT1": "fisetin, NR"}
    tg = [r for r in d["drug_targets"] if r["sym"] in EN]
    tg.sort(key=lambda r: -r["n_drugs"])
    fig, (a, b) = plt.subplots(2, 1, figsize=(7.8, 7.7), gridspec_kw={"height_ratios": [6, 9.2], "hspace": 0.58})
    # panel A
    ys = np.arange(len(dis))
    cols = [RED if r["sym"] == "BUB1B" else "#E8A98C" for r in dis]
    a.barh(ys, [r["dep_median"] for r in dis], color=cols, height=0.62)
    a.axvline(-1, color=INK, ls="--", lw=1)
    a.text(-1.04, -0.78, "−1 = common-essential benchmark", ha="right", va="center", fontsize=8.8, color=INK)
    a.set_yticks(ys); a.set_yticklabels([r["sym"] for r in dis]); a.set_ylim(len(dis) - 0.4, -1.05)
    for lab in a.get_yticklabels():
        if lab.get_text() == "BUB1B": lab.set_fontweight("bold")
    for y, r in zip(ys, dis):
        n = r["drugs"]; a.text(0.07, y, f"{n} drug{'s' if n != 1 else ''}", va="center", ha="left", fontsize=10,
                               color=INK, fontweight="bold" if n == 0 else "normal")
    a.set_xlim(-3.3, 1.0); a.set_xticks([-3, -2, -1, 0]); a.spines["bottom"].set_bounds(-3.3, 0)
    a.set_xlabel("DepMap median CRISPR gene effect\n(more negative = more essential)")
    a.set_title("A  The checkpoint: essential, and undrugged", loc="left", fontsize=10.6, fontweight="bold")
    a.text(-3.25, 4.55, "AURKB / TTK 'drugs':\ncytotoxic Aurora /\nMPS1 inhibitors", fontsize=8.8, color="#5F6B76", va="center")
    # panel B
    ys = np.arange(len(tg))
    cols = [TEAL if r["gen_support_cancer"] >= 0.1 else GREY for r in tg]
    b.barh(ys, [r["n_drugs"] for r in tg], color=cols, height=0.62)
    b.set_yticks(ys); b.set_yticklabels([f"{r['sym']}  ({EN[r['sym']]})" for r in tg], fontsize=9.6); b.invert_yaxis()
    for y, r in zip(ys, tg):
        n = r["n_drugs"]; t = f"{n} drug{'s' if n != 1 else ''}"
        if r["gen_support_cancer"] >= 0.1: t += f"  ·  neoplasia genetic support {r['gen_support_cancer']:.2f}"
        b.text(n + 1.2, y, t, va="center", fontsize=9.4, color=INK)
    b.set_xlim(0, 140); b.set_xlabel("Drugs / clinical candidates in Open Targets")
    b.set_title("B  The downstream targets: drugged, and (teal) genetically supported in human neoplasia", loc="left", fontsize=10.6, fontweight="bold")
    b.legend(handles=[Line2D([0],[0], marker="s", ls="", color=TEAL, label="human genetic support for neoplasia ≥ 0.1"),
                      Line2D([0],[0], marker="s", ls="", color=GREY, label="none / not for neoplasia")],
             loc="upper center", bbox_to_anchor=(0.30, -0.13), ncol=2, fontsize=9.2, frameon=False)
    fig.savefig(os.path.join(OUT, "fig2_druggability.png"), dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print("fig2_druggability.png")

# ======================================================= FIG 3 — volcano GSE277997 (C4)
def fig3():
    xs, ys, names, pads = [], [], [], []
    with gzip.open(os.path.join(REPO, "data", "c4_geo", "GSE277997_H_v_WT.csv.gz"), "rt") as f:
        for r in csv.DictReader(f):
            try: lf, pa = float(r["log2FC"]), float(r["padj"])
            except (ValueError, TypeError): continue
            xs.append(lf); ys.append(-math.log10(max(pa, 1e-300))); names.append(r["gene"]); pads.append(pa)
    xs, ys = np.array(xs), np.array(ys)
    SEN = {"Cdkn1a", "Cdkn2a", "Cdkn2b", "Timp1"}; BOTH = {"Gdf15"}
    sig = (ys > -math.log10(0.05)) & (np.abs(xs) > 0.585)
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    ax.scatter(xs[~sig], ys[~sig], s=6, c="#D5DAE0", lw=0, rasterized=True)
    ax.scatter(xs[sig], ys[sig], s=9, c=GREY, lw=0, rasterized=True)
    # (dx, dy, ha, flecha?)
    pos = {"Cdkn1a": (8, 5, "left", False), "Cdkn2b": (9, -3, "left", False), "Timp1": (-8, 8, "right", False),
           "Gdf15": (8, 6, "left", False), "Fgf21": (-8, 8, "right", False), "Trib3": (-12, 9, "right", True),
           "Ddit3": (-26, 20, "right", True), "Chac1": (22, 32, "left", True), "Cdkn2a": (52, -2, "left", True)}
    for g, (dx, dy, ha, arr) in pos.items():
        i = names.index(g)
        c = PURPLE if g in BOTH else (ORANGE if g in SEN else TEAL)
        ax.scatter(xs[i], ys[i], s=48, c=c, edgecolor="white", lw=0.8, zorder=5)
        ax.annotate(g, (xs[i], ys[i]), xytext=(dx, dy), textcoords="offset points", ha=ha, va="center", fontsize=8.8,
                    color=c, fontweight="bold", zorder=6,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85),
                    arrowprops=dict(arrowstyle="-", lw=0.7, color=c) if arr else None)
    j = names.index("Jmjd7"); ax.annotate("Jmjd7", (xs[j], ys[j]), xytext=(8, -4), textcoords="offset points", fontsize=7.6, color="#5F6B76")
    ax.text(-0.9, 15.2, "streak: 165 genes share\nlog2FC ≈ ±0.81 (a feature of the\ndeposited table; not interpreted)", fontsize=7.2,
            color="#5F6B76", ha="right", va="bottom")
    ax.axvline(0.585, color="#B8BFC7", lw=0.8, ls=":"); ax.axvline(-0.585, color="#B8BFC7", lw=0.8, ls=":")
    ax.axhline(-math.log10(0.05), color="#B8BFC7", lw=0.8, ls=":")
    ax.set_xlabel("log2 fold-change  (BubR1 hypomorph vs wild-type)"); ax.set_ylabel("−log10 adjusted p")
    ax.set_title("BubR1-insufficient mouse heart (GSE277997)", loc="left", fontsize=10, fontweight="bold")
    ax.legend(handles=[Line2D([0],[0], marker="o", ls="", color=ORANGE, label="senescence / SASP"),
                       Line2D([0],[0], marker="o", ls="", color=TEAL, label="integrated stress / mitochondrial"),
                       Line2D([0],[0], marker="o", ls="", color=PURPLE, label="both (Gdf15)")],
              loc="upper right", fontsize=8.3, frameon=False)
    ax.text(1.35, 22.5, "Cdkn2a, Ddit3 and Chac1 pass the\nthreshold narrowly (padj 0.03–0.05);\nthe other labelled genes strongly\n(padj ≤ 1.5×10⁻⁵)", fontsize=7.6,
            color="#5F6B76", ha="left", va="top")
    fig.savefig(os.path.join(OUT, "fig3_signature.png"), dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print("fig3_signature.png")

# ======================================================= FIG 4 — matriz de convergencia
def fig4():
    S, P, N, O = "S", "P", "N", "O"
    cols = ["Curated", "C1\nnetwork", "C2\nliterature", "C3/C4\nsignature", "C5\nrobust-\nness", "C6\nacts down-\nstream",
            "C7\nclinical\nprecedent", "C8\npaediatric\ndose", "C9\nsafety", "C10\ntarget &\ngenetics"]
    rows = [
        ("Metformin",                   [S, S, S, O, S, S, S, S, P, S]),
        ("Nicotinamide riboside",       [S, O, S, O, O, S, S, S, O, P]),
        ("Fisetin",                     [S, O, S, O, P, S, P, P, O, P]),
        ("Aspirin ± resveratrol",       [S, S, S, O, S, S, P, S, P, P]),
        ("Dasatinib + quercetin",       [P, S, P, S, S, S, P, P, P, O]),
        ("Navitoclax",                  [P, S, S, O, S, S, O, P, N, S]),
        ("Rapamycin / sirolimus",       [P, S, S, S, P, S, S, S, P, P]),
        ("17-AAG / HSP90 inhibitors",   [P, S, O, S, P, S, N, N, O, S]),
        ("Aurora / PLK / MPS1 inhibitors", [N, N, N, O, N, N, O, O, O, N]),
    ]
    sty = {S: ("o", TEAL, "supports"), P: ("D", ORANGE, "partial / caveat"), N: ("X", RED, "against / contraindicated"), O: ("s", "#D5DAE0", "no data / no signal")}
    fig, ax = plt.subplots(figsize=(10.6, 5.1))
    for i, (name, cells) in enumerate(rows):
        for j, c in enumerate(cells):
            m, col, _ = sty[c]
            ax.scatter(j, i, marker=m, s=170 if c != O else 60, c=col, edgecolor="white" if c != O else "none", lw=1.1, zorder=3)
    ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, fontsize=8.8); ax.xaxis.tick_top()
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=10.6)
    ax.set_xlim(-0.6, len(cols)-0.4); ax.set_ylim(len(rows)-0.4, -0.6)
    for s_ in ("left", "bottom", "right", "top"): ax.spines[s_].set_visible(False)
    ax.tick_params(length=0)
    ax.axhspan(-0.5, 2.5, color="#F1F8F5", zorder=0); ax.axhspan(7.5, 8.5, color="#FBF1EC", zorder=0)
    for y in (2.5, 3.5, 7.5): ax.axhline(y, color="#D5DAE0", lw=0.8, zorder=1)
    xr = len(cols) - 0.35
    ax.text(xr, 1.0, "proposed\n(ordered by\npaediatric evidence)", fontsize=9.2, va="center", ha="left", color=TEAL, fontweight="bold")
    ax.text(xr, 3.0, "optional context", fontsize=9.2, va="center", ha="left", color="#5F6B76", fontweight="bold")
    ax.text(xr, 5.5, "reserve / hypothesis /\nmechanistic only", fontsize=9.2, va="center", ha="left", color="#5F6B76", fontweight="bold")
    ax.text(xr, 8.0, "contraindicated", fontsize=9.2, va="center", ha="left", color=RED, fontweight="bold")
    ax.legend(handles=[Line2D([0],[0], marker=sty[k][0], ls="", color=sty[k][1], markersize=9 if k != O else 6, label=sty[k][2]) for k in (S, P, N, O)],
              loc="upper center", bbox_to_anchor=(0.46, -0.03), ncol=4, fontsize=9.8, frameon=False)
    fig.savefig(os.path.join(OUT, "fig4_convergence.png"), dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print("fig4_convergence.png")

if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4()
