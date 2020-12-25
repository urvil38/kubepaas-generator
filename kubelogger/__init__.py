import subprocess


class KubeLogger:
    def __init__(self, config):
        self.name = config.get('name')
        self.tail = config.get('tail')
        self.since = config.get('since')
        self.stream = config.get('stream')

    def get_log(self):
        args = ["kubectl", "logs", "deployment/" + self.name, "-c", self.name]
        if self.since is not None:
            args.append(f"--since={self.since}")
        if self.tail is not None:
            args.append(f"--tail={self.tail}")
        if self.stream is not None and self.stream == 'true':
            args.append("-f")
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if process.stderr is not None:
            print(process.stderr)
        return process.stdout
