{
    "source" : {
        "storageSource" : {
            "bucket": "{{build.source_bucket}}",
            "object": "{{build.source_object}}"
        }
    },
    "steps": [
        {
            "name": "gcr.io/cloud-builders/docker",
            "args": [
                "build",
                "-t",
                "gcr.io/{{build.gcp_project_name}}/{{build.docker_image_name}}",
                "{{build.docker_file_path}}"
            ]
        }
    ],
    "images": [
        "gcr.io/{{build.gcp_project_name}}/{{build.docker_image_name}}"
    ],
    "logsBucket": "gs://{{build.log_bucket}}",
    "options": {
        "logStreamingOption": "{{build.logs_stream_option}}"
    }
}