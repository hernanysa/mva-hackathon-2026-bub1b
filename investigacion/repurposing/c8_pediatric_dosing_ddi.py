#!/usr/bin/env python3
"""
C8 — De "hipótesis" a "accionable": dosis pediátrica, PK y interacciones de los
candidatos de Track 2, cruzadas con la farmacogenómica REAL del probando (frontier A).

No es un análisis computacional nuevo: es la consolidación que convierte el set de
candidatos en algo que un equipo de genética + onco-ped podría llevar a un comité
de n-of-1. Fuentes: labels FDA/EMA, ensayos citados (C7), CPIC/DPWG (frontier A).
Salida: c8_RESULTADO.md
"""

# --- farmacogenómica accionable del probando (de investigacion/pgx/RESULTADO.md) ---
PGX = {
  "RYR1 c.6178G>T": "susceptibilidad a hipertermia maligna INCIERTA → anestesia: TIVA, evitar volátiles+succinilcolina, dantroleno disponible",
  "Factor V Leiden (F5) het": "trombofilia → tromboprofilaxis con vías centrales / L-asparaginasa",
  "CYP2C19 *2/*17 (IM)": "voriconazol con TDM; IBP más exposición",
  "CYP2D6 *4/*35 (IM, solo SNV)": "codeína/tramadol → menos analgesia; usar morfina/hidromorfona",
  "CYP2C9 *1/*1 (normal)": "celecoxib y el sustrato-lado de fisetina: sin ajuste",
  "CYP3A4 *1/*1 (normal)": "dasatinib, sirolimus: PK predecible",
  "G6PD normal": "aspirina y rasburicasa sin riesgo de hemólisis",
  "DPYD/TPMT/NUDT15/UGT1A1 normales": "backbone de quimio a dosis estándar",
  "OCT1/SLC22A1": "sin M420del ni R61C/G401S/G465R → respuesta a metformina esperable normal",
}

