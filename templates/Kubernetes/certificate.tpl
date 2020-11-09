apiVersion: cert-manager.io/v1alpha2
kind: Certificate
metadata:
  name: {{config.project_name}}-cert
  namespace: {{config.project_name}}
spec:
  secretName: {{config.project_name}}-cert
  issuerRef:
    name: {{config.issuer_name}}
    kind: ClusterIssuer
  commonName: {{config.project_name}}.kubepaas.ml
  dnsNames:
  - {{config.project_name}}.{{config.dns_name}}