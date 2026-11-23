# node:22-alpine: Node 18 está fuera de soporte (T-02)
FROM node:22-alpine

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

# Sin gestores de paquetes en runtime: npm/yarn/corepack de la imagen base traían CVE propias
# y la app ya no los usa (las migraciones llaman a ./node_modules/.bin/prisma)
RUN apk upgrade --no-cache \
 && rm -rf /usr/local/lib/node_modules/npm /usr/local/lib/node_modules/corepack \
           /usr/local/bin/npm /usr/local/bin/npx /usr/local/bin/corepack \
           /opt/yarn-* /usr/local/bin/yarn /usr/local/bin/yarnpkg \
 && chown -R node:node /app
# Usuario sin privilegios que ya trae la imagen oficial de Node
USER node

EXPOSE 3000

# LOW-001: cualquier respuesta HTTP indica que Express está vivo (no hay /health y las rutas usan la BD)
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://127.0.0.1:3000/',()=>process.exit(0)).on('error',()=>process.exit(1))"

CMD ["node", "index.js"]
