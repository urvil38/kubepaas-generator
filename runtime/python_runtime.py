from generator.kubernetes import KubernetesBuilder


class python_runtime(KubernetesBuilder):
    def __init__(self, config, cluster_config):
        KubernetesBuilder.__init__(self, config, cluster_config)
        self.nginx_conf_tmpl = """
        nginx.conf: |
          server {{
            listen 80;
            location / {{
                include     uwsgi_params;
                uwsgi_pass  unix:/var/run/{project_name}/uwsgi.sock;
            }}
          }}
        """

    def generateRuntimeResources(self):
        kubernetesFile = ""

        self.kubernetes["container_port"] = 80
        self.kubernetes["configmap_data"] = self.nginx_conf_tmpl.format(project_name=self.project_name)
        self.kubernetes["volumeMount"] = [
            {
                "path": "/var/run/" + self.project_name,
                "name": self.project_name + "-run"
            }
        ]
        self.kubernetes["volumes"] = [
            {
                "configMap": {
                    "name": "nginx-conf",
                    "mount": {
                        "name": self.project_name + "-conf",
                    }
                }
            },
            {
                "emptyDir": {
                    "name": self.project_name + "-run"
                }
            }
        ]

        for resource in ["namespace", "configmap", "service", "python-deployment", "ingress",
                         "networkpolicy"]:
            kubernetesFile += self.generate_kubernetes_resource(resource)
            if resource == "service":
                print(self.generate_kubernetes_resource(resource))
            kubernetesFile += self.YAML_SEPARATOR

        return kubernetesFile
