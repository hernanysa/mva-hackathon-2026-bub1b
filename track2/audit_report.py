#!/usr/bin/env python3
"""Auditoría automática del report de Track 2: cada cifra citada se contrasta con su
archivo fuente. Imprime solo los FALLOS y un resumen. Uso: python3 audit_report.py"""
import os, re, json, csv, gzip, math

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..")
R = os.path.join(P, "investigacion", "repurposing")
rep = open(os.path.join(HERE, "track2_report.md"), encoding="utf-8").read()
ok, fail = 0, []

def check(name, cond, detail=""):
    global ok
    if cond: ok += 1
    else: fail.append(f"{name}: {detail}")

def in_report(s):            # la frase/cifra aparece en el report
    return s in rep

def approx(a, b, tol):       return abs(float(a) - float(b)) <= tol

# ---------------- C10 (Open Targets / DepMap) ----------------
c10 = json.load(open(os.path.join(R, "c10_opentargets.json")))
dis = {r["sym"]: r for r in c10["disease_side"]}
for sym, dep, drugs in [("BUB1B", -1.21, 0), ("BUB1", -0.64, 0), ("MAD2L1", -1.37, 0), ("CDC20", -2.09, 0), ("TTK", -0.84, 2), ("AURKB", -2.20, 18)]:
    check(f"C10 {sym} DepMap", approx(dis[sym]["dep_median"], dep, 0.005), f"fuente {dis[sym]['dep_median']} vs report {dep}")
    check(f"C10 {sym} drugs", dis[sym]["drugs"] == drugs, f"fuente {dis[sym]['drugs']} vs report {drugs}")
    check(f"C10 {sym} essential", dis[sym]["essential"] is True, "no figura como esencial")
tg = {r["sym"]: r for r in c10["drug_targets"]}
check("C10 PRKAA1 0.47 gastric", approx(tg["PRKAA1"]["gen_support_cancer"], 0.465, 0.006) and "gastric" in tg["PRKAA1"]["gen_support_cancer_dis"].lower(), str(tg["PRKAA1"]))
check("C10 PRKAA2 0.35 ovarian", approx(tg["PRKAA2"]["gen_support_cancer"], 0.353, 0.006) and "ovarian" in tg["PRKAA2"]["gen_support_cancer_dis"].lower(), "")
for sym, n in [("MTOR", 26), ("BCL2", 7), ("HSP90AA1", 10), ("NAMPT", 3), ("PTGS2", 79), ("HDAC1", 14)]:
    check(f"C10 {sym} n_drugs", tg[sym]["n_drugs"] == n, f"fuente {tg[sym]['n_drugs']} vs {n}")

# ---------------- C6 (Enrichr) ----------------
c6 = json.load(open(os.path.join(R, "c6_enrichment.json")))
check("C6 módulo 187 genes", len(c6["module_genes"]) == 187, f"{len(c6['module_genes'])}")
check("C6 CIN70 37", len(c6["cin70_module_hits"]) == 37 and c6["bub1b_in_cin70"] is False, f"{len(c6['cin70_module_hits'])}, bub1b_in={c6['bub1b_in_cin70']}")
def padj(lib, term):
    for t, p, pa, genes in c6["enrichment"][lib]:
        if t.startswith(term): return pa
    return None
for lib, term, val in [("Reactome_2022", "Cell Cycle R-HSA-1640170", 2.5e-121), ("Reactome_2022", "Mitotic Spindle Checkpoint", 3.4e-119)]:
    v = padj(lib, term)
    check(f"C6 {term[:28]}", v is not None and abs(math.log10(v) - math.log10(val)) < 0.03, f"fuente {v} vs report {val}")
c6md = open(os.path.join(R, "c6_RESULTADO.md"), encoding="utf-8").read()   # (fuera del top-25 del JSON)
for term, val in [("Cellular Senescence R-HSA-2559583", "3.7e-26"), ("Senescence-Associated Secretory Phenotype (SASP) R-HSA-2559582", "1.2e-20"),
                  ("Oxidative Stress Induced Senescence R-HSA-2559580", "7.9e-08")]:
    check(f"C6 {term[:28]}", f"{term} — p adj {val}" in c6md, "no está en c6_RESULTADO.md")

# ---------------- C1 ----------------
c1 = list(csv.DictReader(open(os.path.join(R, "c1_ranking.tsv")), delimiter="\t"))
def z1(drug, mod):
    for r in c1:
        if r["drug"].lower() == drug and r["module"] == mod: return float(r["z"])
for drug, mod, val in [("acadesine", "aneuploidia_estres", -5.7), ("aspirin", "aneuploidia_estres", -6.0), ("tanespimycin", "aneuploidia_estres", -4.2),
                       ("sirolimus", "aneuploidia_estres", -4.0), ("metformin", "aneuploidia_estres", -3.7), ("navitoclax", "senescencia", -2.2)]:
    v = z1(drug, mod); check(f"C1 {drug} {mod}", v is not None and approx(v, val, 0.06), f"fuente {v} vs report {val}")
