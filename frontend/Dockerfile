# Etapa 1: instalar dependencias y compilar
FROM node:18-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json next.config.ts next-env.d.ts tsconfig.json tailwind.config.ts postcss.config.mjs components.json src ./

RUN npm ci && npm run build

# Etapa 2: ejecutar en producción
FROM node:18-alpine AS runner
WORKDIR /app

RUN addgroup -S nextjs && adduser -S nextjs -G nextjs
USER nextjs

COPY --from=builder --chown=nextjs:nextjs /app/.next /app/node_modules /app/package.json /app/next.config.ts ./

EXPOSE 3000

CMD ["npm", "run", "start"]
