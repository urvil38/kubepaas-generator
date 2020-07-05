import os
import datetime
from jinja2 import Template


class KubernetesBuilder(object):
    MIN_REPLICAS = 2
    MAX_REPLICAS = 3
    issuer_name = "letsencrypt-prod"
    gcp_project = "kubepaas-261611"
    YAML_SEPARATOR = "\n---\n"
    KUBERNETES_TEMPLATE_PATH = "./templates/Kubernetes/"

    def __init__(self, config):
        self.project_name = config.get('project_name')
        self.current_version = config.get('current_version')

        deploy = config.get('spec').get('deploy')
        self.container_port = deploy.get('port')
        self.runtime = deploy.get('runtime')
        self.env = deploy.get('env')

        self.kubernetes = {
            "project_name": self.project_name,
            "container_port": self.container_port,
            "current_version": self.current_version,
            "replicas": self.MIN_REPLICAS,
            "issuer_name": self.issuer_name,
            "runtime": self.runtime,
            "gcp_project": self.gcp_project,
            "date": datetime.datetime.now(),
            "env": self.env
        }

    def generateKubernetesResource(self, resourceType):
        template = ""
        with open(self.KUBERNETES_TEMPLATE_PATH+resourceType+".tpl") as tpl:
            template = tpl.read()

        jinjaTemplate = Template(template, trim_blocks=True, lstrip_blocks=True)
        return jinjaTemplate.render(config=self.kubernetes)
