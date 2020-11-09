kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  namespace: {{ config.project_name }}
  name: deny-from-other-namespaces
spec:
  podSelector:
    matchLabels:
  ingress:
  - from:
    - podSelector: {}