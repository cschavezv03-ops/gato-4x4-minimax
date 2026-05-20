# Backend — Gato IA

API REST que expone la lógica del juego Gato (tres en raya, tableros 3×3 y 4×4)
y la IA (Minimax y poda Alpha-Beta). Adapta el núcleo de `project/src/game/`
sin modificar el original. El tamaño del tablero se deriva del propio tablero,
por lo que las reglas y la IA funcionan igual para ambos tamaños.

## Arquitectura

```
app/
├── core/        Núcleo puro: estado, reglas, constantes (sin dependencias de UI)
├── ai/          Algoritmos: Minimax, Alpha-Beta y evaluación heurística
├── schemas/     Modelos Pydantic (contrato de la API)
├── services/    Orquesta núcleo + IA y traduce al contrato de la API
├── api/         Rutas REST
├── config.py    Configuración leída del entorno
└── main.py      Punto de entrada FastAPI
```

La API es **stateless**: cada petición lleva el tablero completo. No hay base de
datos ni sesiones.

## Requisitos

- Python 3.11 o superior

## Instalación

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Documentación interactiva (Swagger): http://localhost:8000/api/docs

## Tests

```bash
pytest
```

## Variables de entorno

| Variable       | Por defecto                                            | Descripción                              |
|----------------|--------------------------------------------------------|------------------------------------------|
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173`          | Orígenes permitidos por CORS, por comas. |

## Endpoints

| Método | Ruta              | Descripción                                      |
|--------|-------------------|--------------------------------------------------|
| GET    | `/api/health`     | Estado del servicio.                             |
| POST   | `/api/games/new`  | Estado inicial de una partida (`{"size": 3}` o `4`). |
| POST   | `/api/moves`      | Aplica una jugada (422 si es ilegal).            |
| POST   | `/api/ai/move`    | Jugada de la IA con métricas.                    |
| POST   | `/api/ai/compare` | Compara Minimax vs Alpha-Beta sobre el estado.   |

### Parámetros de la IA

- `algorithm`: `minimax` o `alpha_beta`.
- `depth_limit`: profundidad de búsqueda (entero de 1 a 6; por defecto 3).

Si el tablero está vacío, la IA juega una posición aleatoria: la búsqueda completa
desde el tablero vacío es intratable (mismo criterio que el proyecto original).
