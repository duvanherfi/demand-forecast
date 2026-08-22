# Pendientes

Diseño completo en
[`superpowers/specs/2026-08-22-demand-forecast-design.md`](superpowers/specs/2026-08-22-demand-forecast-design.md).
Leer eso antes que nada al retomar.

## Planes

Las seis vueltas están planificadas paso a paso, con el código de cada una
ejecutado y verificado antes de escribirlo (34 tests pasan).

| Plan | Vueltas | Tareas |
|---|---|---|
| [vueltas 0 y 1](superpowers/plans/2026-08-22-vueltas-0-y-1.md) | datos, pregunta, baseline, arnés | 1-9 |
| [vuelta 2](superpowers/plans/2026-08-22-vuelta-2.md) | variables, lineal, gradient boosting | 10-14 |
| [vuelta 3](superpowers/plans/2026-08-22-vuelta-3.md) | artefacto, FastAPI, pasarela Go, despliegue | 15-19 |
| [vueltas 4 y 5](superpowers/plans/2026-08-22-vueltas-4-y-5.md) | backtest, deriva, reentrenamiento, red neuronal | 20-24 |

## Falta

- [ ] **Vuelta 0 — datos y pregunta.** Descargar parquet de la TLC, agregar a
      `(zona, hora) → viajes`, escribir la pregunta con precisión. Tareas 1-4.
- [ ] **Vuelta 1 — baseline y arnés.** Partición temporal, cuatro predictores
      tontos, MAE y WAPE (el MAPE se rompe: 41 zonas con menos de 100 viajes
      al mes), marcador. Repo público al terminar. Tareas 5-9.
- [ ] **Vuelta 2a — variables y modelo lineal.** Se pinea en el perfil al
      terminar. Tareas 10-13.
- [ ] **Vuelta 2b — gradient boosting**, comparado contra el lineal y contra
      los cuatro baselines. Tarea 14.
- [ ] **Vuelta 3 — servir peticiones.** FastAPI, pasarela fina en Go por
      delante, artefacto versionado, desplegado en plan gratuito. Tareas 15-19.
- [ ] **Vuelta 4 — que no se pudra.** Backtest mes a mes, deriva,
      reentrenamiento. Tareas 20-22.
- [ ] **Vuelta 5 — red neuronal**, y publicar el resultado gane o pierda.
      Tareas 23-24.

## Hecho

- [x] **Diseño acordado y escrito.** Enfoque en espiral sobre predicción de
      demanda con datos públicos de la TLC de Nueva York; Python 3.12 con `uv`,
      FastAPI para servir, con una pasarela en Go en la vuelta 3; Rails fuera a
      propósito. La profundidad extra se decide al terminar la vuelta 4.
- [x] **Las seis vueltas planificadas al detalle**, 24 tareas, con el código
      ejecutado y verificado antes de escribirlo.

## Verificado el 2026-08-22

Medido contra los servidores de la TLC, no supuesto. Sobre
`yellow_tripdata_2025-01.parquet`: 59 MB, 3 475 226 filas, 261 zonas (ids
1-265), **22 filas con fecha fuera del mes** y **41 zonas con menos de 100
viajes en todo el mes**. Esas dos cifras justifican el filtro de la ingesta y
el descarte del MAPE.

Entorno: Python 3.12.13, pandas **3.0.5** —ojo, `pandas>=2.2` resuelve hoy a la
3, no a la 2—, sklearn 1.9.0, lightgbm 4.7.0, holidays 0.103, Go 1.25.1.
`starlette.testclient` pide **`httpx2`**, no `httpx`.

Tres tests no se pudieron verificar porque necesitan los 700 MB descargados:
`test_pipeline_order.py`, `test_sample.py` y
`test_api.py::test_unknown_zone_is_a_404_not_a_crash`.

## Decisión aplazada

Al terminar la vuelta 4 hay que elegir entre profundizar este repo
(hiperparámetros, importancia de variables, informe escrito) o empezar el
proyecto de música sobre tunebox, que ya guarda historial de escucha real. Se
decide entonces, con lo que hayan preguntado las primeras entrevistas. Nunca en
paralelo.
