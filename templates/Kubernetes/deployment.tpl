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
        {% if config.env is iterable and config.env|length > 0 %}
        env:
        {% for env in config.env %}
        - name: "{{ env.name }}"
          value: "{{ env.value }}"
        {% endfor %}
        {% endif %}
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
          {% if volume.configMap.mount.items is iterable and volume.configMap.mount.items|length > 0 %}
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