apiVersion: v1
kind: ConfigMap
metadata:
  name: {{config.project_name}}-conf
  namespace: {{config.project_name}}
data:
{% if 'configmap_data' in config %}
  {{config.configmap_data}}
{% endif %}