# Этап сборки
FROM node:alpine as build

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Копируем остальные файлы приложения
COPY frontend/ .

# Собираем проект
RUN npm run build  # Это создаст необходимые статические файлы

# Этап запуска
FROM nginx:stable-alpine

# Копируем сгенерированные файлы в директорию Nginx
COPY --from=build /app/.next /usr/share/nginx/html  # Измените на .next, если вы используете серверный рендеринг

# Копируем конфигурацию Nginx (если необходимо)
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80 (по стандарту Nginx)
EXPOSE 80

# Команда запуска Nginx
CMD ["nginx", "-g", "daemon off;"]
