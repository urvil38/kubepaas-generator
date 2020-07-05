from flask import Flask
from flask import request, make_response

from generator.cloudbuild import Cloudbuilder
from generator.docker import DockerFileBuilder
from generator.kubernetes import KubernetesBuilder
from runtime import Runtime

app = Flask(__name__)

dockerTemplatePath = "./templates/Docker/"


@app.route('/dockerfile', methods=["POST"])
def generateDockerfile():
    req = request.get_json(silent=True, force=True)
    config = req.get('deploy')
    print config
    builder = DockerFileBuilder(config)
    outputText = builder.GenerateDockerFile()
    if outputText == "":
        return make_response("", 404)
    res = make_response(outputText)
    res.mimetype = "text/plain"
    return res


@app.route('/cloudbuild/t/docker', methods=["POST"])
def generateCloudBuildForDocker():
    req = request.get_json(silent=True, force=True)
    project_name = req.get('project_name')
    current_version = req.get('current_version')
    docker_file_path = req.get('dockerfilePath')
    config = {
        "project_name": project_name,
        "current_version": current_version
    }

    if docker_file_path != "":
        config["docker_file_path"] = docker_file_path

    builder = Cloudbuilder(config)
    outputText = builder.GenerateBuildConfigForDocker()
    res = make_response(outputText)
    res.mimetype = "text/plain"
    return res


@app.route('/cloudbuild/t/kubernetes', methods=["POST"])
def generateCloudBuildForKubernetes():
    req = request.get_json(silent=True, force=True)
    project_name = req.get('project_name')
    current_version = req.get('current_version')
    config = {
        "project_name": project_name,
        "current_version": current_version
    }
    builder = Cloudbuilder(config)
    outputText = builder.GenerateBuildConfigForKubernetes()
    res = make_response(outputText)
    res.mimetype = "text/plain"
    return res


@app.route('/kubernetes', methods=["POST"])
def generateKubernetesConfig():
    config = request.get_json(silent=True, force=True)
    runtime = Runtime(config)
    res = make_response(runtime.GenerateKubernetesFile())
    res.mimetype = "text/plain"
    return res


@app.route('/', methods=["GET"])
def welcome():
    return "hello to kubepaas generation service"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
