import os

from jinja2 import Template


class DockerFileBuilder:
    BASE_DOCKER_TEMPLATE_PATH = "./templates/Docker/"
    runtimes = {
        "nodejs": "node:13-alpine",
        "golang113": "golang:1.13-alpine",
        "python2": "python:2.7",
        "python3": "python:3.7",
        "web": "nginx:1.17-alpine"
    }
    supported_runtime = ["nodejs", "golang113", "python2", "python3", "web"]

    def __init__(self, config):
        self.runtime = config.get('runtime')
        self.port = config.get('port')
        self.static_dir = config.get('static_dir')
        if self.static_dir is not None:
            self.static_dir = self.static_dir + "/"
        else:
            self.static_dir = "."

    def generate_docker_file(self):
        if self.runtime in self.supported_runtime:
            docker_image = self.runtimes[self.runtime]
        else:
            return ""

        config = {
            "docker_image": docker_image,
            "port": self.port,
            "static_dir": self.static_dir
        }

        if not os.path.exists(self.BASE_DOCKER_TEMPLATE_PATH + self.runtime + ".tpl"):
            return ""
        else:
            with open(self.BASE_DOCKER_TEMPLATE_PATH + self.runtime + ".tpl", 'r') as tpl:
                template = tpl.read()
            jinja_template = Template(template)
            return jinja_template.render(config=config)
