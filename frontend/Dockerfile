# Этап сборки
FROM node:alpine as build

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Копируем все остальные файлы приложения
COPY frontend/ .

# Собираем проект
RUN npm run build  # Это создаст нужные файлы для работы Nginx

# Этап запуска
FROM nginx:stable-alpine

# Копируем сгенерированные файлы в директорию Nginx
COPY --from=build /app/.next /usr/share/nginx/html  # Или другой путь, если не /app/.next

# Копируем конфигурацию Nginx
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80
EXPOSE 80

# Команда запуска Nginx
CMD ["nginx", "-g", "daemon off;"]
