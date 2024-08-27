# Этап сборки
FROM node:alpine as build

# Копируем файлы зависимостей
COPY package.json package-lock.json ./
RUN npm install

WORKDIR /app

# Копируем остальные файлы приложения
COPY . .

# Собираем проект
RUN npm run build

# Этап запуска
FROM nginx:stable-alpine

# Копируем сгенерированные файлы в директорию Nginx
COPY --from=build /app/.next /usr/share/nginx/html

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

# Команда запуска Nginx
CMD ["nginx", "-g", "daemon off;"]
