from flask import request, make_response, Flask, json, abort

from generator.cloudbuild import Cloudbuilder
from generator.docker import DockerFileBuilder
from generator.kubernetes import KubernetesBuilder
from runtime import Runtime
from config import Config

import json

app = Flask(__name__)

cluster_config = Config()

@app.route('/dockerfile', methods=["POST"])
def generateDockerfile():
    req = request.get_json(silent=True, force=True)
    config = req.get('deploy')

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

    builder = Cloudbuilder(config, cluster_config)
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
    builder = Cloudbuilder(config, cluster_config)
    outputText = builder.GenerateBuildConfigForKubernetes()
    res = make_response(outputText)
    res.mimetype = "text/plain"
    return res


@app.route('/kubernetes', methods=["POST"])
def generateKubernetesConfig():
    config = request.get_json(silent=True, force=True)
    runtime = Runtime(config, cluster_config)
    res = make_response(runtime.GenerateKubernetesFile())
    res.mimetype = "text/plain"
    return res


@app.route('/', methods=["GET"])
def welcome():
    return "hello to kubepaas generation service"

@app.route('/kubepaas/<type>', methods=["GET"])
def kubepaasConf(type=None):
    if type == None:
        abort(404, description="request resource type was not found!")

    if str(type) == "config":

        conf = {
            "gcp_project": cluster_config.gcp_project,
            "source_bucket": cluster_config.source_bucket,
            "cloudbuild_bucket": cluster_config.cloudbuild_bucket,
            "cloudbuild_secret": cluster_config.build_secret,
            "cloudstorage_secret": cluster_config.storage_secret
        }

        response = app.response_class(
            response = json.dumps(conf),
            mimetype = 'application/json'
        )
        return response

    return abort(404, description="Resource not found")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
