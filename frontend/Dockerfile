# Etapa 1: Compilación de Flutter Web
FROM ghcr.io/cirrusci/flutter:stable AS build-stage

WORKDIR /app

# Descarga de dependencias
COPY pubspec.yaml pubspec.lock ./
RUN flutter pub get

# Copia de código fuente y construcción bundle producción
COPY . .
RUN flutter build web --release

# Etapa 2: Servidor Nginx ultra-ligero para servir Flutter Web en Producción
FROM nginx:alpine AS production-stage

COPY --from=build-stage /app/build/web /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
