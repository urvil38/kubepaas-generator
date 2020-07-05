from jinja2 import Template


class Cloudbuilder:
    BUCKET_NAME = "kubepaas-ml"
    CLOUDBUILD_TEMPLATE_PATH = "./templates/cloudbuild/"
    GCP_PROJECT = "kubepaas-261611"
    LOG_BUCKET = "kubepaas-cloudbuild-logs-bucket"
    COMPUTE_ZONE = "asia-southeast1-b"
    CLUSTER_NAME = "kubepaas"

    def __init__(self, config):
        self.user_project_name = config["project_name"]
        self.current_version = config["current_version"]
        self.docker_file_path = config.get('docker_file_path')
        self.stream_option = "STREAM_ON"
        self.stream_log = True

        self.docker_build = {
            "gcp_project_name": self.GCP_PROJECT,
            "source_bucket": self.BUCKET_NAME,
            "docker_image_name": self.user_project_name+"-"+self.current_version,
            "source_object": self.user_project_name+"/"+self.user_project_name+"-"+self.current_version+".tgz",
            "log_bucket": self.LOG_BUCKET,
        }

        self.kubernetes_build = {
            "gcp_project_name": self.GCP_PROJECT,
            "source_bucket": self.BUCKET_NAME,
            "source_object": self.user_project_name+"/"+"kubernetes"+"-"+self.user_project_name+"-"+self.current_version+".tgz",
            "log_bucket": self.LOG_BUCKET,
            "compute_zone": self.COMPUTE_ZONE,
            "cluster_name": self.CLUSTER_NAME
        }

        if self.isLogTrailer():
            self.docker_build["logs_stream_option"] = self.stream_option
            self.kubernetes_build["logs_stream_option"] = self.stream_option
        else:
            self.docker_build["logs_stream_option"] = ""
            self.kubernetes_build["logs_stream_option"] = ""

        if self.docker_file_path is not None and self.docker_file_path != "":
            self.docker_build["docker_file_path"] = self.docker_file_path
        else:
            self.docker_build["docker_file_path"] = "."

    def GenerateBuildConfigForDocker(self):
        template = ""
        with open(self.CLOUDBUILD_TEMPLATE_PATH+"cloudbuild_docker.tpl") as tpl:
            template = tpl.read()

        jinjaTemplate = Template(template)
        return jinjaTemplate.render(build=self.docker_build)

    def GenerateBuildConfigForKubernetes(self):
        template = ""
        with open(self.CLOUDBUILD_TEMPLATE_PATH+"cloudbuild_kubernetes.tpl") as tpl:
            template = tpl.read()

        jinjaTemplate = Template(template)
        return jinjaTemplate.render(build=self.kubernetes_build)

    def isLogTrailer(self):
        return self.stream_log == True
