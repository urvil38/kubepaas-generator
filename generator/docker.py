import os
from jinja2 import Template

class DockerFileBuilder:
    BASE_DOCKER_TEMPLATE_PATH = "./templates/Docker/"
    runtimes = {
        "nodejs" : "node:13-alpine",
        "golang113" : "golang:1.13-alpine",
        "python2" : "python:2.7-alpine",
        "static": "nginx:1.17-alpine"
    }
    supported_runtime = ["nodejs","golang113","python2","static"]
    def __init__(self,config):
        self.runtime = config.get('runtime')
        self.port = config.get('port')
        static_dir = config.get('static_dir')
        if static_dir != "":
            self.static_dir = static_dir
        else:
            self.static_dir = "."

    def GenerateDockerFile(self):
        if self.runtime in self.supported_runtime:
            docker_image = self.runtimes[self.runtime]
        else:
            return ""

        config = {
            "docker_image": docker_image,
            "port": self.port,
        }

        template = ""
        if not os.path.exists(self.BASE_DOCKER_TEMPLATE_PATH+self.runtime+".tpl"):
            return ""
        else:
            with open(self.BASE_DOCKER_TEMPLATE_PATH+self.runtime+".tpl",'r') as tpl:
                template = tpl.read()
            jinjaTemplate = Template(template)
            if self.runtime == "static":
                if self.static_dir != ".":
                    config["static_dir"] = self.static_dir + "/"
                else:
                    config["static_dir"] = self.static_dir
            return jinjaTemplate.render(config=config)
