# Track 2 — síntesis curada (para revisar y convertir en report)

Del pipeline de evidencia (`out/candidatos_track2.md` = crudo, 1432 fármacos con ruido).
Acá está lo que **realmente tiene fundamento mecanístico para BUB1B-MVA1**, filtrado a mano.

---

## La cadena mecanística (lo que hay que explicar en el report)

**BUB1B → BUBR1** (pérdida de función bialélica, hipomórfica):

BUBR1 es una pseudoquinasa del cinetocoro, componente del **complejo de checkpoint mitótico
(MCC: BUBR1–BUB3–MAD2–CDC20)** que inhibe al **APC/C** hasta que todos los cromosomas están
correctamente unidos al huso. Con BUBR1 hipomórfico → **checkpoint de ensamblaje del huso (SAC)
debilitado** → dos consecuencias, cada una con su vía terapéutica:

| Consecuencia | Fenotipo del probando | Vía terapéutica |
|---|---|---|
| **1. Missegregación cromosómica** → aneuploidía mosaico constitucional + separación prematura de cromátides | predisposición a rabdomiosarcoma, tumor de Wilms | atacar la **vulnerabilidad de los clones aneuploides** |
| **2. Insuficiencia de BubR1** → senescencia celular acelerada, fenotipo progeroide | RCIU severo, retraso del crecimiento, atrofia muscular, falla de medro | **eliminar las células senescentes acumuladas** (senolíticos) |

> Clave: el ratón **BubR1^H/H** (hipomorfo) es **el modelo fundador del campo de los senolíticos**
> (Baker et al., *Nature* 2011, PMID 22048312 — "Clearance of p16Ink4a-positive senescent cells
> delays ageing-associated disorders"). El vínculo BUB1B ↔ senescencia no es analógico: es directo.
> Revisión que une los dos ejes: PMID 25964054 (*Trends Mol Med* 2015, "BubR1 kinase: protection
> against aneuploidy and premature aging").

---

## EJE 1 — Senolíticos (el fenotipo progeroide / falla de crecimiento)

### 1a. Dasatinib + Quercetina (D+Q)
- **Dasatinib**: inhibidor de tirosina-quinasas, **aprobado FDA** (LMC, LLA Ph+). **Quercetina**:
  flavonoide (suplemento). Juntos = el primer combo senolítico descrito (Zhu et al. 2015).
- Evidencia específica: **NCT04733534** — ensayo abierto de D+Q y fisetina para reducir senescencia
  y fragilidad en **sobrevivientes ADULTOS (≥18 a) de cáncer infantil** (SEN-SURVIVORS; población
  cercana por senescencia inducida por quimio, pero NO pediátrica). Múltiples ensayos
  de fase 2 en fragilidad, ERC, fibrosis pulmonar, Alzheimer.
- Racional MVA: si BubR1-bajo causa el fenotipo progeroide vía células senescentes p16+, limpiarlas
  es exactamente lo que rescató a los ratones BubR1^H/H.

### 1b. Fisetina
- Flavonoide (suplemento). "Fisetin is a senotherapeutic that extends health and lifespan"
  (Yousefzadeh et al. 2018, PMID 30279143). Perfil de seguridad muy favorable, en múltiples ensayos.
- Ventaja sobre D+Q para un chico: sin la toxicidad de dasatinib.

### 1c. NAD+ / nicotinamida / NR — para *subir* BubR1 (mecanísticamente directo)
- **SIRT2 induce la quinasa BubR1 para aumentar la longevidad** (North et al. 2014, PMID 24825348).
  El eje NAD+→SIRT2→BubR1 sugiere que **reponer NAD+ podría elevar el BubR1 residual del alelo
  hipomórfico**. Nicotinamida, nicotinamida ribósido (NR), NMN — suplementos, muy seguros.
- Es el candidato más "upstream": ataca la causa, no la consecuencia. Evidencia solo preclínica.

---

## EJE 2 — Vulnerabilidad de los clones aneuploides (la predisposición a cáncer)

### 2a. Metformina
- Biguanida **aprobada** (diabetes). Activa AMPK → estrés energético. Las células aneuploides tienen
  estrés metabólico y proteotóxico basal (Torres/Amon).
- Soporte: **"Identification of aneuploidy-selective antiproliferation compounds"** (Tang, Amon et al.,
  *Cell* 2011, PMID 21315436) — el screening encontró **AICAR** (agonista AMPK, análogo de metformina)
  y **17-AAG** (HSP90) como selectivos de células aneuploides.
- Bonus: metformina tiene datos de quimioprevención en varios contextos; perfil pediátrico conocido.

### 2b. Resveratrol + Aspirina (eliminación de células tetraploides)
- **"Resveratrol and aspirin eliminate tetraploid cells for anticancer chemoprevention"**
  (PMID 24516128). Ataca directamente los precursores poliploides/aneuploides que originan tumores.
- Ambos OTC, baratos, muy seguros. Ángulo de quimioprevención pura.

### 2c. Hidroxicloroquina (inhibición de autofagia) — más especulativo
- Las células aneuploides dependen de autofagia para la proteostasis. HCQ **aprobada** (malaria,
  lupus, AR). Evidencia: PMID 21315436 + literatura de "mitotic slippage-induced senescence".
- Riesgo/beneficio menos claro en un chico; mencionar como hipótesis, no como recomendación fuerte.

---

## Contexto — estándar de cuidado actual (no es "repurposing" pero va en el report)

- **Vigilancia tumoral intensiva** (ecografía abdominal seriada, etc.) — es lo que hoy se hace en
  síndromes de predisposición. PMID 31081598 (remisión a largo plazo de tumores de Wilms bilaterales
  en un paciente MVA/PCS) muestra que la detección temprana + quimio estándar (que incluye
  **dactinomicina/vincristina**) funciona.
- **Celecoxib** — hay un ensayo de quimioprevención (NCT00981201); COX-2 en contextos de CIN.

---

## Excluidos (aparecen en el crudo pero NO son candidatos)
- **Cisplatino, carboplatino, etopósido, doxorubicina, vincristina, dactinomicina** — quimioterapia
  estándar, no reposicionamiento (aparecen por la literatura de RMS/Wilms/aneuploidía).
- **Alisertib, barasertib, CFI-402257, MPS1 inhibitors** — inhibidores de Aurora/MPS1, **no aprobados**,
  y conceptualmente contraindicados (inhibir más un checkpoint ya débil).
- Matches de contexto irrelevante (COVID/HIV transcriptome, viabilidad de ovocitos, etc.).

---

## Set recomendado para el report (3 candidatos + contexto)

1. **Senolíticos (fisetina como primera opción por seguridad; D+Q como alternativa)** — Eje 1,
   evidencia más fuerte y más específica (el modelo fundador ES BubR1-bajo).
2. **Metformina** — Eje 2, aprobada, AMPK/aneuploidy-selective, quimiopreventiva.
3. **Precursores de NAD+ (NR/nicotinamida)** — el más upstream (SIRT2→BubR1), como adyuvante.
+ **Contexto:** vigilancia tumoral + resveratrol/aspirina como quimioprevención de bajo riesgo.

Innovación del approach: unir explícitamente los **dos ejes** (senescencia + aneuploidía) que
derivan del *mismo* defecto de BubR1, y priorizar agentes seguros/OTC apropiados para un niño.
