# Etapa 1 — construir el sitio estático.
FROM node:22-alpine AS build
WORKDIR /app

# La URL de la API se fija en tiempo de compilación (variables de Vite).
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Etapa 2 — servir los archivos estáticos con nginx.
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
