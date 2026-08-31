# Predicción de demanda de taxis por zona y hora

Cuántos viajes se originarán en cada zona de Nueva York durante la hora
siguiente, con los datos públicos de la TLC.

## Marcador

Error sobre el mes de validación (2025-11). El mes de prueba (2025-12) sigue
sin tocarse.

| predictor                  |    mae |   wape |
|:---------------------------|-------:|-------:|
| zone x hour x weekday mean |  5.047 | 0.2277 |
| zone mean                  | 13.326 | 0.6012 |
| same hour last week        | 25.551 | 1.1527 |
| global mean                | 31.987 | 1.4431 |


**Léelo así:** un MAE de N significa que la predicción se equivoca en N viajes
por zona y hora. El predictor que gana es zone x hour x weekday mean ya que hay menos equivocación en los viajes.

## Por qué el MAPE no está en esa tabla

41 de las 261 zonas ven menos de 100 viajes en todo un mes, así que las horas
con cero viajes son normales, no excepcionales. El MAPE divide por el valor
real: con un cero abajo, da infinito. La tabla usa MAE —en viajes, que es una
unidad que se entiende— y WAPE, que es adimensional y sobrevive a los ceros.

## Cómo ejecutarlo

Con la muestra que viene en el repo, sin descargar nada:

```bash
make install
make test
```

Con los datos completos (unos 700 MB):

```bash
make download
make ingest
make score
```

## Decisiones

- **Partición por tiempo, nunca aleatoria.** Una partición aleatoria dejaría
  ver febrero mientras se puntúa enero, que no es un error que un modelo
  desplegado pueda cometer. Infla todas las métricas de forma invisible.
  `tests/test_split.py` lo vigila.
- **Las horas sin viajes son ceros, no filas ausentes.** Ausencia de dato y
  demanda cero son cosas distintas; confundirlas hace que el modelo nunca
  aprenda que hay horas muertas.
- **Se descartan las filas fuera de su mes.** Los ficheros de la TLC traen
  filas con fecha de otro mes — 22 en 2025-01.

## Estado

Vuelta 1 de 6. Lo que falta está en [`docs/pendientes.md`](docs/pendientes.md).
El diseño completo, en [`docs/superpowers/specs/`](docs/superpowers/specs/).
