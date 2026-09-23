# Etapa 1: instalar dependencias y compilar
FROM node:18-alpine AS builder
WORKDIR /app

# URL del orchestrator visible desde el navegador (se hornea en el build de Next.js)
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_TELEMETRY_DISABLED=1

# Dependencias primero para aprovechar la caché de capas
COPY package.json package-lock.json ./
RUN npm ci

COPY next.config.ts tsconfig.json tailwind.config.ts postcss.config.mjs components.json ./
COPY src ./src

RUN npm run build && npm prune --omit=dev

# Etapa 2: ejecutar en producción
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1

RUN addgroup -S nextjs && adduser -S nextjs -G nextjs
USER nextjs

COPY --from=builder --chown=nextjs:nextjs /app/.next ./.next
COPY --from=builder --chown=nextjs:nextjs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nextjs /app/package.json /app/next.config.ts ./

EXPOSE 3000

CMD ["npm", "run", "start"]
