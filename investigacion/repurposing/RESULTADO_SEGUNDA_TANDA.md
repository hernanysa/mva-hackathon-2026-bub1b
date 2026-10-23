# Track 2 — segunda tanda de pruebas (C4–C10): síntesis

Después del análisis curado + C1–C3, se añadieron **7 verificaciones más**, cada una atacando un
flanco que un revisor va a mirar. Ninguna usa la curación como entrada.

| # | análisis | método | qué agrega | veredicto |
|---|---|---|---|---|
| **C4** | reversión de firma con firma **real** de BubR1 | 2 datasets GEO de ratón BubR1-bajo → DE → L1000CDS2 | firma de datos primarios, no listas de literatura | ✅ la firma real enciende p16/p21/p15 + Gdf15/Fgf21/CHOP; reversores = mismos MOA que C3 (HSP90/mTOR/HDAC/CDK) |
| **C5** | robustez de la proximidad de red | RWR / personalized PageRank en STRING≥700 y ≥900 | ¿la conclusión de C1 depende de la métrica/umbral? | ✅ robusta: con otra métrica y otro umbral, misma conclusión — venenos de huso en el gen, candidatos río abajo |
| **C6** | enriquecimiento de vías del interactoma de BUB1B | Enrichr (GO/Reactome/Hallmark) | respaldo **cuantitativo** de los dos ejes | ✅ checkpoint del huso p≤1e-121; senescencia p=3.7e-26 en el mismo módulo |
| **C7** | precedente clínico sistemático | ClinicalTrials.gov API v2, 44 búsquedas | ¿es una idea disparatada o hay ensayos en poblaciones análogas? | ✅ 0 en MVA; **15 precedentes verificados** en poblaciones análogas |
| **C8** | dosis pediátrica + PK + interacciones | labels + ensayos (C7) + PGx (frontier A) | de "hipótesis" a "accionable" | ✅ dosis pediátricas publicadas para metformina y NR; **fisetina: solo dosis de adultos, extrapolada por peso**; sin conflicto con la PGx del probando |
| **C9** | señales de seguridad | openFDA FAERS | ¿señales pediátricas / que choquen con el fenotipo? | ✅ experiencia pediátrica existe; AE de clase conocidos y manejables |
| **C10** | soporte genético + druggability de las dianas | Open Targets GraphQL | ¿el gen es drogable? ¿las dianas tienen soporte genético humano (Nelson 2015)? | ✅ BUB1B **pan-esencial, 0 fármacos**; AMPK/BCL2/HSP90 con **soporte genético para neoplasia** |

---

## C4 — Firma transcripcional REAL de BubR1-bajo

C3 usó listas de marcadores de literatura. C4 deriva la firma de **datos primarios**:
- **GSE277997** (BubR1 insuficiente, corazón): la DE Hypomorph-vs-WT enciende **Cdkn1a (p21), Cdkn2a
  (p16), Cdkn2b (p15), Gdf15, Timp1** (senescencia/SASP) **y Chac1, Ddit3 (CHOP), Fgf21, Trib3**
  (respuesta integrada al estrés — la firma canónica de células aneuploides de Tang-Amon).
- **GSE134781** (van Deursen, PMID 31738183; músculo de **portadores heterocigotos** de alelos MVA
  knock-in: L1002P en numeración de ratón = **L1012P humano**, a ~10 residuos de la N1002K del probando
  — *no es el mismo residuo* — y X753 truncante): el solapamiento con la firma cardíaca es a nivel de
  azar (esperable en portadores sanos y otro tejido); se usa solo como contexto, sin conclusión
  transcripcional.
- **Reversión de firma (L1000CDS2)**: los MOA sobre-representados entre los reversores (HSP90, mTOR,
  HDAC, CDK) **coinciden con C3** → robusto a cómo se defina la firma. Ningún candidato nuevo.

→ **Los dos ejes de Track 2 no son solo teoría: están en el transcriptoma real de un modelo de ratón
de BubR1 hipomórfico (corazón).** (Un dataset informativo; el segundo —portadores en músculo— no replica.)

---

## C10 — Open Targets: druggability + soporte genético

- **El gen de enfermedad es intratable**: BUB1B **pan-esencial** (DepMap geneEffect −1,2), **0
  fármacos/candidatos** en Open Targets, muy intolerante a LoF. Igual para BUB1, MAD2L1, CDC20,
  AURKB. → **confirmación curada de C1/C5/C6: inhibir el checkpoint es quimioterapia, no terapia
  dirigida.**
