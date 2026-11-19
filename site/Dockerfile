#
# Build Layer
#
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
# Форма заявки: FormSubmit (письмо на office@dex-it.ru), счётчик Метрики — пусто (не подключён).
ARG PUBLIC_FORM_ENDPOINT=https://formsubmit.co/ajax/office@dex-it.ru
ARG PUBLIC_FORM_EMAIL=office@dex-it.ru
ARG PUBLIC_YM_ID=
ENV PUBLIC_FORM_ENDPOINT=$PUBLIC_FORM_ENDPOINT \
    PUBLIC_FORM_EMAIL=$PUBLIC_FORM_EMAIL \
    PUBLIC_YM_ID=$PUBLIC_YM_ID \
    ASTRO_TELEMETRY_DISABLED=1
RUN npm run build

#
# Final Layer
#
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
