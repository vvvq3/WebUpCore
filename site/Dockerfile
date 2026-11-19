#
# Build Layer
#
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
# Форма заявки: письмо через FormSubmit + копия в Telegram через свой обработчик /api/lead (nginx/lead.js).
# PUBLIC_FORM_EMAIL — почта, которая показывается на сайте (и в запасном варианте «письмом»).
ARG PUBLIC_FORM_ENDPOINT=https://formsubmit.co/ajax/office@dex-it.ru
ARG PUBLIC_FORM_EMAIL=office@dex-it.ru
ARG PUBLIC_TG_ENDPOINT=/api/lead
ARG PUBLIC_YM_ID=
ENV PUBLIC_FORM_ENDPOINT=$PUBLIC_FORM_ENDPOINT \
    PUBLIC_FORM_EMAIL=$PUBLIC_FORM_EMAIL \
    PUBLIC_TG_ENDPOINT=$PUBLIC_TG_ENDPOINT \
    PUBLIC_YM_ID=$PUBLIC_YM_ID \
    ASTRO_TELEMETRY_DISABLED=1
RUN npm run build

#
# Final Layer
#
FROM nginx:alpine
# DNS для обработчика заявок берётся из /etc/resolv.conf контейнера
ENV NGINX_ENTRYPOINT_LOCAL_RESOLVERS=1
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf.template /etc/nginx/templates/default.conf.template
COPY nginx/lead.js /etc/nginx/njs/lead.js
COPY nginx/16-default-resolver.envsh /docker-entrypoint.d/16-default-resolver.envsh
RUN chmod +x /docker-entrypoint.d/16-default-resolver.envsh && rm -f /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
