FROM node as build-stage
WORKDIR /code
COPY package*.json ./
RUN npm install --only=production
COPY . .
RUN npm run build

FROM nginx
COPY --from=build-stage /code/dist/ /usr/share/nginx/html
#COPY --from=build-stage /nginx.conf /etc/nginx/conf.d/default.conf