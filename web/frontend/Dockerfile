
FROM node:15-alpine

WORKDIR /opt/frontend

COPY package*.json ./


RUN npm install -g package.json 

ENTRYPOINT [ "npm", "run", "serve" ]
