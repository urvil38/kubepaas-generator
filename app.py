import json

from flask import request, make_response, Flask, json, abort, Response

from config import Config
from generator.cloudbuild import CloudBuilder
from generator.docker import DockerFileBuilder
from kubelogger import KubeLogger
from runtime import Runtime

app = Flask(__name__)

cluster_config = Config()


@app.route('/dockerfile', methods=["POST"])
def generate_dockerfile():
    req = request.get_json(silent=True, force=True)
    config = req.get('deploy')

    builder = DockerFileBuilder(config)
    output_text = builder.generate_docker_file()
    if output_text == "":
        return make_response("", 404)
    res = make_response(output_text)
    res.mimetype = "text/plain"
    return res


@app.route('/cloudbuild/t/docker', methods=["POST"])
def generate_cloud_build_for_docker():
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

    builder = CloudBuilder(config, cluster_config)
    output_text = builder.generate_build_config_for_docker()
    res = make_response(output_text)
    res.mimetype = "text/plain"
    return res


@app.route('/cloudbuild/t/kubernetes', methods=["POST"])
def generate_cloud_build_for_kubernetes():
    req = request.get_json(silent=True, force=True)
    project_name = req.get('project_name')
    current_version = req.get('current_version')
    config = {
        "project_name": project_name,
        "current_version": current_version
    }
    builder = CloudBuilder(config, cluster_config)
    output_text = builder.generate_build_config_for_kubernetes()
    res = make_response(output_text)
    res.mimetype = "text/plain"
    return res


@app.route('/kubernetes', methods=["POST"])
def generate_kubernetes_config():
    config = request.get_json(silent=True, force=True)
    runtime = Runtime(config, cluster_config)
    res = make_response(runtime.GenerateKubernetesFile())
    res.mimetype = "text/plain"
    return res


@app.route('/logs/<name>', methods=["GET"])
def get_logs(name=None):
    config = {
        'name': name,
        'since': request.args.get('since'),
        'tail': request.args.get('tail'),
        'stream': request.args.get('stream'),
        'container_name': request.args.get('container_name')
    }
    logger = KubeLogger(config)
    read_line = logger.get_log()
    headers = logger.http_response_headers()
    mime_type = logger.http_mime_type()
    return Response(read_line(), mimetype=mime_type, headers=headers)


@app.route('/', methods=["GET"])
def welcome():
    return "hello to kubepaas generation service"


@app.route('/kubepaas/<type>', methods=["GET"])
def kubepaas_config(type=None):
    if type is None:
        abort(404, description="request resource type was not found!")

    if str(type) == "config":
        conf = {
            "gcp_project": cluster_config.gcp_project,
            "source_bucket": cluster_config.source_bucket,
            "cloudbuild_bucket": cluster_config.cloudbuild_bucket,
            "cloudbuild_secret": cluster_config.build_secret,
            "cloudstorage_secret": cluster_config.storage_secret,
            "domain_name": cluster_config.dns_name
        }

        response = app.response_class(
            response=json.dumps(conf),
            mimetype='application/json'
        )
        return response

    return abort(404, description="Resource not found")
