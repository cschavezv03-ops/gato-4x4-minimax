# Despliegue

El proyecto son **dos servicios independientes**, cada uno con su propio
`Dockerfile`:

- `backend/` — API FastAPI (Python).
- `frontend/` — sitio estático (Vite) servido con nginx.

## Coolify (recomendado)

Usar el Build Pack **Dockerfile** en cada aplicación. No usar Nixpacks: con
Nixpacks el backend necesita configurar el comando de arranque a mano y el
frontend no se sirve como sitio estático de forma fiable. Los `Dockerfile` ya
resuelven todo eso.

Crear **dos aplicaciones** en Coolify desde este repositorio.

### 1. Backend

| Ajuste | Valor |
|---|---|
| Build Pack | `Dockerfile` |
| Base Directory | `/backend` |
| Puerto | `8000` |

Variable de entorno:

- `CORS_ORIGINS` = URL pública del frontend (ej. `https://gato.midominio.com`)

### 2. Frontend

| Ajuste | Valor |
|---|---|
| Build Pack | `Dockerfile` |
| Base Directory | `/frontend` |
| Puerto | `80` |

Argumento de build (Build Variable / Build Argument):

- `VITE_API_URL` = URL pública del backend (ej. `https://api.midominio.com`)

`VITE_API_URL` se aplica en **tiempo de compilación**: si cambia la URL del
backend, hay que reconstruir el frontend.

### Orden de despliegue

1. Desplegar el **backend** y anotar su URL pública.
2. Desplegar el **frontend** con `VITE_API_URL` apuntando a esa URL.
3. Poner `CORS_ORIGINS` del backend con la URL del frontend y redeplegar.

## Local (Docker Compose)

```bash
docker compose up --build
```

Frontend en http://localhost:5173, backend en http://localhost:8000.

Para apuntar a otras URLs, exportar `VITE_API_URL` y `CORS_ORIGINS` antes de
`docker compose up`.