# --- candidatos: dosis pediátrica, ruta, PK, DDI, monitoreo, ajuste PGx ---
CAND = [
 dict(nombre="Fisetina", tier="1 (senólisis)",
   dosis="20 mg/kg/día VO × 2 días consecutivos, repetir cada 4 semanas ('hit-and-run'). "
         "Régimen de los ensayos Mayo (STOP-Sepsis, COVID-FIS, osteoartritis). Flavonoide, OTC. "
         "**Es una dosis de ADULTOS extrapolada por peso — no existe ensayo pediátrico de fisetina.**",
   ped="**NINGÚN ensayo pediátrico.** Solo adultos: SEN-SURVIVORS NCT04733534 (fisetina y D+Q en "
       "sobrevivientes ADULTOS ≥18 a de cáncer infantil con fragilidad, Phase 2, n=120); "
       "NCT04313634 (senolíticos en adultos mayores ≥60 a, Phase 2, n=74, completo). "
       "La PK/dosis pediátrica de fisetina es una hipótesis a resolver con farmacología pediátrica.",
   pk="Biodisponibilidad oral baja y variable; tomar con comida grasa / formulación lipídica. "
      "Vida media corta → por eso el pulso de 2 días.",
   ddi="**Inhibe CYP2C9, UGT1A1, OATP1B1/1B3, P-gp** in vitro. El probando es CYP2C9 normal, "
       "así que el riesgo es que fisetina **suba niveles de co-medicación** (celecoxib, "
       "ibuprofeno, warfarina, metotrexato, irinotecán-SN38). En el pulso de 2 días/mes el "
       "riesgo es acotado; separar de quimio.",
   pgx="CYP2C9 *1/*1 → sin ajuste intrínseco. Vigilar co-sustratos de CYP2C9/UGT durante el pulso.",
   monit="Función hepática basal; revisar lista de medicación concomitante antes de cada pulso.",
   flag="✅ senolítico de elección sobre D+Q (mejor perfil de seguridad) — pero ⚠️ el eslabón con "
        "MENOS evidencia pediátrica: mecanismo fuerte, dosis extrapolada."),

 dict(nombre="Metformina", tier="1 (estrés de aneuploidía / AMPK)",
   dosis="Protocolo del ensayo en Fanconi (NCT03398824): comenzar 500 mg/día y subir 500 mg/día "
         "hasta la dosis objetivo por edad — **500 mg c/12 h si <10 años; 1000 mg c/12 h si ≥10 años**; "
         "bajar 500 mg/día ante intolerancia GI/renal. Metformina de liberación inmediata, 6 meses, "
         "dosis 'prescritas para DM2'. Aprobada FDA en ≥10 años (DM2); <10 años = off-label.",
   ped="**NCT03398824** (anemia de Fanconi, 6–35 a, mediana 9,4 a, 14 tratados/13 evaluables, no "
       "diabéticos, Boston Children's, 6 meses): respuesta hematológica 4/13 (31%); **sin acidosis "
       "metabólica ni hipoglucemia; sin eventos ≥grado 3**; diarrea 12/14 (grado 1–2); 1 reducción "
       "de dosis por GI; proteómica → ↓ vías inflamatorias. Blood Adv 2022;6(12):3803 (PMID 35500223). "
       "Phase 3 registrada en niños 5–18 a (NCT06519786, estado 'unknown'). Adultos: Li-Fraumeni "
       "(NCT01981525, ≥18 a, Phase 1) y ataxia-telangiectasia (NCT02733679, 18–30 a, Phase 4).",
   pk="Sin metabolismo hepático; se elimina **intacta por riñón** (secreción tubular vía OCT2/MATE). "
      "t½ ~5 h.",
   ddi="Competición OCT2/MATE con cimetidina, dolutegravir, trimetoprima, ranolazina → ↑ metformina. "
       "**Contraste yodado y cualquier causa de fallo renal agudo → suspender** (riesgo acidosis "
       "láctica). Mínima interacción CYP.",
   pgx="OCT1 del probando sin variantes de pérdida de función → captación hepática y respuesta "
       "**normales**. No hay gen CPIC que fuerce ajuste.",
   monit="⚠️ **El probando tiene nefrocalcinosis** → TFG basal y periódica; suspender en "
         "deshidratación/vómitos/contraste; **B12 anual**; lactato si hay enfermedad intercurrente.",
   flag="✅ el candidato MEJOR respaldado: único con ensayo en un síndrome pediátrico de "
        "inestabilidad genómica (Fanconi). Caveat renal explícito (nefrocalcinosis)."),

 dict(nombre="Nicotinamida ribósido (NR)", tier="2 (adyuvante upstream — SIRT2→BubR1)",
   dosis="25 mg/kg/día VO — régimen del estudio de Veenhuis en "
         "ataxia-telangiectasia (24 pacientes, 17 niños, 4 meses; sin tope de dosis informado). Adultos: 250–1000 mg/día. Suplemento.",
   ped="**Veenhuis et al., Mov Disord 2021** (publicación, ataxia-telangiectasia, 24 pacientes "
       "—niños >2 a y adultos—, 4 meses): mejoró scores de ataxia e IgG; ↑NAD+ hasta ~4×. "
       "Registros: NCT04870866 (A-T, ≥3 a, Phase 2, n=13, activo), NCT06324877 (A-T, 'ATNAD', "
       "n=10, estado 'unknown'); NR en Friedreich NCT04192136 (10–40 a, n=75, completo).",
   pk="Se convierte a NAD+ vía NRK1/2 y ruta de salvamento; buena tolerancia oral.",
   ddi="Mínima. A dosis muy altas de **nicotinamida** (no NR) puede inhibir sirtuinas y CYP — "
       "por eso se prefiere NR y no megadosis de nicotinamida.",
   pgx="Sin genes CPIC asociados.",
   monit="Función hepática si se combina con nicotinamida a dosis alta; por lo demás, mínimo.",
   flag="✅ muy seguro; el más 'upstream' (podría elevar el BubR1 del alelo hipomórfico)."),

 dict(nombre="Aspirina (dosis baja)", tier="contexto (quimioprevención)",
   dosis="1–5 mg/kg/día VO (rango antiagregante pediátrico, precedente en cardiología / Kawasaki). "
         "Quimioprevención en adultos con Lynch: 100–600 mg/día según ensayo.",
   ped="Uso antiagregante pediátrico bien establecido. **Quimioprevención: solo adultos** — "
       "NCT02813824 (AAS-Lynch, aspirina dosis baja, Lynch 18–75 a, n=852, Phase 3) y NCT02497820 "
       "(CaPP3, registro Israel, 600 vs 300 vs 100 mg, ≥18 a, n=1800, 'not yet recruiting'). "
       "No hay datos de quimioprevención con aspirina en niños.",
   pk="Hidrólisis a salicilato; el efecto antiagregante es irreversible sobre COX-1 plaquetaria.",
   ddi="Aditivo con anticoagulantes/NSAIDs (sangrado); ↑ niveles de **metotrexato** (desplaza y "
       "compite en secreción tubular) — **separar de dosis altas de MTX**; con IECA ↓ efecto renal.",
   pgx="G6PD normal → sin hemólisis.",
   monit="⚠️ **suspender en cuadros virales febriles y peri-cirugía (síndrome de Reye)**; "
         "sangrado GI; no usar durante trombocitopenia por quimio.",
   flag="⚠️ adyuvante de bajo costo; ventana de uso limitada por Reye y por quimio."),

 dict(nombre="Rapamicina / sirolimus", tier="hipótesis (mTOR — no 1ª línea)",
   dosis="Trough-dirigida (5–15 ng/mL) o ~0,8 mg/m²/dosis; uso pediátrico establecido en "
         "anomalías vasculares y TSC. eRapa (encapsulada) en FAP: NCT06950385 (Phase 3).",
   ped="Amplio uso pediátrico off-label (anomalías linfáticas, TSC). Progeria: NCT02579044 "
       "(everolimus+lonafarnib). FAP: eRapa Phase 3.",
   pk="Sustrato CYP3A4 y P-gp → **superficie de interacción enorme**.",
   ddi="Azoles, macrólidos, diltiazem, **pomelo** → ↑↑ sirolimus. Rifampicina, anticonvulsivantes "
       "inductores → ↓↓. El probando es CYP3A4 normal pero CYP3A5 no-expresor (*3/*3).",
   pgx="CYP3A4 *1/*1 normal. CYP3A5 *3/*3 → si alguna vez tacrolimus, dosis estándar alcanza diana.",
   monit="Niveles (TDM), lípidos, recuento (mielosupresión), heridas, neumonitis. "
         "**Inmunosupresor → cauteloso en un chico con predisposición tumoral e infecciones.**",
   flag="❌ no 1ª línea: fuerte en los 3 métodos computacionales pero inmunosupresor. "
        "Hipótesis para uso intermitente / senomórfico."),
]

