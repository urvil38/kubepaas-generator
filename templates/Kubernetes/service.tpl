kind: Service
apiVersion: v1
metadata:
  namespace: {{config.project_name}}
  name: {{config.project_name}}-service
spec:
  selector:
    app: {{config.project_name}}
  ports:
  - protocol: TCP
    port: 80
    targetPort: {{config.container_port}}
  type: ClusterIP