apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{config.project_name}}
  namespace: {{config.project_name}}
  annotations:
    date: {{config.date}}
spec:
  selector:
    matchLabels:
      app: {{config.project_name}}
  replicas: {{config.replicas}}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: {{config.project_name}}
    spec:
      containers:
      - name: nginx
        image: nginx:1.13.0
        lifecycle:
          preStop:
            exec:
              command: ["/usr/sbin/nginx","-s","quit"]
        ports:
        - containerPort: 80
          protocol: TCP
        volumeMounts:
        - name: {{config.project_name}}-run
          mountPath: /var/run/{{config.project_name}}
        - name: nginx-conf
          mountPath: /etc/nginx/conf.d
          readOnly: true
      - name: {{config.project_name}}
        imagePullPolicy: "Always"
        image: gcr.io/{{config.gcp_project}}/{{config.project_name}}-{{config.current_version}}:latest
        workingDir: /app
        command: ["/usr/local/bin/uwsgi"]
        {% if config.env is iterable and config.env|length > 0 %}
        env:
        {% for env in config.env %}
        - name: "{{ env.name }}"
          value: "{{ env.value }}"
        {% endfor %}
        {% endif %}
        args:
          - "--die-on-term"
          - "--manage-script-name"
          - "--mount=/=app:app"
          - "--socket=/var/run/{{config.project_name}}/uwsgi.sock"
          - "--chmod-socket=666"
        {% if config.volumeMount is iterable and config.volumeMount|length > 0 %}
        volumeMounts:
        {% for mount in config.volumeMount %}
        - mountPath: {{ mount.path }}
          name: {{ mount.name }}
          {% if "readonly" in mount %}
          readOnly: {{ mount.readonly }}
          {% endif %}
          {% if "subpath" in mount %}
          subPath: {{ mount.subpath }}
          {% endif %}
        {% endfor %}
        {% endif %}
      {% if config.volumes is iterable and config.volumes|length > 0 %}
      volumes:
      {% for volume in config.volumes %}
      {% if "configMap" in volume %}
      - name: {{volume.configMap.name}}
        configMap:
          name: {{volume.configMap.mount.name}}
          {% if volume.configMap.mount.items is iterable %}
          items:
          {% for item in volume["configMap"]["mount"]["items"] %}
            - key: {{ item.key }}
              path: {{ item.path }}
          {% endfor %}
          {% endif %}
      {% elif "emptyDir" in volume %}
      - name: {{volume.emptyDir.name}}
        emptyDir: {}
      {% endif %}
      {% endfor %}
      {% endif %}