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
      - name: {{config.project_name}}
        imagePullPolicy: "Always"
        image: gcr.io/{{config.gcp_project}}/{{config.project_name}}-{{config.current_version}}:latest
        ports:
        - containerPort: {{config.container_port}}
        {% if config.env and config.env|length > 0 %}
        env:
        {% for ev in config.env %}
        - name: {{ ev.name }}
          value: {{ ev.value }}
        {% endfor %}
        {% endif %}
        {% if config.volumeMount|length > 0 %}
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
      {% if config.volumes|length > 0 %}
      volumes:
      {% for volume in config.volumes %}
      {% if "configMap" in volume %}
      - name: {{volume.configMap.name}}
        configMap:
          name: {{volume.configMap.mount.name}}
          items:
          {% for item in volume["configMap"]["mount"]["items"] %}
            - key: {{ item.key }}
              path: {{ item.path }}
          {% endfor %}
      {% elif "emptyDir" in volume %}
      - name: {{volume.emptyDir.name}}
        emptyDir: {}
      {% endif %}
      {% endfor %}
      {% endif %}