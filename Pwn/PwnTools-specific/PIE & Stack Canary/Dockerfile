FROM ubuntu as app
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update

WORKDIR /app/

COPY pwny run
COPY flag.txt flag.txt

FROM pwn.red/jail
COPY --from=app / /srv
ENV JAIL_MEM=20M
ENV JAIL_PORT=1337