# syntax=docker/dockerfile:1

FROM node:22-bookworm-slim AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev

FROM node:22-bookworm-slim

WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./
COPY server.js ./

RUN mkdir -p /app/events \
    && chown -R node:node /app

ENV APP_HOST=0.0.0.0
ENV PORT=3003

EXPOSE 3003

USER node

CMD ["node", "server.js"]
