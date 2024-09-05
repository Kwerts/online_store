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

COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