- **Las dianas río abajo son todas drogables y con fármacos aprobados**: mTOR (26), BCL2 (7),
  HSP90AA1 (10), NAMPT (3), PTGS2 (79), HDAC1 (14) — vs. 0 del gen de enfermedad.
- **Soporte genético humano** (Nelson 2015: duplica la probabilidad de aprobación de un fármaco):
  **PRKAA1/PRKAA2 (AMPK→metformina), BCL2/BCL2L1 (senólisis), HSP90AA1** tienen evidencia genética
  para neoplasia/tumor. → las dianas de nuestros candidatos no son solo plausibles: están
  genéticamente implicadas en cáncer en humanos.

---

## C7 — Precedente clínico: lo más contundente

**Ningún ensayo en MVA / PCS / BUB1B** (0 resultados) → confirma que esto es una hipótesis, no
práctica establecida. **Pero** los fármacos que proponemos **ya se probaron clínicamente en
enfermedades de la misma clase** (inestabilidad genómica / progeroides / predisposición a cáncer).
**Salvedad importante, verificada leyendo las edades de elegibilidad de cada registro:** solo
**5 de los 15** precedentes incluyen explícitamente niños o adolescentes; **el eje senolítico solo
tiene ensayos en adultos.**

| eje | precedente | NCT | población (edad) | fase | estado |
|---|---|---|---|---|---|
| **metformina** | **anemia de Fanconi** — respuesta hematológica 4/13 (31%), sin acidosis ni eventos ≥G3 | **NCT03398824** | **niños/jóvenes 6–35 a** (mediana 9,4) | 2 | **completo, con resultados** |
| metformina | anemia de Fanconi, confirmatorio | NCT06519786 | **niños 5–18 a** | 3 | estado "unknown" |
| metformina | Li-Fraumeni (predisposición a cáncer por TP53) | NCT01981525 | adultos ≥18 a | 1 | completo |
| metformina | ataxia-telangiectasia (RAMP) | NCT02733679 | 18–30 a | 4 | completo |
| **NAD+ (NR)** | ataxia-telangiectasia (Veenhuis, Mov Disord 2021: mejoró ataxia e IgG; ↑NAD+ ~4×) | publicación + NCT04870866 | **niños >2–3 a y adultos** | 2 | activo (NCT04870866) |
| NR | ataxia de Friedreich | NCT04192136 | **10–40 a** | — | completo |
| nicotinamida | quimioprevención de cáncer de piel en trasplantados (SPRINTR) | NCT05955924 | adultos | 3 | reclutando |
| **mTOR** | **progeria** (everolimus + lonafarnib) | NCT02579044 | **18 meses–25 a** | 1/2 | en curso |
| mTOR | rapamicina encapsulada en poliposis adenomatosa familiar (SERENTA) | NCT06950385 | adultos | 3 | reclutando |
| **senólisis** | SEN-SURVIVORS: fisetina y D+Q en sobrevivientes de cáncer infantil | NCT04733534 | **adultos ≥18 a** | 2 | activo |
| senólisis | D+Q / fisetina, salud ósea en adultos mayores | NCT04313634 | adultos ≥60 a | 2 | completo |
| senólisis | D+Q en sobrevivientes de trasplante de células madre | NCT02652052 | adultos ≥18 a | 1 | completo |
| **aspirina** | síndrome de Lynch (AAS-Lynch; CaPP3-Israel) | NCT02813824, NCT02497820 | adultos | 3 | activo / no iniciado |
| control | tanespimicina (HSP90i) — 38 ensayos oncológicos, abandonado por toxicidad | varios | — | 1–2 | terminados |

→ **Metformina y NR tienen ensayos en síndromes de inestabilidad genómica con niños** (Fanconi,
ataxia-telangiectasia, Friedreich); mTOR en progeria pediátrica. **Los senolíticos y la aspirina
solo tienen evidencia en adultos.** El precedente más directo sigue siendo metformina en Fanconi
(NCT03398824, Blood Adv 2022): mismo tipo de enfermedad (inestabilidad genómica pediátrica), niños
no diabéticos, sin acidosis láctica ni eventos ≥G3, señal de eficacia sobre citopenias.
---

## C5 — Robustez de la proximidad de red

C1 usó distancia "closest" (Guney 2016) sobre STRING≥700. C5 rehace la proximidad con
**random-walk-with-restart / personalized PageRank** (integra todos los caminos, no solo el más
corto) en STRING≥700 **y** ≥900:

- **Concordancia C1↔C5: ρ Spearman −0,6 aprox.** (el signo negativo *es* el acuerdo — una es
  distancia, la otra proximidad).
