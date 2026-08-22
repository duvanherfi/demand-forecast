# Pendientes

Diseño completo en
[`docs/superpowers/specs/2026-08-22-demand-forecast-design.md`](superpowers/specs/2026-08-22-demand-forecast-design.md).
Leer eso antes que nada al retomar.

## Falta

- [ ] **Vuelta 0 — datos y pregunta.** Descargar parquet de la TLC, agregar a
      `(zona, hora) → viajes`, escribir la pregunta con precisión.
- [ ] **Vuelta 1 — baseline y arnés.** Partición temporal, cuatro predictores
      tontos, MAE y MAPE, marcador. Repo público al terminar.
- [ ] **Vuelta 2a — variables y modelo lineal.** Se pinea en el perfil al
      terminar.
- [ ] **Vuelta 2b — gradient boosting**, comparado contra el lineal y contra
      los cuatro baselines.
- [ ] **Vuelta 3 — servir peticiones.** FastAPI, artefacto versionado,
      desplegado en plan gratuito.
- [ ] **Vuelta 4 — que no se pudra.** Backtest mes a mes, deriva,
      reentrenamiento.
- [ ] **Vuelta 5 (opcional) — red neuronal**, y publicar el resultado gane o
      pierda.

## Hecho

- [x] **Diseño acordado y escrito.** Enfoque en espiral sobre predicción de
      demanda con datos públicos de la TLC de Nueva York; Python 3.12 con `uv`,
      FastAPI para servir; Rails y Go fuera a propósito.

## Después de esto

Segundo proyecto sobre música apoyado en tunebox, que ya guarda historial de
escucha real. Va después de la vuelta 4, nunca en paralelo.
