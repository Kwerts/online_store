# Этап сборки
FROM node:alpine as build

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY package.json package-lock.json ./
RUN npm install

# Копируем остальные файлы приложения
COPY . .  # Убедитесь, что все файлы копируются корректно

# Собираем проект
RUN npm run build  # Это создаст необходимые статические файлы

# Этап запуска
FROM nginx:stable-alpine

# Копируем сгенерированные файлы в директорию Nginx
COPY --from=build /app/.next /usr/share/nginx/html  # По умолчанию выходные файлы могут находиться в .next

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf  # Убедитесь, что путь правильный

# Открываем порт 80
EXPOSE 80

# Команда запуска Nginx
CMD ["nginx", "-g", "daemon off;"]
