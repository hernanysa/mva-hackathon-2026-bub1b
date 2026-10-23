#!/usr/bin/env python3
"""C7 (anexo) — metadatos EXACTOS de los 15 precedentes citados: título oficial, fase, N,
estado, y sobre todo EDAD de elegibilidad (adulto vs pediátrico). Evita sobre-afirmar
'población pediátrica' en el report. Salida: c7_verified.json"""
import json, urllib.request, time
NCTS = ["NCT03398824","NCT06519786","NCT01981525","NCT02733679","NCT04733534","NCT04313634",
        "NCT02652052","NCT04870866","NCT06324877","NCT04192136","NCT05955924","NCT02579044",
        "NCT06950385","NCT02497820","NCT02813824"]
out = {}
for n in NCTS:
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(
                f"https://clinicaltrials.gov/api/v2/studies/{n}", headers={"User-Agent":"mva-c7/1.0"}), timeout=30) as r:
                d = json.load(r); break
        except Exception as e:
            d = None; time.sleep(2)
    if not d: out[n] = {"error": "fetch failed"}; continue
    p = d["protocolSection"]; im = p["identificationModule"]; st = p["statusModule"]
    el = p.get("eligibilityModule", {}); ds = p.get("designModule", {})
    out[n] = {
      "title": im.get("officialTitle") or im.get("briefTitle"),
      "acronym": im.get("acronym"),
      "status": st.get("overallStatus"), "phase": "/".join(ds.get("phases", [])) or "NA",
      "n": (ds.get("enrollmentInfo") or {}).get("count"),
      "minAge": el.get("minimumAge"), "maxAge": el.get("maximumAge"), "stdAges": el.get("stdAges"),
      "conditions": p.get("conditionsModule", {}).get("conditions"),
      "interventions": [x.get("name") for x in p.get("armsInterventionsModule", {}).get("interventions", [])],
      "hasResults": bool(d.get("hasResults")),
    }
    o = out[n]
    print(f"{n} | {o['phase']:<13}| n={str(o['n']):<5}| {o['minAge']}–{o['maxAge'] or '∞':<9}| {o['status']:<22}| {(o['acronym'] or '')[:12]:<12}| {o['title'][:95]}")
    time.sleep(0.25)
json.dump(out, open("c7_verified.json", "w"), indent=1)
