# Frontend — Gato IA

Interfaz web del juego Gato (tres en raya) con tableros 3×3 y 4×4. Aplicación
de una sola página construida con Vite, React y TypeScript. Consume la API del
backend.

## Arquitectura

```
src/
├── domain/       Tipos del dominio (única fuente de verdad)
├── services/     Cliente HTTP de la API (traduce snake_case a camelCase)
├── state/        Reducer: máquina de estados de la partida (puro)
├── hooks/        useGame: combina el reducer con los efectos de la API
├── components/   Componentes de interfaz reutilizables
├── screens/      Pantallas: menú y partida
└── styles/       Tokens de diseño y estilos globales
```

La lógica de las reglas vive solo en el backend: el frontend nunca la
reimplementa, lo que evita tener dos fuentes de verdad.

## Requisitos

- Node.js 20 o superior

## Instalación

```bash
cd frontend
npm install
```

## Ejecución

```bash
npm run dev
```

La aplicación queda en http://localhost:5173 (necesita el backend en marcha).

## Scripts

| Script           | Descripción                                  |
|------------------|----------------------------------------------|
| `npm run dev`    | Servidor de desarrollo.                      |
| `npm run build`  | Verifica tipos y genera el sitio en `dist/`. |
| `npm run preview`| Sirve el sitio ya construido.                |
| `npm test`       | Ejecuta los tests (Vitest).                  |

## Variables de entorno

| Variable        | Por defecto              | Descripción                          |
|-----------------|--------------------------|--------------------------------------|
| `VITE_API_URL`  | `http://localhost:8000`  | URL base de la API del backend.      |

Las variables de Vite se fijan en tiempo de compilación. Para producción,
defínela antes de `npm run build`.

## Diseño

- Estilo Flat Design, tema oscuro con tablero verde y acentos azules.
- Tipografía Plus Jakarta Sans.
- Accesible: navegación por teclado, contraste alto, `prefers-reduced-motion`.
- Responsive desde 320 px: el tablero se adapta a móviles, tablets y escritorio.
