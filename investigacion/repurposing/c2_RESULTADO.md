# C2 — Minería de texto completo (Europe PMC)

25 consultas dirigidas · **220 artículos Open Access** con texto completo descargado y escaneado ·
léxico de 6.578 fármacos/compuestos (Broad Repurposing Hub + senoterapéuticos + anti-aneuploidía).
Datos crudos: `c2_hits.json`. (El TSV de contextos completo se descartó por tamaño; los snippets
relevantes están abajo.)

## Qué se puede y qué no

La co-ocurrencia en texto completo es **demasiado ruidosa para generar candidatos nuevos**: el
ranking crudo lo dominan (a) reactivos de laboratorio y metabolitos (glutatión, adenosina, NADPH,
nocodazol, puromicina…) y (b) quimioterapia estándar (cisplatino, doxorubicina, paclitaxel,
etopósido, 5-FU…) que aparece porque los papers de RMS/Wilms/aneuploidía-cáncer la discuten.

**Pero sí sirve como validación cruzada.** Tras filtrar reactivos y quimio, los compuestos que más
co-ocurren con la literatura terapéutica de BUB1B / aneuploidía / senescencia son **exactamente el
set curado**:

| fármaco (curado) | PMIDs | # consultas | contexto en texto completo |
|---|---|---|---|
| **rapamicina** | 53 | 14 | supresor de SASP; senomórfico; droga anti-envejecimiento del ITP (NIA) |
| **resveratrol** | 34 | 12 | SIRT1/IκB, atenúa SASP; probado por el ITP; "la amplificación de centrosomas inducida por 5-FU baja el umbral a la apoptosis por resveratrol" (link directo al eje centrosoma/aneuploidía) |
| **nicotinamida** | 29 | 11 | eje NAD+/sirtuinas (también inhibidor de SIRT a dosis alta — matiz de dosis) |
| **metformina** | 29 | 7 | "compuestos con actividad senolítica/senomórfica como metformina o dasatinib, en uso con otras indicaciones" — marco explícito de reposicionamiento; ensayos de envejecimiento (TAME) |
| **quercetina** | 20 | 9 | D+Q, modulador NF-κB/PI3K/mTOR; senolítico |
| **dasatinib** | 18 | 8 | D+Q en ensayos fase II; ⚠️ "los ITK (imatinib, nilotinib, dasatinib) **inducen aberraciones cromosómicas de novo**" — caución relevante en un paciente cuyo defecto ES inestabilidad cromosómica |
| **aspirina** | 16 | 8 | anti-inflamatorio anti-aging; quimioprevención; probada por el ITP |
| **fisetina** | 11 | 6 | senolítico multi-diana (topoisomerasas, CDKs, NF-κB, PI3K/Akt/mTOR, antioxidante); combinada con luteolina/curcumina |
| **navitoclax (ABT-263)** | 15 | 8 | senolítico canónico, BH3-mimético BCL-2/BCL-xL (Zhu 2016 *Aging Cell*) |

## Dos matices nuevos que aporta C2

1. **Combinaciones de flavonoides como senolítico.** Varios textos: *"luteolina y curcumina
   rindieron bien probadas junto con fisetina como tratamiento senolítico combinado"*; A1331852 /
   A1155463 como inhibidores de BCL-xL más selectivos y menos tóxicos que navitoclax. → la
   recomendación senolítica puede mencionar el **abordaje de flavonoides combinados** (fisetina ±
   luteolina/curcumina) y los BH3-miméticos BCL-xL-selectivos de nueva generación como alternativa
   más segura a navitoclax en un niño.

2. **Caución sobre dasatinib / ITK.** Además del efecto sobre la placa de crecimiento (Frontier F),
   la literatura reporta que los ITK **inducen aberraciones cromosómicas de novo**. En un paciente
   con MVA1 (inestabilidad cromosómica constitucional) esto es un argumento extra para **preferir
   fisetina sobre D+Q**.

## Señal recurrente entre métodos: inhibidores de HDAC

`vorinostat` / `panobinostat` aparecen tanto en C1 (módulo del gen de enfermedad) como en C2
(score ~46, 7 consultas). Hay literatura de HDACi en contextos de inestabilidad cromosómica /
senescencia. **Es un tercer ángulo real pero citotóxico y no-reposicionable** (agentes
oncológicos) — se menciona, no se recomienda.

## Conclusión C2

Ningún candidato **nuevo y limpio**. Confirmación independiente (corpus de texto completo, método
distinto a C1 y al pipeline de Track 2) de que **el set curado es el correcto**, + el matiz de
combinaciones de flavonoides + la caución sobre ITK y estabilidad cromosómica.
