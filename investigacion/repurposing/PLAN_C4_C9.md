# Track 2 — segunda tanda de pruebas (C4–C10)

Track 1 cerrado. Antes de redactar el report de Track 2, se le sumó rigor con estos análisis,
cada uno atacando un flanco distinto que un revisor va a mirar. Ninguno usa el set curado
como entrada — son verificaciones independientes.

| # | análisis | qué flanco cubre | fuente | estado |
|---|---|---|---|---|
| **C4** | reversión de firma con firma **real** de BubR1 (GEO) | C3 usó marcadores de literatura; esto usa datos primarios | GSE277997 + GSE134781 + L1000CDS2 | ✅ `c4_RESULTADO.md` |
| **C5** | robustez de la proximidad de red (RWR / personalized PageRank, STRING≥700 y ≥900) | ¿la conclusión de C1 depende de la métrica? | STRING v12 local (PPR con numpy, sin scipy) | ✅ `c5_RESULTADO.md` |
| **C6** | enriquecimiento de vías del interactoma de BUB1B | respaldo cuantitativo de los "dos ejes" | Enrichr REST | ✅ `c6_RESULTADO.md` |
| **C7** | búsqueda sistemática de precedente clínico | ¿es una idea disparatada o hay ensayos? | ClinicalTrials.gov v2 | ✅ `c7_RESULTADO.md` |
| **C8** | dosis pediátrica + PK + interacciones para ESTE chico | pasar de "teórico" a "accionable" | labels + C7 + frontier A (PGx) | ✅ `c8_RESULTADO.md` |
| **C9** | minería de señales de seguridad (FAERS) | ¿seguro en un niño con este fenotipo? | openFDA FAERS | ✅ `c9_RESULTADO.md` |
| **C10** | soporte genético + druggability de las dianas | ¿el gen es drogable? ¿las dianas tienen soporte genético humano? (Nelson 2015) | Open Targets GraphQL | ✅ `c10_RESULTADO.md` |

**Síntesis: `RESULTADO_SEGUNDA_TANDA.md`.**

Resultado global: el set curado **no cambia** — ahora con **11 líneas de evidencia independientes**
(curado + C1–C10) y 2 refinamientos ya incorporados (fisetina > D+Q; metformina con precedente
directo en Fanconi + caveat renal por la nefrocalcinosis del probando).

**Con esto se cierra el cómputo de Track 2.** Pendiente: redactar el report + methods form + video.
