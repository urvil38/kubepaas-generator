# PLEASE DO NOT EDIT 
# AUTOGENERATED WITH KUBEPAAS-GENERATOR

FROM {{config.docker_image}}
RUN touch /etc/nginx/wasm.mime.types && echo "types { application/wasm    wasm; }" >> /etc/nginx/wasm.mime.types
WORKDIR /usr/share/nginx/html
COPY {{config.static_dir}} .