FROM node:12.13.0

WORKDIR /app
COPY package.json package-lock.json /app/

RUN npm install @angular-devkit/build-angular
RUN npm install
COPY . /app

RUN npm run build

CMD ["npm", "audit", "fix"]
CMD ["npm", "start"]
