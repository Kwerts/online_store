# Этап сборки
FROM node:alpine as build

WORKDIR /app

# Копируем файлы зависимостей
COPY package.json package-lock.json ./

RUN npm install --production

# Копируем остальные файлы приложения
COPY . .

# Собираем проект
RUN npm run build

# Этап запуска
FROM nginx:stable-alpine

# Копируем сгенерированные файлы из стадии сборки
COPY --from=build /app/.next/standalone ./
COPY --from=build /app/public ./public

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