EXCLUIDOS = [
 ("Dasatinib + quercetina (D+Q)", "senólisis alternativa",
  "dasatinib afecta la **placa de crecimiento** (~4%, malo con RCIU) e **induce aberraciones "
  "cromosómicas de novo** (malo con CIN constitucional). Derrame pleural, mielosupresión. "
  "Solo si fisetina falla. PK de dasatinib OK (CYP3A4 normal)."),
 ("Navitoclax", "senólisis (BCL-xL)",
  "**trombocitopenia dosis-limitante** (inhibición de BCL-xL en plaquetas). Reservar para BH3-"
  "miméticos BCL-xL-selectivos más nuevos (A1331852/A1155463) si algún día hay datos pediátricos."),
 ("17-AAG / tanespimicina (HSP90i)", "validación mecanística de Tang-Amon 2011",
  "**NO aprobado** — 38 ensayos oncológicos, abandonado por toxicidad hepática/ocular (ver C7). "
  "Se cita como prueba de concepto del eje, no como candidato."),
 ("Inhibidores de Aurora / MPS1 / PLK", "aparecen en C1/C6 por proximidad al gen",
  "**contraindicados**: inhibir aún más un checkpoint ya débil. Quimioterápicos, no repurposing."),
]

out = ["# C8 — Dosis pediátrica, PK e interacciones para ESTE probando\n"]
out.append("_Convierte el set de candidatos en algo accionable: qué dosis, por qué vía, qué "
           "vigilar, y cómo se cruza con la farmacogenómica real del chico (frontier A). "
           "No sustituye la evaluación de un equipo de genética + oncología pediátrica._\n")

out.append("\n## Farmacogenómica del probando que toca a estos fármacos\n")
out.append("| hallazgo | implicancia |\n|---|---|")
for k,v in PGX.items():
    out.append(f"| {k} | {v} |")

