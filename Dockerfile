# PLEASE DO NOT EDIT 
# AUTOGENERATED WITH KUBEPAAS-GENERATOR

FROM python:3.7
WORKDIR /app
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin
COPY requirements.txt .
RUN pip3 install uwsgi==2.0.15 && pip3 install -r requirements.txt
COPY . .
CMD ["python3","app.py"]