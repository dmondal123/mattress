FROM node:20-alpine as build  
LABEL version="1.0"
LABEL description="This is the base docker frontend image for CTO-RND-GENAI-GCP-ASSESSMENT-DEMO2."

WORKDIR /webapp

COPY . .
RUN rm -rf node_modules package-lock.json
RUN npm install
RUN npm run build

FROM nginx:latest
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /webapp/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
