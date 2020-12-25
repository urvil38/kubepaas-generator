from util import get_env


class Config:
    def __init__(self):
        self.build_secret = None
        self.storage_secret = None

        try:
            with open("/secrets/cloudbuild/cloudbuild-secret", "r") as self.build_secret_file:
                self.build_secret = self.build_secret_file.read()
        except Exception as e:
            print(e)

        try:
            with open("/secrets/cloudstorage/cloudstorage-secret", "r") as self.storage_secret_file:
                self.storage_secret = self.storage_secret_file.read()
        except Exception as e:
            print(e)

        self.gcp_project = get_env("GCP_PROJECT")
        self.source_bucket = get_env("SOURCE_BUCKET")
        self.cloudbuild_bucket = get_env("CLOUDBUILD_BUCKET")
        self.issuer_name = get_env("ISSUER_NAME")
        self.compute_zone = get_env("COMPUTE_ZONE")
        self.cluster_name = get_env("CLUSTER_NAME")
        self.dns_name = get_env("DNS_NAME")
        self.dns_ttl = get_env("DNS_TTL", "60")
