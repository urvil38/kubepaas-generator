from generator.kubernetes import KubernetesBuilder
from runtime.other_runtime import other_runtime
from runtime.static_runtime import static_runtime


class Runtime(KubernetesBuilder):
    def __init__(self, config):
        KubernetesBuilder.__init__(self, config)
        self.s_runtime = static_runtime(config)
        self.o_runtime = other_runtime(config)


    def GenerateKubernetesFile(self):
        kubernetesFile = ""
        if self.runtime == "static":
            kubernetesFile = self.s_runtime.generateRuntimeResources()
        else:
            kubernetesFile = self.o_runtime.generateRuntimeResources()
        return kubernetesFile
