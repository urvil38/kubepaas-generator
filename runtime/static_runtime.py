from generator.kubernetes import KubernetesBuilder


class static_runtime(KubernetesBuilder):

    def __init__(self, config):
        KubernetesBuilder.__init__(self, config)
        self.nginxConf = """
    worker_processes  3;
    error_log  /dev/stderr;
    events {
      worker_connections  10240;
    }
    http {
      log_format  main
              'remote_addr:$remote_addr\t'
              'time_local:$time_local\t'
              'method:$request_method\t'
              'uri:$request_uri\t'
              'host:$host\t'
              'status:$status\t'
              'bytes_sent:$body_bytes_sent\t'
              'referer:$http_referer\t'
              'useragent:$http_user_agent\t'
              'forwardedfor:$http_x_forwarded_for\t'
              'request_time:$request_time';
      access_log	/dev/stdout main;
      server {
          include /etc/nginx/mime.types;
          include /etc/nginx/wasm.mime.types;
          root   /usr/share/nginx/html;
          listen       80;
          index  index.html index.htm;
          try_files $uri $uri/ /index.html;
      }
    }
"""

    def generateRuntimeResources(self):
        kubernetesFile = ""

        self.kubernetes["container_port"] = "80"
        self.kubernetes["static_conf"] = self.nginxConf
        self.kubernetes["volumeMount"] = [
            {
                "path": "/etc/nginx/nginx.conf",
                "name": self.project_name+"-conf",
                "readonly": "true",
                "subpath": "nginx.conf"
            },
            {
                "path": "/var/log/nginx",
                "name": "log"
            }
        ]
        self.kubernetes["volumes"] = [
            {
                "configMap": {
                    "name": self.project_name+"-conf",
                    "mount": {
                        "name": self.project_name+"-conf",
                        "items": [
                            {
                                "key": "nginx.conf",
                                "path": "nginx.conf"
                            }
                        ]
                    }
                }
            },
            {
                "emptyDir": {
                    "name": "log"
                }
            }
        ]
        for resource in ["namespace", "configmap", "service", "deployment", "ingress", "certificate",
                         "networkpolicy"]:
            kubernetesFile += self.generateKubernetesResource(resource)
            kubernetesFile += self.YAML_SEPARATOR

        return kubernetesFile
