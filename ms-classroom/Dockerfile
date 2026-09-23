FROM node:18-alpine

ENV NODE_ENV=production

# Prisma necesita OpenSSL en Alpine
RUN apk add --no-cache openssl

WORKDIR /app

# Dependencias primero para aprovechar la caché de capas
COPY --chown=node:node package.json package-lock.json ./
RUN npm ci --omit=dev

COPY --chown=node:node prisma ./prisma
RUN npx prisma generate

COPY --chown=node:node index.js ./
COPY --chown=node:node src ./src

RUN chown -R node:node /app
# Usuario sin privilegios que ya trae la imagen oficial de Node
USER node

EXPOSE 3000

CMD ["node", "index.js"]
