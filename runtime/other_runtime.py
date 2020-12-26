from generator.kubernetes import KubernetesBuilder


class OtherRuntime(KubernetesBuilder):
    def __init__(self, config, cluster_config):
        KubernetesBuilder.__init__(self, config, cluster_config)

    def generate_runtime_resources(self):
        kubernetes_file = ""
        for resource in ["namespace", "configmap", "service", "deployment", "ingress",
                         "networkpolicy"]:
            kubernetes_file += self.generate_kubernetes_resource(resource)
            kubernetes_file += self.YAML_SEPARATOR

        return kubernetes_file
