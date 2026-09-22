FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json index.js ./
COPY prisma ./prisma
COPY src ./src

RUN npm install --production && npx prisma generate

EXPOSE 3000

CMD ["node", "./index.js"]