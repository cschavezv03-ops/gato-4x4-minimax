# Gato con IA — Minimax y poda Alpha-Beta

Juego del Gato (tres en raya) con tableros **3×3 y 4×4** y una IA basada en
búsqueda adversaria. Proyecto académico de Inteligencia Artificial — EPN.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?logo=typescript&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

La IA juega como **MAX** (maximiza su puntaje) contra el humano, que actúa como
**MIN**. Para árboles grandes la búsqueda se limita por profundidad y, al
alcanzar el límite, evalúa el tablero con una función heurística.

<p align="center">
  <img src="docs/screenshot.png" alt="Interfaz web del juego: tablero 4×4 con victoria de la IA y panel de métricas" width="420">
</p>

---

## Características

- **Dos tamaños de tablero:** 3×3 y 4×4 — las reglas y la IA derivan el tamaño
  del propio tablero, así que funcionan igual para ambos.
- **Dos modos de juego:** Humano vs Humano y Humano vs IA.
- **Tres algoritmos:** Minimax, Minimax con poda Alpha-Beta y un modo
  comparación que ejecuta ambos sobre el mismo estado.
- **Métricas en vivo:** nodos evaluados, puntaje y tiempo de cálculo.
- **Búsqueda con límite de profundidad** (1 a 6) y heurística para estados no
  terminales.
- **Resaltado de la línea ganadora** al terminar la partida.

---

## Estructura del repositorio

El proyecto tiene tres partes independientes:

| Carpeta      | Qué es                          | Stack                          |
|--------------|---------------------------------|--------------------------------|
| `project/`   | Versión original de consola     | Python                         |
| `backend/`   | API REST que expone juego e IA  | FastAPI · Pydantic             |
| `frontend/`  | Interfaz web                    | Vite · React 19 · TypeScript   |

```
gato-4x4-minimax/
├── project/      # Versión de consola (núcleo original, intacto)
├── backend/      # API REST  →  ver backend/README.md
├── frontend/     # Interfaz web  →  ver frontend/README.md
└── docker-compose.yml
```

`backend/` es una copia adaptada del núcleo de `project/src/game/` (imports
consistentes, type hints, sin acoplamiento a la consola). El módulo original se
deja sin tocar. La lógica de las reglas vive **solo en el backend**: el frontend
nunca la reimplementa, evitando dos fuentes de verdad.

---

## Inicio rápido

La forma más simple de levantar el juego completo (API + web) es con Docker:

```bash
docker compose up --build
```

Luego abrí **http://localhost:5173**.

Para apuntar a otras URLs en un despliegue, exportá antes las variables:

```bash
VITE_API_URL=https://api.midominio.com
CORS_ORIGINS=https://gato.midominio.com
```

---

## Desarrollo local

Cada módulo se ejecuta por separado. Detalles completos en cada README.

**Backend** — requiere Python 3.11+:

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

API en http://localhost:8000 · Swagger en http://localhost:8000/api/docs

**Frontend** — requiere Node.js 20+:

```bash
cd frontend
npm install
npm run dev
```

Web en http://localhost:5173 (necesita el backend en marcha).

→ [`backend/README.md`](backend/README.md) · [`frontend/README.md`](frontend/README.md)

---

## Versión de consola

La versión original vive en `project/` y se juega en la terminal con un menú de
cinco opciones: Humano vs Humano, IA con Minimax, IA con Alpha-Beta, modo
comparación y salir.

```bash
cd project
python3 -m src.game.main
```

---

## La IA

El proyecto aplica los conceptos clásicos de búsqueda adversaria:

| Concepto              | Implementación                                                |
|-----------------------|---------------------------------------------------------------|
| Estados y acciones    | `GameState` inmutable; movimientos legales = celdas vacías.    |
| Estados terminales    | Hay ganador o el tablero está lleno.                          |
| Función de utilidad   | Victoria `+100000`, derrota `-100000`, empate `0`.            |
| Minimax               | Explora el árbol asumiendo juego óptimo de ambos lados.       |
| Poda Alpha-Beta       | Descarta ramas irrelevantes; mismo resultado, menos nodos.    |
| Heurística            | Suma el valor de cada línea cuando se alcanza el límite.      |
| Búsqueda con límite   | Profundidad de 1 a 6 (3 por defecto).                         |

**Heurística:** cada línea (fila, columna o diagonal) vale `10ⁿ` según las
fichas de la IA, y `−10ⁿ` según las del oponente. Una línea mixta no sirve a
nadie y vale `0`. El puntaje del tablero es la suma de todas sus líneas.

**Tablero vacío:** la búsqueda completa desde cero es intratable, así que la IA
abre con una jugada aleatoria (mismo criterio que la versión de consola).

**Comparación:** ambos algoritmos eligen la misma jugada óptima. El modo
comparación mide la diferencia de **nodos evaluados** — la prueba concreta de
que la poda Alpha-Beta hace el mismo trabajo explorando menos.

---

## API REST

La API es **stateless**: cada petición lleva el tablero completo. No hay base de
datos ni sesiones.

| Método | Ruta              | Descripción                                       |
|--------|-------------------|---------------------------------------------------|
| GET    | `/api/health`     | Estado del servicio.                              |
| POST   | `/api/games/new`  | Estado inicial de una partida (`size`: 3 o 4).    |
| POST   | `/api/moves`      | Aplica una jugada (422 si es ilegal).             |
| POST   | `/api/ai/move`    | Jugada de la IA con métricas.                     |
| POST   | `/api/ai/compare` | Compara Minimax vs Alpha-Beta sobre el estado.    |

Contrato completo y parámetros en [`backend/README.md`](backend/README.md) o en
la documentación interactiva de Swagger.

---

## Tests

```bash
cd backend  && pytest      # 60 tests: reglas, IA y API
cd frontend && npm test    # tests del reducer de estado (Vitest)
```

---

## Equipo

**Grupo 5** — Inteligencia Artificial, EPN

- Renato Aguilar
- Sebastián Chávez
- Frank Jumbo
- Dax Navarrete

---

## Licencia

[MIT](LICENSE)
