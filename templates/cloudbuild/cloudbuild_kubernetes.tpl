{
    "source" : {
        "storageSource" : {
            "bucket": "{{build.source_bucket}}",
            "object": "{{build.source_object}}"
        }
    },
    "steps": [
        {
            "name": "gcr.io/cloud-builders/kubectl",
            "args": [
                "apply",
                "-f",
                "."
            ],
            "env": [
                "CLOUDSDK_COMPUTE_ZONE={{build.compute_zone}}",
                "CLOUDSDK_CONTAINER_CLUSTER={{build.cluster_name}}"
            ]
        }
    ],
    "logsBucket": "gs://{{build.log_bucket}}",
    "options": {
        "logStreamingOption": "{{build.logs_stream_option}}"
    }
}