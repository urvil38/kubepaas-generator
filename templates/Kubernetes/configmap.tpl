apiVersion: v1
kind: ConfigMap
metadata:
  name: {{config.project_name}}-conf
  namespace: {{config.project_name}}
data:
{% if 'static_conf' in config %}
  nginx.conf: |
    {{config.static_conf}}
{% endif %}