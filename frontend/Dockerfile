# Чистый образ для Node.js
FROM node:18

# Размещаем рабочую директорию
WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем все остальные файлы
COPY . .

# Собираем приложение
RUN npm run build

# Указываем команду для старта приложения
CMD ["npm", "start"]

# Открываем порт
EXPOSE 3000
