FROM node:12.13.0

WORKDIR /app
COPY package.json package-lock.json /app/

RUN npm install
COPY . /app

CMD ["npm", "audit", "fix"]
CMD ["npm", "start"]
