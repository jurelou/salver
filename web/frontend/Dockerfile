
FROM node:15-alpine

WORKDIR /opt/frontend

COPY package*.json ./

RUN npm install

ENTRYPOINT [ "npm", "run", "serve" ]