
#Building
FROM node:20-alpine AS build 
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
# npm ci installs packages only from packages.json

COPY . .
RUN npm run build


#Running

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
