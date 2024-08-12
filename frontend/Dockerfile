# Этап сборки
FROM node:alpine as build

WORKDIR /app

# Копируем файлы зависимостей
COPY package.json package-lock.json ./
RUN npm install

# Копируем остальные файлы приложения
COPY . .

# Собираем проект
RUN npm run build  # Это также создаст папку out, если конфиг настроен

# Этап запуска
FROM nginx:stable-alpine

# Копируем экспортированные файлы в nginx
COPY --from=build /app/out /usr/share/nginx/html

# Открываем порт 3000 (или 80, если nginx)
EXPOSE 80

# Запускаем nginx
CMD ["nginx", "-g", "daemon off;"]
