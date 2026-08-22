# Predicción de demanda por zona y hora — diseño

Fecha: 2026-08-22

## Por qué existe este proyecto

El perfil de GitHub de Duván declara una maestría en desarrollo de aplicaciones
inteligentes y no tiene nada público que la sostenga. Lo más cercano es Smart
Tracking, cuyo código es privado. Todo el trabajo de IA hecho hasta ahora es de
terceros o está bajo NDA, así que hay que construir desde cero.

El proyecto sirve a tres objetivos declarados, en este orden de dificultad:

1. **Backend que además mete IA en producto** — la silla natural dado el perfil.
2. **Ingeniero de ML aplicado** — la más costosa, y la que exige entrenar, medir
   y comparar contra una línea base.
3. **Freelance para clientes** — exige que se pueda enseñar funcionando.

Un solo proyecto los cubre los tres si —y solo si— la parte inteligente se
modela y se evalúa aquí, en vez de delegarse a una API externa. Un sistema que
solo llama a un LLM demuestra 1 y 3, y no demuestra 2 en absoluto.

## Punto de partida

El nivel declarado en fundamentos de ML es **oxidado**: la teoría se reconoce
pero no se escribe sin releer. El plan no da por sabido `pandas` ni
`scikit-learn`, e introduce cada concepto donde hace falta usarlo.

Presupuesto de tiempo asumido: **6-8 horas por semana**. Si cambia, cambian los
plazos, no el contenido ni el orden.

## El problema

**Dado todo lo ocurrido hasta el instante T, predecir cuántos viajes se
originarán en la zona Z durante la hora siguiente.**

Datos: viajes de taxi de Nueva York publicados mensualmente por la TLC en
parquet. Son millones de viajes reales, públicos, y no dependen de datos de
ningún empleador.

Se elige sobre la predicción de ETA por una razón pedagógica: aquí el baseline
tonto —la media histórica de esa zona, a esa hora, ese día de la semana— es
**genuinamente bueno**, y batirlo cuesta. Eso enseña humildad con números en vez
de con sermones, y obliga a entender la fuga temporal de datos, que es el error
que más veces arruina un modelo que parecía excelente.

## Enfoque: espiral

Un problema, resuelto varias veces, cada vuelta con más maquinaria y todas
reutilizando el mismo arnés de evaluación. El repo crece en el sitio y su
historia de git es el relato del aprendizaje.

Se descartaron dos alternativas:

- **Fundamentos primero, proyecto después.** El orden de un curso. Se descarta
  porque produce material no publicable durante semanas, y porque el
  conocimiento sin aplicar se evapora.
- **Producto primero, modelo después.** Montar el servicio y sustituir después
  una predicción falsa. Se descarta porque pone a construir durante días
  aquello que ya está demostrado en otros repos, y aplaza lo único que hay que
  probar.

Lo que de verdad está oxidado no son los algoritmos: es la **disciplina de
evaluación** —baseline antes que modelo, particiones que respeten el tiempo,
una métrica que signifique algo—. La espiral la repite en cada vuelta hasta que
sea instinto.

## Las vueltas

### Vuelta 0 — Los datos y la pregunta (~1 semana)

Descargar los parquet de la TLC, agregarlos a `(zona, hora) → nº de viajes`, y
escribir la pregunta con precisión: qué se predice, con qué horizonte, y con
qué información disponible en el momento de predecir.

**Concepto:** `pandas` aplicado —agrupar, remuestrear por tiempo, unir tablas—,
y por qué la unidad de agregación condiciona todo lo demás.

**Entregable:** `src/ingest.py` y un notebook de exploración.

### Vuelta 1 — El baseline y el arnés (~2 semanas)

La vuelta más importante. El aparato de medir se construye **antes** que
cualquier modelo:

- Partición temporal: entrenar con los primeros meses, validar con el
  siguiente, y reservar el último sin tocarlo hasta el final.
- Cuatro predictores tontos: media global; media por zona; media por
  zona-hora-día de la semana; y "lo mismo que la semana pasada a esta hora".
- Métricas: MAE y MAPE, incluyendo por qué el MAPE se rompe en las zonas de
  poco tráfico.

**Concepto:** fuga temporal de datos; por qué una partición aleatoria miente en
series temporales; qué significa un MAE.

**Entregable:** `src/baselines.py`, `src/evaluate.py` —el arnés que se reutiliza
en todas las vueltas siguientes— y el marcador inicial en `reports/`.

**Hito:** el repo se hace público aquí.

### Vuelta 2 — El primer modelo de verdad (~3 semanas)

Variables derivadas (hora, día de la semana, festivos, retardos, medias
móviles), un modelo lineal primero por interpretable, y después gradient
boosting. Todos pasan por el mismo marcador.

**Concepto:** ingeniería de variables, sobreajuste, regularización, validación
cruzada adaptada al tiempo.

**Entregable:** `src/features.py`, `src/models.py`, marcador actualizado.

**Hito:** se pinea en el perfil, sustituyendo a `ytm_auto_yes`.

**Resultado admisible:** que el modelo **no** le gane al baseline de
zona-hora-día. Si pasa, va en la tabla con su número y su explicación.

### Vuelta 3 — Que sirva peticiones (~1-2 semanas)

Un servicio FastAPI que responde predicciones por HTTP, el modelo entrenado
como artefacto versionado, y el entrenamiento reproducible con un comando.
Desplegado en un plan gratuito (Fly.io o Railway).

**Concepto:** un modelo en un notebook no es un sistema. Serialización,
latencia, y el desajuste entre cómo se calculan las variables al entrenar y
cómo se calculan al servir —el fallo que rompe modelos en producción sin que
nadie se entere—.

