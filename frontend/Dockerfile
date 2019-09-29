FROM node as builder

WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm install @angular/cli@8 -g
RUN cd /app && npm install
COPY . /app

RUN cd /app && npm run build

EXPOSE 4200
CMD ["npm", "start"]
