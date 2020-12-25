from generator.kubernetes import KubernetesBuilder
from runtime.other_runtime import OtherRuntime
from runtime.python_runtime import python_runtime
from runtime.static_runtime import static_runtime


class Runtime(KubernetesBuilder):
    def __init__(self, config, cluster_config):
        KubernetesBuilder.__init__(self, config, cluster_config)
        self.s_runtime = static_runtime(config, cluster_config)
        self.o_runtime = OtherRuntime(config, cluster_config)
        self.python_runtime = python_runtime(config, cluster_config)

    def GenerateKubernetesFile(self):
        kubernetesFile = ""
        if self.runtime == "web":
            kubernetesFile = self.s_runtime.generateRuntimeResources()
        elif self.runtime == "python2" or self.runtime == "python3":
            kubernetesFile = self.python_runtime.generateRuntimeResources()
        else:
            kubernetesFile = self.o_runtime.generate_runtime_resources()
        return kubernetesFile
