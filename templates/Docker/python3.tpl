# PLEASE DO NOT EDIT 
# AUTOGENERATED WITH KUBEPAAS-GENERATOR

FROM {{config.docker_image}}
WORKDIR /app
COPY requirements.txt .
RUN pip3 install uwsgi==2.0.15 && pip3 install -r requirements.txt
COPY . .
CMD ["python3","app.py"]