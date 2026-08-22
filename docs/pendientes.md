# Pendientes

Diseño completo en
[`docs/superpowers/specs/2026-08-22-demand-forecast-design.md`](superpowers/specs/2026-08-22-demand-forecast-design.md).
Leer eso antes que nada al retomar.

## Falta

- [ ] **Vuelta 0 — datos y pregunta.** Descargar parquet de la TLC, agregar a
      `(zona, hora) → viajes`, escribir la pregunta con precisión.
      Pasos en [`superpowers/plans/2026-08-22-vueltas-0-y-1.md`](superpowers/plans/2026-08-22-vueltas-0-y-1.md).
- [ ] **Vuelta 1 — baseline y arnés.** Partición temporal, cuatro predictores
      tontos, MAE y WAPE (el MAPE se rompe: 41 zonas con menos de 100 viajes
      al mes), marcador. Repo público al terminar. Pasos en el mismo plan.
- [ ] **Vuelta 2a — variables y modelo lineal.** Se pinea en el perfil al
      terminar.
- [ ] **Vuelta 2b — gradient boosting**, comparado contra el lineal y contra
      los cuatro baselines.
- [ ] **Vuelta 3 — servir peticiones.** FastAPI, pasarela fina en Go por
      delante, artefacto versionado, desplegado en plan gratuito.
- [ ] **Vuelta 4 — que no se pudra.** Backtest mes a mes, deriva,
      reentrenamiento.
- [ ] **Vuelta 5 (opcional) — red neuronal**, y publicar el resultado gane o
      pierda.

## Hecho

- [x] **Diseño acordado y escrito.** Enfoque en espiral sobre predicción de
      demanda con datos públicos de la TLC de Nueva York; Python 3.12 con `uv`,
      FastAPI para servir, con una pasarela en Go en la vuelta 3; Rails fuera a
      propósito. La profundidad extra se decide al terminar la vuelta 4.

## Decisión aplazada

Al terminar la vuelta 4 hay que elegir entre profundizar este repo (vuelta 5,
hiperparámetros, importancia de variables, informe) o empezar el proyecto de
música sobre tunebox, que ya guarda historial de escucha real. Se decide
entonces, con lo que hayan preguntado las primeras entrevistas. Nunca en
paralelo.
