# Pipeline de análisis — MVA Hackathon 2026

Probando: `WGS_EX2312012` · WGS Illumina, GATK 4.2.4.0, **GRCh38** (contigs Ensembl `1..22,X,Y`), corrido en DNAnexus (feb-2025). Muestra única, **sin trío**.
Sexo genético: **masculino (XY)** — chrX ~0.48× dosis autosómica, ~4.6k het en X vs ~65k en autosoma equivalente; chrY presente.

## Restricción de cómputo (importante)

Máquina: **Intel i7-6500U (2 núcleos / 4 hilos, 2015), 11 GB RAM**.
→ **Alinear las 8 FASTQ (85 GB, ~30×) localmente NO es viable**: `bwa-mem2` necesita ~40 GB RAM solo para el índice de GRCh38; `bwa` clásico entra en RAM pero el alineamiento de ~800M pares de lecturas a 4 hilos son **~15–30 h con la máquina inutilizable** (+ swapping). Sort/markdup añaden horas.
→ **Decisión: análisis basado en el VCF** (que ya trae `AD` y `DP` por sitio → alcanza para BAF y dosis). El alineamiento a BAM queda como **fase 2 opcional en una VM cloud** (16+ cores / 64 GB, ~4–6 h) si se necesitan breakpoints de CNV finos o llamado de variantes estructurales.

## Hipótesis (fenotipo + organizador = MVA Society)

**Aneuploidía Variegada en Mosaico (MVA)**, recesiva. Fenotipo: rabdomiosarcoma (HP:0002859) + nefrocalcinosis + talla baja + RCIU severo (~1 kg, 32 sem) + atrofia muscular + abortos recurrentes parentales → "inestabilidad cromosómica" (texto del challenge). Falta microcefalia (sello de MVA) en la lista dada — tenerlo en cuenta.

Genes: **BUB1B** (MVA1, ~50%, rabdomiosarcoma/Wilms) > **TRIP13** (MVA3, renal) > **CEP57** (MVA2) > CENATAC.

## Pasos

| # | script | qué hace | dependencias |
|---|--------|----------|--------------|
| 0 | `extraer_todo.py` | 1 pasada stdlib: BAF/pos, cobertura en bins, ventanas de gen | — (hecho) |
| 1 | `01_cnv_baf.py` | CNV genome-wide + BAF / aneuploidía mosaico desde el VCF; figura genome-wide; segmentos | pysam, numpy, matplotlib |
| 2 | `02_genes_candidatos.py` | panel de 20 genes (coords Ensembl REST) → variantes PASS → anotación VEP REST (consecuencia/gnomAD/ClinVar/AlphaMissense) → shortlist priorizado | pysam, red |
| 3 | `03_reporte.py` | ensambla hallazgos → informe markdown | — |

Extras si hacen falta: ClinVar VCF completo (`clinvar.vcf.gz`, ~90 MB) como respaldo si VEP REST limita; `mosdepth`/CNV desde BAM si se hace la fase 2 cloud.

## Estado (30-ago 15:00)

- Descarga: ~27/85 GB, ETA ~16:35. No instalar nada hasta que termine (satura la red).
- Pasada stdlib hecha. **Cobertura plana en todos los autosomas** (con enmascarado pericentromérico correcto) → sin trisomía/monosomía de cromosoma entero de nivel alto. *(Un "exceso" en chr21/22 fue artefacto de los pile-ups en brazos cortos acrocéntricos — descartado.)*
- BAF: la métrica cruda stdlib no distingue mosaico real de ruido de mapeo → hace falta el paso 1 con las herramientas.
- Genes BUB1B/CEP57/TRIP13: sin LoF bialélico obvio en la mirada rápida; **falta anotación VEP** (un missense patogénico es invisible sin ella) y descartar deleción intragénica de exón.