- **En los módulos del gen** (`MVA_genes`, `SAC_MCC`): el top por RWR sigue siendo **venenos de
  huso** (paclitaxel, docetaxel, vinorelbina, colchicina, PLK-i) + quimio. Los candidatos de
  repurposing puntúan bajo.
- **En los módulos río abajo**: senolíticos z medio 0,60 en `senescencia` vs 0,19 en `MVA_genes`
  (~3×); mTOR/HSP90/AMPK z medio 1,37 en `aneuploidia_estres` vs 0,64 en `MVA_genes` (~2×).

→ **La conclusión de C1 no depende de la métrica ni del umbral de red: no hay atajo farmacológico
en el gen de enfermedad; la oportunidad está en las consecuencias río abajo.**

---

## C6 — Enriquecimiento: los dos ejes, cuantificados

El vecindario de interacción de BUB1B en STRING (187 genes) da:

- **Checkpoint de ensamblaje del huso / segregación cromosómica**: p ajustada hasta **1e-121**
  (Reactome "Cell Cycle"), 1e-119 ("Mitotic Spindle Checkpoint"). Es literalmente la maquinaria
  que falla en MVA1 → **eje aneuploidía, confirmado**.
- **Cellular Senescence** p=**3.7e-26** · **SASP** p=**1.2e-20** · Oxidative-Stress-Induced
  Senescence p=7.9e-08 — enriquecidas **en el mismo módulo** → **eje senescencia, confirmado
  cuantitativamente** (no solo por el ratón BubR1^H/H).
- **37 de los 187 genes del módulo están en CIN70** (la firma clínica pronóstica de inestabilidad
  cromosómica) → el módulo de BUB1B y la firma de CIN tumoral comparten núcleo.
- **Ningún candidato de repurposing toca la maquinaria del checkpoint** (único cruce: fisetina–TP53,
  y TP53 es nodo de senescencia). Todos actúan río abajo → **coincide con C1**.

---

## C8 — Accionable: el régimen mínimo defendible

| # | fármaco | dosis pediátrica | precedente de la dosis | PGx del probando |
|---|---|---|---|---|
| 3 | **Fisetina** | 20 mg/kg/día × 2 días, cada 4 sem | ensayos Mayo "hit-and-run" — **adultos; extrapolada por peso, sin ensayo pediátrico** | CYP2C9 normal → sin ajuste |
| 1 | **Metformina** | desde 500 mg/día, +500 mg/día hasta 500 mg c/12 h (<10 a) o 1000 mg c/12 h (≥10 a) | NCT03398824 (Fanconi, 6–35 a) — protocolo publicado | OCT1 sin variantes LoF → respuesta normal |
| 2 | **NR** | 25 mg/kg/día | Veenhuis A-T (24 pacientes, 17 niños) | sin gen CPIC |
| + | vigilancia tumoral (eco renal c/3 meses, nacimiento → 7 años, todos los tipos de MVA) | — | Nakano et al. 2024 | — |
| ± | aspirina dosis baja | 1–5 mg/kg/día (rango antiagregante) | cardiología pediátrica; quimioprevención solo en adultos (Lynch) | G6PD normal → sin hemólisis |

**La farmacogenómica del probando (frontier A) despeja el camino** para los 3 principales:
OCT1 normal (metformina), CYP2C9 normal (fisetina), CYP3A4 normal (todo lo demás), G6PD normal
(aspirina). El único hallazgo PGx que obliga a conducta es **RYR1 → hipertermia maligna incierta**,
y es sobre **anestesia**, no sobre los repurposing.

**Caveat #1 (explícito en el report):** el probando tiene **nefrocalcinosis** → metformina exige
monitoreo de TFG y suspensión en deshidratación/contraste (riesgo de acidosis láctica).

---

## C9 — Seguridad (FAERS): señales de clase, todas manejables

FAERS es numerador sin denominador y confundido por indicación — sirve para confirmar experiencia
pediátrica y AE de clase:

- **Experiencia pediátrica existe**: metformina 523 · sirolimus 672 · aspirina 1.344 reportes en
  <18 a. Fisetina/NR: perfil de suplemento (NR: 36 reportes totales).
- **Metformina**: acidosis láctica (19.411 reportes; 86 pediátricos) — rara, ligada a fallo renal →
  **valida el caveat renal**. Déficit de B12.
