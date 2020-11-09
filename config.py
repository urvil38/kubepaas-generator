from util import getEnv

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

    self.gcp_project = getEnv("GCP_PROJECT")
    self.source_bucket = getEnv("SOURCE_BUCKET")
    self.cloudbuild_bucket = getEnv("CLOUDBUILD_BUCKET")
    self.issuer_name = getEnv("ISSUER_NAME")
    self.compute_zone = getEnv("COMPUTE_ZONE")
    self.cluster_name = getEnv("CLUSTER_NAME")
    self.dns_name = getEnv("DNS_NAME")