check("C1 8.706 fármacos en report", in_report("8,706"), "")

# ---------------- C5 ----------------
c5 = open(os.path.join(R, "c5_RESULTADO.md"), encoding="utf-8").read()
rhos = [float(x) for x in re.findall(r"\| (-0\.\d+) \|", c5)]
check("C5 rango rho −0.58..−0.67", rhos and approx(min(rhos), -0.67, 0.005) and approx(max(rhos), -0.58, 0.005), f"{rhos}")
check("C5 report cita rho", in_report("−0.58 to −0.67"), "")

# ---------------- C4 ----------------
c4 = json.load(open(os.path.join(R, "c4_hits.json")))
check("C4 168 up / 160 dn", len(c4["gse277997_up"]) == 168 and len(c4["gse277997_dn"]) == 160, f"{len(c4['gse277997_up'])}/{len(c4['gse277997_dn'])}")
check("C4 streak 165", c4["n_streak"] == 165, f"{c4['n_streak']}")
check("C4 top reverser estricto INK-128", c4["l1000_top_strict"] and c4["l1000_top_strict"][0]["drug"] == "INK-128", f"{c4['l1000_top_strict'][:1]}")
geo = {}
with gzip.open(os.path.join(R, "data", "c4_geo", "GSE277997_H_v_WT.csv.gz"), "rt") as f:
    for r in csv.DictReader(f):
        try: geo[r["gene"]] = (float(r["log2FC"]), float(r["padj"]))
        except (ValueError, TypeError): pass
for g in ["Cdkn1a", "Cdkn2b", "Timp1", "Gdf15", "Fgf21", "Trib3"]:
    check(f"C4 {g} fuerte (padj ≤1.5e-5)", geo[g][1] <= 1.5e-5 and geo[g][0] > 0.585, f"{geo[g]}")
for g in ["Cdkn2a", "Ddit3", "Chac1"]:
    check(f"C4 {g} marginal (0.03–0.05)", 0.025 <= geo[g][1] <= 0.05, f"{geo[g]}")
check("C4 Gdf15 log2FC 3.4 / Fgf21 5.2", approx(geo["Gdf15"][0], 3.4, 0.05) and approx(geo["Fgf21"][0], 5.2, 0.05), f"{geo['Gdf15']} {geo['Fgf21']}")

# ---------------- C7 ----------------
c7 = json.load(open(os.path.join(R, "c7_verified.json")))
c7md = open(os.path.join(R, "c7_RESULTADO.md"), encoding="utf-8").read()
check("C7 44 búsquedas / 146 estudios", "44 búsquedas" in c7md and "146 estudios" in c7md, re.search(r"_ClinicalTrials.*?_", c7md).group(0)[:120])
def ages(n): return (c7[n]["minAge"], c7[n]["maxAge"])
exp = {"NCT03398824": ("6 Years", "35 Years"), "NCT06519786": ("5 Years", "18 Years"), "NCT01981525": ("18 Years", None),
       "NCT02733679": ("18 Years", "30 Years"), "NCT04733534": ("18 Years", None), "NCT04313634": ("60 Years", None),
       "NCT02652052": ("18 Years", None), "NCT04870866": ("3 Years", None), "NCT04192136": ("10 Years", "40 Years"),
       "NCT02579044": ("18 Months", "25 Years"), "NCT06950385": ("18 Years", None), "NCT02813824": ("18 Years", "75 Years"),
       "NCT02497820": ("18 Years", None), "NCT05955924": ("18 Years", None)}
for n, a in exp.items():
    check(f"C7 edades {n}", ages(n) == a, f"fuente {ages(n)} vs {a}")
    check(f"C7 {n} citado en report", in_report(n), "no aparece")
for n, ph, N in [("NCT03398824", "PHASE2", 15), ("NCT06519786", "PHASE3", 30), ("NCT01981525", "PHASE1", 26), ("NCT02733679", "PHASE4", 27),
                 ("NCT04733534", "PHASE2", 120), ("NCT04313634", "PHASE2", 74), ("NCT02652052", "PHASE1", 9), ("NCT04870866", "PHASE2", 13),
                 ("NCT04192136", "NA", 75), ("NCT05955924", "PHASE3", 396), ("NCT02579044", "PHASE1/PHASE2", 80), ("NCT06950385", "PHASE3", 168),
                 ("NCT02813824", "PHASE3", 852), ("NCT02497820", "PHASE3", 1800)]:
    check(f"C7 fase/N {n}", c7[n]["phase"] == ph and c7[n]["n"] == N, f"fuente {c7[n]['phase']}/{c7[n]['n']} vs {ph}/{N}")