- **Dasatinib**: derrame pleural (AE #1), hepatotoxicidad, citopenias → **confirma que es el
  senolítico más riesgoso** → preferir fisetina.
- **Navitoclax**: trombocitopenia es el AE #2 → **dosis-limitante**, confirmado → BH3-miméticos
  BCL-xL-selectivos como alternativa.
- **Nicotinamida** (no NR): daño hepático a dosis alta (272 reportes) → preferir **NR**, no
  megadosis de nicotinamida.
- **Aspirina**: síndrome de Reye → suspender en virosis febril / peri-cirugía (ya en frontier F).

---

## Cómo queda el set de Track 2 tras las 11 líneas de evidencia

| candidato | curado | C1 red | C2 lit | C3+C4 firma | C5 RWR | C6 vías | C7 clínico | C8 dosis ped | C9 FAERS | C10 diana | veredicto |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| **Fisetina** (senólisis) | ✓ 1ª | — (no está en C1) | ✓ 11 PMID | — (no aparece en C3/C4) | ~ débil (z≈1–1,4) | ✓ río abajo | ⚠️ solo adultos (NCT04733534, ≥18 a) | ⚠️ dosis de adultos, extrapolada | — sin datos FAERS (suplemento) | SIRT1/2 drogables, sop. genético | **3º por evidencia pediátrica** · mecanismo fuerte, sin ensayo pediátrico |
| **Metformina** (AMPK) | ✓ | ✓ z=−3.7 | ✓ marco repurposing | — (no aparece en C3/C4) | ✓ río abajo (z 2,8) | ✓ río abajo | ✓✓ **NCT03398824 Fanconi** | ✓ NCT03398824 | ⚠️ acidosis láctica (renal) | **AMPK: sop. genético cáncer** | **1º · la mejor respaldada** |
| **NR / nicotinamida** (NAD+→SIRT2→BubR1) | ✓ | — (z −0,8, sin señal) | ✓ 29 PMID | — | — | — | ✓ NCT04870866 (A-T) | ✓ 25 mg/kg (Veenhuis, 17/24 niños) | — (36 reportes: sin datos útiles) | NAMPT drogable | **2º · adyuvante, muy seguro** |
| vigilancia tumoral | ✓ | — | ✓ | — | — | — | estándar de cuidado | AACR 2024 | — | — | **base (probado)** |
| aspirina + resveratrol | ✓ | ✓ | ✓ | — | ✓ **z=4,2** aneupl. | — | ✓ CAPP (Lynch) | ✓ | ⚠️ Reye | COX-2: 79 fármacos | contexto |
| D+Q (dasatinib) | ✓ alt | ✓ z=−3.4 | ⚠️ "induce aberraciones cromosómicas" | ✓ | ✓ río abajo | ✓ | ✓ | ⚠️ placa de crecimiento | ⚠️ derrame pleural | — | **reserva** (si fisetina falla) |
| navitoclax | ✓ | ✓ z=−2.2 | ✓ 15 PMID | — | ✓ | ✓ | ✓ (mielofibrosis) | ⚠️ | ⚠️ trombocitopenia | **BCL2/xL: sop. genético cáncer** | **reserva** |
| rapamicina | ✓ | ✓ z=−4.0 | ✓ 53 PMID | ✓ | ~ (sirolimus z 1,5; temsirolimus 2,2) | ✓ | ✓ progeria/FAP | uso ped establecido | inmunosupresión | mTOR: 26 fármacos, sop. genético | **hipótesis** (no 1ª línea) |
| 17-AAG / HSP90i | ✓ (Tang-Amon) | ✓ **z=−4.2** | — | ✓ (C3 2/2; C4 MOA) | ✓ (pero es hub) | — | ❌ 38 ensayos, abandonado | ❌ no aprobado | ❌ | HSP90: sop. genético cáncer | **validación mecanística, NO candidato** |
| Aurora/MPS1/PLK i · **BUB1B** | ❌ | (aparecen) | (aparecen) | — | (top del módulo del gen) | — | — | — | — | **pan-esencial, 0 fármacos** | **contraindicados / intratable** |

**Sin cambios respecto al set curado — ahora con 11 líneas de evidencia independientes detrás, y
2 refinamientos ya incorporados** (fisetina > D+Q por estabilidad cromosómica; metformina con
precedente directo en Fanconi + caveat renal por la nefrocalcinosis del probando).

**La innovación del enfoque** (para la methods form): unir explícitamente los **dos ejes que
derivan del mismo defecto de BubR1**, mostrar que **múltiples métodos ortogonales convergen** en
ese marco sin proponer nada nuevo fuera de él, y **aterrizarlo en un régimen pediátrico concreto
compatible con la farmacogenómica real del paciente**.
