FROM node:22-alpine

RUN apk add udev ttf-freefont chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

WORKDIR /usr/src/app
COPY src/ .
RUN npm install

EXPOSE 3000

CMD [ "node", "index.js" ]