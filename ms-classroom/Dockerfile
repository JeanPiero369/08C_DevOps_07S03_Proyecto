FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json prisma src index.js ./

RUN npm install --production && npx prisma generate

EXPOSE 3000

CMD ["node", "./index.js"]