# Этап сборки
FROM node:alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# Этап запуска
FROM nginx:stable-alpine

WORKDIR /usr/share/nginx/html

# Попробовать копировать .next целиком
COPY --from=build /app/.next ./
COPY --from=build /app/public ./public

# Копировать конфигурацию Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
