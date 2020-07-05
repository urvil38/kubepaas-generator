from generator.kubernetes import KubernetesBuilder

class other_runtime(KubernetesBuilder):
    def __init__(self, config):
        KubernetesBuilder.__init__(self, config)

    def generateRuntimeResources(self):
        kubernetesFile = ""

        for resource in ["namespace", "configmap", "service", "deployment", "ingress", "certificate",
                         "networkpolicy"]:
            kubernetesFile += self.generateKubernetesResource(resource)
            kubernetesFile += self.YAML_SEPARATOR

        return kubernetesFile
