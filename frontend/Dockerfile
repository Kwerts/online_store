# Этап сборки
FROM node:alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

FROM nginx:stable-alpine

COPY --from=build /app/.next /usr/share/nginx/html/.next
COPY --from=build /app/public /usr/share/nginx/html/public
COPY --from=build /app/package.json /usr/share/nginx/html/

# Открываем порт 3000
EXPOSE 3000

# Запускаем сервер Next.js
CMD ["npm", "start"]
