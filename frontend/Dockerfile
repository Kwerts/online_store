# Этап сборки
FROM node:alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# Этап запуска
FROM nginx:stable-alpine

# Удаляем конфигурацию Nginx по умолчанию
RUN rm /etc/nginx/conf.d/default.conf

# Копируем вашу конфигурацию Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копируем сгенерированные статические файлы в директорию Nginx
COPY --from=build /app/.next /usr/share/nginx/html/.next
COPY --from=build /app/public /usr/share/nginx/html/public  # Если есть статические файлы в public
COPY --from=build /app/package.json /usr/share/nginx/html/  # Если это необходимо

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
