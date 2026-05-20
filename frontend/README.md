# Frontend — Tic-Tac-Toe AI

Web interface for the Tic-Tac-Toe game with 3×3 and 4×4 boards. Single-page
application built with Vite, React, and TypeScript. It consumes the backend API.

## Architecture

```
src/
├── domain/       Domain types (single source of truth)
├── services/     API HTTP client (translates snake_case to camelCase)
├── state/        Reducer: the game state machine (pure)
├── hooks/        useGame: combines the reducer with the API effects
├── components/   Reusable UI components
├── screens/      Screens: menu and game
└── styles/       Design tokens and global styles
```

The rules logic lives only in the backend: the frontend never reimplements it,
which avoids having two sources of truth.

## Requirements

- Node.js 20 or higher

## Installation

```bash
cd frontend
npm install
```

## Running

```bash
npm run dev
```

The app runs at http://localhost:5173 (needs the backend running).

## Scripts

| Script            | Description                                  |
|-------------------|----------------------------------------------|
| `npm run dev`     | Development server.                          |
| `npm run build`   | Type-checks and builds the site into `dist/`.|
| `npm run preview` | Serves the already-built site.               |
| `npm test`        | Runs the tests (Vitest).                     |

## Environment variables

| Variable        | Default                  | Description                          |
|-----------------|--------------------------|--------------------------------------|
| `VITE_API_URL`  | `http://localhost:8000`  | Base URL of the backend API.         |

Vite variables are fixed at build time. For production, set it before running
`npm run build`.

## Design

- Flat Design style, dark theme with a green board and blue accents.
- Plus Jakarta Sans typography.
- Accessible: keyboard navigation, high contrast, `prefers-reduced-motion`.
- Responsive from 320 px: the board adapts to phones, tablets, and desktop.
