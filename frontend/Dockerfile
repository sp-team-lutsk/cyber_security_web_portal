FROM node as builder

WORKDIR /app
COPY package.json package-lock.json /app/

RUN npm install
COPY . /app

RUN npm run build

CMD ["npm", "audit", "fix"]
CMD ["npm", "start"]
