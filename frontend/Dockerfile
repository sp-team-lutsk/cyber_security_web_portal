FROM node as builder

WORKDIR /app
COPY package.json package-lock.json /app/

RUN npm install
COPY . /app

RUN npm run build

EXPOSE 4200
CMD ["npm", "start"]
