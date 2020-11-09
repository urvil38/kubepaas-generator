apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: {{config.project_name}}-ingress
  namespace: {{config.project_name}}
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
  tls:
    - hosts:
        - "{{config.project_name}}.{{config.dns_name}}"
  rules:
  - host: {{config.project_name}}.{{config.dns_name}}
    http:
      paths:
        - path: /*
          backend:
            serviceName: {{config.project_name}}-service
            servicePort: 80
  backend:
    serviceName: {{config.project_name}}-service
    servicePort: 80