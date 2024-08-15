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
RUN npm run build

# Этап запуска
FROM nginx:stable-alpine

# Копируем сгенерированные файлы в директорию Nginx
COPY --from=build /app/.next /usr/share/nginx/html

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80
EXPOSE 80

# Команда запуска Nginx
CMD ["nginx", "-g", "daemon off;"]
