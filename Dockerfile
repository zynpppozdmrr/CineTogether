# 1. Build aşaması
FROM node:18-alpine as build
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# 2. Production aşaması
FROM node:18-alpine as production
WORKDIR /app
COPY --from=build /app ./
RUN npm install --production

EXPOSE 3000
CMD ["npm", "run", "start"]
