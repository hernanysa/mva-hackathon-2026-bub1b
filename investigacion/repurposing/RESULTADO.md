# Frontier C — Reposicionamiento por métodos independientes (segunda opinión de Track 2)

El análisis curado de Track 2 (`../../track2/candidatos_curados.md`) se construyó desde un pipeline
de evidencia + curación manual. Frontier C lo somete a **tres métodos computacionales ortogonales**,
ninguno de los cuales usa esa curación como entrada:

| método | qué usa | archivo |
|---|---|---|
| **C1** proximidad de red | topología del interactoma STRING (15.882 genes) + dianas de 8.706 fármacos | `c1_RESULTADO.md` |
| **C2** minería de texto completo | 220 artículos Open Access de Europe PMC, léxico de 6.578 compuestos | `c2_RESULTADO.md` |
| **C3** reversión de firma | expresión LINCS L1000 (Connectivity Map) vs 3 firmas patológicas | `c3_RESULTADO.md` |

## Resultado principal: convergencia

Los tres métodos + el análisis curado **convergen en el mismo conjunto reducido de mecanismos**.
Ninguno aporta un candidato nuevo, limpio y aprobado fuera de ese marco.

| Mecanismo / fármaco | curado | C1 red | C2 literatura | C3 firma | ¿apropiado para un niño? |
|---|:--:|:--:|:--:|:--:|---|
| **Senólisis — dasatinib+quercetina (D+Q)** | ✓ | ✓ (senesc. z=−2.2 navitoclax) | ✓ 18/20 PMIDs | ✓ (dasatinib revierte firma senescencia) | ⚠️ dasatinib afecta placa de crecimiento (~4%) e **induce aberraciones cromosómicas** (C2) — mal en un chico con RCIU y CIN |
| **Senólisis — fisetina** | ✓ | ~ | ✓ 11 PMIDs (+ combos luteolina/curcumina) | ~ | ✅ mejor perfil de seguridad; ensayo en sobrevivientes ADULTOS de cáncer infantil (NCT04733534, ≥18 a); inhibe CYP2C9 (interacción, no intrínseco) |
| **Activación de AMPK — metformina** | ✓ | ✓ z=−3.7 (AICAR −5.7) | ✓ marco de reposicionamiento explícito | ~ | ✅ perfil pediátrico conocido; OCT1 del probando normal (Frontier A) → respuesta esperable |
| **Inhibición de mTOR — rapamicina/sirolimus** | ✓ | ✓ z=−4.0 | ✓ 53 PMIDs (droga ITP) | ✓ revierte firma aneuploidía | ⚠️ inmunosupresor — cauteloso en un chico con predisposición tumoral e infecciones; uso intermitente / dosis baja como senomórfico es la hipótesis |
| **Precursores de NAD+ (NR / nicotinamida)** | ✓ | sin señal PPI | ✓ 29 PMIDs (eje NAD+/SIRT2→BubR1) | — | ✅ muy seguros; el más "upstream" (podría subir el BubR1 del alelo hipomórfico) |
| **Quimioprevención — aspirina** | ✓ | ✓ z=−6.0 | ✓ (droga ITP, quimioprevención) | — | ✅ dosis baja; G6PD del probando normal (Frontier A) → sin riesgo de hemólisis |
| **Quimioprevención — resveratrol** | ✓ | ✓ (senesc. z=−1.7) | ✓ 34 PMIDs (link a amplificación de centrosoma) | — | ✅ suplemento, muy seguro |
| **Inhibición de HSP90 (17-AAG / geldanamicina)** | ✓ (Tang-Amon) | ✓ **z=−4.2, d_c=0** | — | ✓ **revierte 2/2 firmas** | ❌ NO aprobado, fracasó por toxicidad hepática/ocular — **validación mecanística, no recomendación** |
| Inhibidores de Aurora / PLK / MPS1 | excluidos | ✓ (aparecen) | ✓ (aparecen) | — | ❌ **contraindicados** — inhiben aún más un checkpoint ya débil |
| Inhibidores de HDAC (vorinostat/panobinostat) | excluidos | ✓ | ✓ (recurrente) | ~ | ❌ oncológicos citotóxicos, no reposicionamiento |
| Quimioterapia clásica (cisplatino, doxo, etopósido…) | excluidos (ruido) | ✓ (aparecen) | ✓ (dominan el crudo) | — | es estándar de cuidado tumoral, no reposicionamiento |

## Lo que esto agrega al análisis curado

1. **Robustez.** El set curado no era una corazonada: tres métodos independientes lo reconstruyen.
   La señal computacional más fuerte y consistente es el **eje de estrés proteotóxico/metabólico de
   la aneuploidía** (HSP90, mTOR, AMPK) — exactamente Tang & Amon 2011.
2. **La topología de red confirma que no hay atajo en el gen de enfermedad**: lo único cerca de
   BUB1B/SAC son inhibidores de huso (contraindicados). La oportunidad terapéutica está río abajo.
3. **Dos matices que refuerzan la elección de fármaco:**
   - **Preferir fisetina sobre D+Q**: dasatinib afecta la placa de crecimiento *y* induce
     aberraciones cromosómicas de novo (mal en un paciente con CIN constitucional). C2.
   - **Combos de flavonoides**: fisetina ± luteolina/curcumina, y BH3-miméticos BCL-xL-selectivos
     (A1331852/A1155463) como alternativa más segura a navitoclax. C2.
4. **Farmacogenómica (Frontier A) despeja el camino** para los candidatos seguros: OCT1 normal
   (metformina), G6PD normal (aspirina), CYP2C9 normal (celecoxib/fisetina-interacción manejable),
   CYP3A4 normal (dasatinib PK).

## Set recomendado (sin cambios respecto al curado, ahora con respaldo multi-método)

1. **Senólisis: fisetina** (1ª opción por seguridad; D+Q como alternativa con reservas).
2. **Activación de AMPK: metformina.**
3. **Precursores de NAD+ (NR / nicotinamida)** como adyuvante upstream.
4. **Contexto / quimioprevención de bajo riesgo:** aspirina dosis baja + resveratrol; vigilancia
   tumoral intensiva (eco renal c/3 meses hasta los 7 años, **evitar radiación** — AACR 2024).

Innovación del enfoque: unir explícitamente los **dos ejes** (senescencia + tolerancia a la
aneuploidía) que derivan del *mismo* defecto de BubR1, priorizar agentes seguros para un niño, y
**mostrar que tres métodos ortogonales convergen** en ese marco.