out.append("\n## Candidatos — ficha accionable\n")
for c in CAND:
    out.append(f"\n### {c['nombre']}  ·  tier {c['tier']}  ·  {c['flag']}\n")
    out.append(f"- **Dosis:** {c['dosis']}")
    out.append(f"- **Precedente pediátrico:** {c['ped']}")
    out.append(f"- **PK:** {c['pk']}")
    out.append(f"- **Interacciones:** {c['ddi']}")
    out.append(f"- **Cruce con la PGx del probando:** {c['pgx']}")
    out.append(f"- **Monitoreo:** {c['monit']}")

out.append("\n## Excluidos / reservados — y por qué\n")
out.append("| agente | rol | por qué no |\n|---|---|---|")
for n,r,w in EXCLUIDOS:
    out.append(f"| {n} | {r} | {w} |")

out.append("\n## Interacción con el tratamiento oncológico probable\n")
out.append("En MVA el riesgo de cáncer está claramente aumentado pero no se puede cuantificar (Nakano 2024); "
           "en MVA1-BUB1B se reportaron rabdomiosarcoma embrionario y Wilms bilateral. "
           "Si aparece un tumor, la quimio manda y los repurposing se **pausan**:")
out.append("- **Fisetina/aspirina**: suspender durante ciclos de quimio (interacción CYP2C9/UGT, "
           "sangrado, trombocitopenia). Reanudar en mantenimiento/remisión.")
out.append("- **Metformina**: suspender con nefrotoxicidad (cisplatino, ifosfamida), mucositis "
           "severa, o cualquier contraste. Compatible con mantenimiento de LLA (6-MP: TPMT/NUDT15 "
           "del probando normales).")
out.append("- **NR**: probablemente el más compatible con quimio activa (perfil de suplemento), "
           "aunque sin datos de co-administración.")
out.append("- La **vigilancia tumoral** (eco renal c/3 meses desde el nacimiento hasta los 7 años, para "
           "todos los tipos de MVA — Nakano et al. 2024) es la intervención de mayor impacto y es independiente de todo esto.")

out.append("\n## Síntesis\n")
out.append("El régimen mínimo defendible para llevar a un comité de n-of-1, **ordenado por solidez "
           "de la evidencia clínica en niños** (el mecanismo es fuerte en los tres):\n")
out.append("1. **Metformina** — la mejor respaldada: única con ensayo en un síndrome *pediátrico* de "
           "inestabilidad genómica (Fanconi, 6–35 a), con dosis por edad publicada (500 mg c/12 h "
           "<10 a; 1000 mg c/12 h ≥10 a) y perfil de seguridad en niños no diabéticos; vigilar TFG "
           "por la nefrocalcinosis.\n"
           "2. **NR** 25 mg/kg/día — adyuvante upstream; dosis del estudio de "
           "ataxia-telangiectasia (17 de 24 pacientes eran niños; \"tolerated well\"); muy buena tolerabilidad, evidencia solo en "
           "enfermedades neuro/mitocondriales, **no** en predisposición tumoral.\n"
           "3. **Fisetina** 20 mg/kg × 2 días/mes — mecanismo más directo para el eje senescencia "
           "(el ratón BubR1^H/H es la prueba de concepto del campo) pero **sin ningún ensayo pediátrico**: "
           "la dosis es de adultos extrapolada por peso. Requiere revisión de farmacología pediátrica "
           "antes de considerarla; es el eslabón más incierto.\n"
           "\\+ vigilancia tumoral intensiva. Aspirina dosis baja opcional en ventanas sin quimio "
           "(quimioprevención: evidencia solo en adultos con Lynch).\n\n"
           "Todo VO, OTC o aprobado, y **sin conflicto con la farmacogenómica del probando** (de hecho "
           "la PGx despeja el camino: OCT1 normal para metformina, CYP2C9 normal para la interacción "
           "de fisetina, G6PD normal para aspirina, CYP3A4 normal para todo lo demás). "
           "**Dosis pediátricas publicadas: metformina y NR. Fisetina: solo adultos.**")

open("c8_RESULTADO.md","w").write("\n".join(out) + "\n")
print("OK -> c8_RESULTADO.md")
