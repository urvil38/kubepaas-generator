# PLEASE DO NOT EDIT 
# AUTOGENERATED WITH KUBEPAAS-GENERATOR

FROM {{config.docker_image}}
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE {{config.port}}
CMD ["python3","app.py"]