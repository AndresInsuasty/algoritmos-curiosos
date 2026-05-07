# algoritmos-curiosos

Demos interactivos en Python para enseñar algoritmos curiosos con visualizaciones sencillas tipo juego.

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Instalación

```bash
uv sync
```

## Demos incluidos

Cada algoritmo tiene su carpeta aislada dentro de `demos/` y también un módulo Python dedicado en `src/algoritmos_curiosos/`.

| Algoritmo | Carpeta | Comando |
| --- | --- | --- |
| Sleep Sort | `demos/sleep_sort/` | `uv run python demos/sleep_sort/main.py` |
| Floyd (Tortuga y Liebre) | `demos/floyd_cycle/` | `uv run python demos/floyd_cycle/main.py` |
| Fast Inverse Square Root | `demos/fast_inverse_square_root/` | `uv run python demos/fast_inverse_square_root/main.py` |
| Bogosort / Quantum Bogosort | `demos/bogosort/` | `uv run python demos/bogosort/main.py` |
| Laberintos con Prim / Kruskal | `demos/maze_generation/` | `uv run python demos/maze_generation/main.py` |

También puedes usar el lanzador:

```bash
uv run algoritmos-curiosos sleep-sort
uv run algoritmos-curiosos floyd
uv run algoritmos-curiosos fast-inverse-sqrt
uv run algoritmos-curiosos bogosort
uv run algoritmos-curiosos maze
```

## Qué muestra cada demo

- **Sleep Sort**: barras que “despiertan” según su valor y van apareciendo ordenadas.
- **Floyd**: animación de la tortuga y la liebre recorriendo una estructura con ciclo.
- **Fast Inverse Square Root**: dos drones persiguen un objetivo; uno usa la raíz exacta y otro la aproximación famosa de Quake III.
- **Bogosort / Quantum Bogosort**: comparación entre mezclar al azar y la variante teórica que “colapsa” al estado ordenado.
- **Prim / Kruskal modificados**: construcción animada de un laberinto y recorrido automático de su solución.

## Controles

- Haz clic en los botones para cambiar parámetros simples.
- `Esc` cierra la demo.
- En la demo de Fast Inverse Square Root puedes hacer clic en el tablero para mover el objetivo.

## Automatización y capturas

Todas las demos aceptan:

```bash
--headless --autoplay --frames 120 --screenshot salida.png
```

Esto permite generar capturas sin abrir ventana real, útil para pruebas o CI.
