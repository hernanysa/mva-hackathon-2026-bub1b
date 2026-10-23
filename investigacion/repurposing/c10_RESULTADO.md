# C10 — Open Targets: soporte genético + druggability de las dianas

_Dos ángulos que C1–C9 no tocaron: (1) qué dice un recurso curado de druggability sobre el gen de enfermedad; (2) ¿las dianas de los fármacos propuestos tienen **soporte genético humano** — el predictor de Nelson 2015 de que un fármaco llegue a aprobarse?_


## 1. El gen de enfermedad y el checkpoint — ¿drogables?

| gen | ¿esencial? | drogas/candidatos en OT | esencialidad DepMap (mediana geneEffect) | LoF-constraint |
|---|---|---|---|---|
| BUB1B | **sí** | **0** | -1.21 (min -2.76) | bin 2/6 (intolerante) |
| BUB1 | **sí** | **0** | -0.64 (min -1.5) | bin 2/6 (intolerante) |
| TTK | **sí** | **2** | -0.84 (min -1.89) | bin 2/6 (intolerante) |
| MAD2L1 | **sí** | **0** | -1.37 (min -3.05) | bin 2/6 (intolerante) |
| CDC20 | **sí** | **0** | -2.09 (min -4.27) | bin 3/6 |
| AURKB | **sí** | **18** | -2.2 (min -3.52) | bin 4/6 |
| TRIP13 | no | **0** | -0.24 (min -1.78) | bin 2/6 (intolerante) |

> **BUB1B es pan-esencial** (DepMap geneEffect mediana ≈ −1,2, min −2,8 → inhibirlo mata células en división normales), **0 fármacos/candidatos** en Open Targets, y **muy intolerante a LoF**. Lo mismo para BUB1, TTK, CDC20, AURKB. → **confirmación curada de C1/C5: el checkpoint no es una diana farmacológica útil — inhibirlo es quimioterapia, no terapia dirigida.** (Es coherente con que un doble-null de BUB1B sea letal embrionario.)

## 2. Las dianas de los candidatos — druggability + soporte genético

| diana | eje / fármaco | # fármacos que la tocan (OT) | soporte genético (fenotipo) | soporte genético cáncer/tumor |
|---|---|---|---|---|
| PRKAA1 | metformina / AMPK | **1** | 0.465 (gastric carcinoma) | **0.465** (gastric carcinoma) |
| PRKAA2 | metformina / AMPK | **1** | 0.405 (allergic rhinitis) | **0.353** (ovarian neoplasm) |
| MTOR | rapamicina / mTOR | **26** | 0.931 (isolated focal cortical dysplasia ) | — |
| BCL2L1 | navitoclax / senólisis (BCL-xL) | **3** | 0.195 (Hereditary breast and ovarian canc) | **0.195** (Hereditary breast and ovarian ) |
| BCL2 | navitoclax / venetoclax | **7** | 0.769 (type 2 diabetes mellitus) | **0.762** (lymphoid leukemia) |
| SIRT1 | fisetina / NR (sirtuinas) | **1** | 0.561 (atrial fibrillation) | — |
| SIRT2 | fisetina (SIRT2→BubR1) | **0** | 0.163 (type 2 diabetes mellitus) | — |
| NAMPT | NR / salvamento de NAD+ | **3** | 0.387 (eosinophilic esophagitis) | — |
| HSP90AA1 | 17-AAG / HSP90 (control) | **10** | 0.497 (gout) | **0.489** (ovarian neoplasm) |
| PTGS2 | aspirina / COX-2 | **79** | — | — |
| HDAC1 | vorinostat (recurrente en C1/C2/C4) | **14** | — | — |

_El 'soporte genético' de Open Targets = el gen está genéticamente implicado en esa enfermedad (GWAS/ClinVar/etc.); **no indica la dirección** (protector vs. riesgo). Lo informativo aquí es el contraste: estas dianas están genéticamente ligadas a neoplasia en humanos, mientras que el checkpoint (tabla 1) tiene 0 fármacos y es pan-esencial._

- **Dianas con soporte genético humano (≥0,1) para algún fenotipo:** PRKAA1, PRKAA2, MTOR, BCL2L1, BCL2, SIRT1, SIRT2, NAMPT, HSP90AA1
- **Dianas con soporte genético para cáncer/tumor:** PRKAA1, PRKAA2, BCL2L1, BCL2, HSP90AA1
- **Todas las dianas de los candidatos son 'small-molecule tractable'** y varias ya tienen fármacos aprobados que las tocan — a diferencia del gen de enfermedad (0).

## 3. Lectura

- **El contraste es el punto**: el gen de enfermedad (BUB1B) y todo el checkpoint son **pan-esenciales y sin fármacos** — no hay diana ahí. Las dianas río abajo (AMPK, mTOR, BCL-xL, sirtuinas, NAMPT, COX-2) son **todas drogables y ya tienen fármacos aprobados**.
- **Soporte genético (Nelson 2015):** las dianas con evidencia genética humana para fenotipos relevantes tienen mayor probabilidad de éxito. Ver la tabla — se marca cuáles de nuestras dianas la tienen.
- Open Targets **no propone ningún fármaco para MVA / BUB1B** (0 candidatos). Coincide con C7 (0 ensayos). La estrategia de repurposing río abajo es la única vía.
