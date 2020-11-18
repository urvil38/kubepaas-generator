from generator.kubernetes import KubernetesBuilder

class python_runtime(KubernetesBuilder):
    def __init__(self, config, cluster_config):
        KubernetesBuilder.__init__(self, config, cluster_config)
        self.nginxConf = """
        nginx.conf: |
          server {
            listen 80;
            location / {
                include     uwsgi_params;
                uwsgi_pass  unix:/var/run/generator/uwsgi.sock;
            }
          }
        """

    def generateRuntimeResources(self):
        kubernetesFile = ""

        self.kubernetes["configmap_data"] = self.nginxConf
        self.kubernetes["volumeMount"] = [
            {
                "path": "/var/run/"+self.project_name,
                "name": self.project_name+"-run"
            }
        ]
        self.kubernetes["volumes"] = [
            {
                "configMap": {
                    "name": "nginx-conf",
                    "mount": {
                        "name": self.project_name+"-conf",
                    }
                }
            },
            {
                "emptyDir": {
                    "name": self.project_name+"-run"
                }
            }
        ]

        for resource in ["namespace", "configmap", "service", "python-deployment", "ingress",
                         "networkpolicy"]:
            kubernetesFile += self.generateKubernetesResource(resource)
            kubernetesFile += self.YAML_SEPARATOR

        return kubernetesFile
