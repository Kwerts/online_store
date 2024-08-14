# Этап сборки
FROM node:alpine as build

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY package.json package-lock.json ./
RUN npm install

# Копируем остальные файлы приложения
COPY . .

# Собираем проект
RUN npm run build  # Эта команда создаст необходимые статические файлы

# Этап запуска
FROM nginx:stable-alpine

# Копируем файлы из папки out в директорию Nginx
COPY --from=build /app/out /usr/share/nginx/html

# Копируем конфигурацию Nginx (если необходимо)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80 (по стандарту Nginx)
EXPOSE 80

# Команда запуска Nginx
CMD ["nginx", "-g", "daemon off;"]