kids = [n for n, v in c7.items() if v.get("minAge") and (("Years" in v["minAge"] and int(v["minAge"].split()[0]) < 18) or "Month" in v["minAge"])]
check("C7 '5 of 15 include children'", len(kids) == 5, f"{len(kids)}: {kids}")
check("C7 los 15 NCT del dict aparecen en el report", all(in_report(n) for n in c7), f"faltan {[n for n in c7 if not in_report(n)]}")

# ---------------- C9 ----------------
c9 = {r["label"]: r for r in json.load(open(os.path.join(R, "c9_faers.json")))}
check("C9 metformina 523 ped", c9["metformina"]["ped"] == 523, f"{c9['metformina']['ped']}")
check("C9 sirolimus 672 ped", c9["rapamicina/sirolimus"]["ped"] == 672, "")
check("C9 aspirina 1.344 ped", c9["aspirina"]["ped"] == 1344, "")
check("C9 NR 36 total", c9["nicotinamida ribósido"]["tot"] == 36, "")
check("C9 dasatinib AE #1 derrame pleural", c9["dasatinib (D+Q)"]["top"][0][0] == "PLEURAL EFFUSION", f"{c9['dasatinib (D+Q)']['top'][:1]}")

# ---------------- C2 ----------------
c2md = open(os.path.join(R, "c2_RESULTADO.md"), encoding="utf-8").read()
check("C2 25 consultas / 220 textos / 6.578 compuestos", "25 consultas" in c2md and "220 artículos" in c2md and "6.578" in c2md, "")

# ---------------- Ensayo de Fanconi (texto completo, Europe PMC) ----------------
fa = os.path.join(R, "data", "lit", "PMC9631552.xml")
if not os.path.exists(fa):
    import urllib.request
    os.makedirs(os.path.dirname(fa), exist_ok=True)
    urllib.request.urlretrieve("https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9631552/fullTextXML", fa)
import html as _h; t = _h.unescape(re.sub(r"<[^>]+>", " ", open(fa, encoding="utf-8", errors="ignore").read()))
for frag in ["500 mg twice daily for patients < 10 years", "1000 mg twice daily for patients 10 years or older",
             "median age of treated patients was 9.4 years", "12 of 14", "No subjects developed hypoglycemia or metabolic acidosis",
             "no grade 3 or higher adverse events", "4 of 13", "2000 to 1500 mg/day"]:
    check(f"Fanconi: '{frag[:40]}'", frag in re.sub(r"\s+", " ", t), "no está en el texto completo")

# ---------------- Track 1 / fronteras citadas ----------------
t1p = next(x for x in (os.path.join(P, "submission", "track1_report.md"), os.path.join(P, "report", "track1_report.md")) if os.path.exists(x))
t1 = open(t1p, encoding="utf-8").read()
for frag in ["40209701", "40220612", "c.2210T>G", "c.3006T>G", "VCV000533901", "0.997", "0.923"]:
    check(f"Track1 '{frag}'", frag in t1, "no figura en el report de Track 1")
est = open(os.path.join(P, "investigacion", "estructura", "RESULTADO.md"), encoding="utf-8").read()
for frag in ["91", "161", "Trp973", "Phe954"]:
    check(f"Estructura '{frag}'", frag in est, "no figura en estructura/RESULTADO.md")
skipped = []
pgxp = os.path.join(P, "investigacion", "pgx", "RESULTADO.md")
if os.path.exists(pgxp):
    pgx = open(pgxp, encoding="utf-8").read()
    for frag in ["c.6178G>T", "rs6025", "*4/*35", "*2/*17", "*3/*3", "M420del", "R61C", "G401S", "G465R"]:
        check(f"PGx '{frag}'", frag in pgx, "no figura en pgx/RESULTADO.md")
else:
    skipped.append("PGx (9 checks): source has the proband's genotypes, kept private; runs only on the author's machine")

# ---------------- Estructura: se recalcula desde el modelo de AlphaFold ----------------
import subprocess, sys
out = subprocess.run([sys.executable, os.path.join(P, "investigacion", "estructura", "n1002_structure.py")],
                     capture_output=True, text=True).stdout
num = lambda pat: float(re.search(pat, out).group(1))
check("Estructura pLDDT 91", round(num(r"pLDDT \(C-alpha\): ([\d.]+)")) == 91 and in_report("pLDDT 91"), out[:80])
check("Estructura 161 átomos", int(num(r"own atoms included\): (\d+)")) == 161 and in_report("161 heavy atoms within 10 Å of its Cα"), "")
check("Estructura ~19 Å HRD-like", round(num(r"HRD-like \(HGD 880-882\): ([\d.]+)")) == 19 and in_report("~19 Å"), "")
check("Estructura ~27 Å DFG-like", round(num(r"DFG-like \(DFS 911-913\): ([\d.]+)")) == 27 and in_report("~27 Å"), "")

print(f"\nAUDITORÍA: {ok} OK · {len(fail)} FALLOS" + (f" · {len(skipped)} grupo(s) privado(s) omitido(s)" if skipped else ""))
for x in skipped: print("  ·", x)
for f in fail: print("  ✗", f)
