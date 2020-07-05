# PLEASE DO NOT EDIT 
# AUTOGENERATED WITH KUBEPAAS-GENERATOR

FROM {{ config.docker_image }}
WORKDIR /app
ADD package.json .
RUN npm i --only=production
COPY . .
EXPOSE {{ config.port }}
CMD [ "npm", "run","start" ]