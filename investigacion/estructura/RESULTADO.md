# N1002K — análisis estructural (AlphaFold O60566, BUBR1)

- Residuo N1002: pLDDT **91.1** (muy alta confianza del modelo en esa región).
- **Enterrado** en el núcleo del lóbulo C del dominio pseudoquinasa: 161 átomos pesados a ≤10 Å de su Cα
  (contando los propios).
- Entorno local hidrofóbico/aromático: Ile941, Leu953, Phe954, Trp973, Ser976, Phe977, Trp978,
  Phe996, Phe997, Val998, Arg999, Ile1000, Leu1001, Ala1003, Asn1004, Asp1005, Val1011.
- Lejos del (pseudo)sitio activo: ~19 Å del motivo HRD-like (HGD 880-882) y ~27 Å del DFG-like (DFS 911-913),
  distancias Cα-Cα. **Corregido 12-oct-2026:** antes decía "~35-38 Å del DFG-like", medido por error sobre
  los residuos 895-901. Reproducible con `n1002_structure.py`.
- **Interpretación:** N→K introduce una carga positiva enterrada en un core hidrofóbico →
  penalización de desolvatación + choque estérico + pérdida de puentes H del Asn → mutación
  **desestabilizante del plegamiento**, no de sitio activo. El dominio pseudoquinasa de BUBR1,
  aunque catalíticamente inactivo en humanos, es necesario para localización al cinetocoro,
  ensamblaje del MCC y estabilidad de la proteína → una mutación que desestabiliza su core
  produce **pérdida parcial de función (alelo hipomórfico)**, exactamente el 2º tipo de alelo
  esperado en MVA1 (un null + un hipomórfico; el null bialélico completo es letal embrionario).
- Concuerda con AlphaMissense (0.923, likely pathogenic), que es un score informado por estructura.