**Entregable:** `src/api/`, `docker-compose.yml`, URL viva.

**Hito:** enseñable a un cliente.

### Vuelta 4 — Que no se pudra (~2 semanas)

Backtest mes a mes para ver la degradación, detección de deriva en los datos, y
un reentrenamiento programado.

**Concepto:** lo que separa un proyecto de portafolio de alguien que ha pensado
en producción.

**Entregable:** informe de backtest en `reports/`, trabajo de reentrenamiento.

### Vuelta 5, opcional — Probar una red neuronal

En datos tabulares el gradient boosting suele ganar. Probarlo y publicar que
perdió demuestra criterio: saber cuándo no sacar la herramienta grande. Si
gana, mejor.

## Stack

**Python en todo, hasta la vuelta 3.** El ecosistema de modelado está ahí y
pelearlo desde otro lenguaje es trabajo que no enseña nada. Para servir,
**FastAPI**: mismo lenguaje, cero traducción entre el cálculo de variables al
entrenar y al servir.

Queda fuera Rails y Go deliberadamente: ya están demostrados en otros repos, y
lo que hay que probar aquí es lo otro. Si más adelante interesa hacer explícita
la historia de la silla 1 —*el modelo en Python, el servicio en Go*—, añadir una
pasarela fina en Go sobre la vuelta 3 es un día de trabajo. No se mete al
principio porque distrae con plomería ya dominada.

**Python 3.12 gestionado por `uv`.** El intérprete del sistema es 3.14, donde
parte del ecosistema de ML todavía va con retraso. `uv` fija la versión sin
tocar la instalación del sistema.

## Estructura del repo

```
demand-forecast/
├── src/
│   ├── ingest.py      # parquet crudo → tabla (zona, hora, viajes)
│   ├── features.py    # variables derivadas — idéntico al entrenar y al servir
│   ├── baselines.py   # los cuatro predictores tontos
│   ├── models.py      # lineal, gradient boosting
│   ├── evaluate.py    # el arnés: entra un predictor, sale el marcador
│   └── api/           # FastAPI (vuelta 3)
├── notebooks/         # explorar, nunca la fuente de verdad
├── tests/
├── reports/           # el marcador y las gráficas, versionados
├── data/              # crudo ignorado por git; una muestra pequeña sí se sube
└── Makefile
```

## Reglas

Cada una evita un fallo concreto:

1. **Los notebooks exploran; `src/` es la verdad.** El fallo más común de un
   repo de portafolio es que todo vive en un notebook de 900 celdas que nadie
   puede ejecutar. Lo que funciona se muda a `src/` con un test.
2. **`features.py` es único y compartido entre entrenamiento y servicio.**
   Duplicar ese cálculo es como nacen los modelos que van perfectos en local y
   mienten en producción.
3. **`make train` reconstruye todo desde cero**, con semillas fijas y
   dependencias ancladas. Si no se pueden regenerar los propios resultados, no
   son resultados.
4. **La muestra pequeña de datos se sube al repo.** Así cualquiera clona y
   ejecuta en dos minutos sin bajarse 4 GB. Un reclutador que puede ejecutar el
   proyecto es un reclutador que lo mira.

## Tests

El test que importa no es el del modelo: es **el de la partición temporal**.
Debe verificar que ninguna fila de validación es anterior a la última de
entrenamiento, y que ninguna variable derivada mira al futuro. Una fuga
silenciosa ahí invalida el proyecto entero sin que nada falle ni dé error.

Además: tests de `features.py` (el cálculo de retardos y medias móviles es
donde se cuelan los fallos de índice) y de `ingest.py` (que la agregación
conserve el total de viajes).

## README

Va invertido respecto a lo habitual: **el marcador arriba**, antes de la
arquitectura y antes del stack. Una tabla con cada predictor, su error, la
fecha, y qué gana a qué. Quien lo abra ve en cinco segundos que aquí se mide.

**Lo que pierde también se publica.** Un candidato que publica un resultado
negativo con su número al lado transmite que sus cifras son de fiar.

## Hitos de publicación

| Vuelta | Qué se publica | Para qué habilita |
|---|---|---|
| 1 | Repo público, baseline, marcador | Criterio de evaluación |
| 2 | Primer modelo y su comparación | Se pinea en el perfil |
| 3 | URL viva | Enseñable a un cliente (silla 3) |
| 4 | Backtest y deriva | Entrevista de la silla 2 (ML aplicado) |

Difusión: dos publicaciones, no una por vuelta. Una en la vuelta 2, con el
número y qué sorprendió; otra en la vuelta 3, con la demo viva.

## Fuera de alcance

- **Herramientas de seguimiento de experimentos (MLflow y similares).** Un
  marcador en markdown versionado con git basta hasta la vuelta 4. Añadir
  infraestructura antes de tener experimentos que seguir es sentirse productivo
  sin avanzar.
- **Datos de Picap o de cualquier empleador.** Solo datos públicos.
- **Predicción de ETA, detección de anomalías, y cualquier otro problema del
  dominio.** Un problema, bien resuelto.
- **Aprendizaje profundo antes de la vuelta 5.**

## Qué viene después

Un segundo proyecto sobre música, apoyado en tunebox, que ya guarda historial
de escucha y estadísticas reales en el dispositivo. Costará la mitad porque el
andamiaje —preparación de datos, evaluación, despliegue, documentación— se
reutiliza. Va **después** de la vuelta 4, nunca en paralelo: dos proyectos a la
vez es la forma fiable de acabar con dos repos a medias.
