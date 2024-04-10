FROM alpine:latest AS alpine-gencerts

RUN apk add bash openssl
COPY certs/ /var/tmp/certs/
WORKDIR /var/tmp/certs
RUN ./gencerts.sh self_cert.conf rsa
# RUN openssl dhparam -out dhparam.pem 4096 # single-cpu bound 

FROM nginx:stable-alpine3.17-slim
RUN apk add openssl bash vim tree
RUN mkdir -p /etc/nginx/certs
COPY --from=alpine-gencerts /var/tmp/certs /etc/nginx/certs/

COPY etc/nginx/nginx.conf /etc/nginx/
COPY etc/nginx/conf.d/    /etc/nginx/conf.d/

EXPOSE 5050 5051 3000

ENTRYPOINT ["nginx", "-g", "daemon off;"] 
