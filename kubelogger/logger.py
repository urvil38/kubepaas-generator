import subprocess

from gevent.select import select


class KubeLogger:
    def __init__(self, config):
        self.name = config.get('name')
        self.tail = config.get('tail')
        self.since = config.get('since')
        self.stream = config.get('stream')
        self.container_name = config.get('container_name')

    def get_log(self):
        args = ["kubectl", "logs", "deployment/" + self.name, "-n", self.name]
        if self.container_name is not None:
            args.extend(["-c", self.container_name])
        else:
            args.extend(["-c", self.name])
        if self.since is not None:
            args.append(f"--since={self.since}")
        if self.tail is not None:
            args.append(f"--tail={self.tail}")
        if self.stream is not None and self.stream == 'true':
            args.append("-f")

        def read_process():
            proc = subprocess.Popen(
                ' '.join(args),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # pass data until client disconnects, then terminate
            # see https://stackoverflow.com/questions/18511119/stop-processing-flask-route-if-request-aborted
            try:
                awaiting = [proc.stdout, proc.stderr]
                while awaiting:
                    # wait for output on one or more pipes, or for proc to close a pipe
                    ready, _, _ = select(awaiting, [], [])
                    for pipe in ready:
                        line = pipe.readline()
                        if line:
                            # some output to report
                            yield line.rstrip() + b'\n'
                        else:
                            # EOF, pipe was closed by proc
                            awaiting.remove(pipe)
                if proc.poll() is None:
                    print("process closed stdout and stderr but didn't terminate; terminating now.")
                    proc.terminate()

            except GeneratorExit:
                # occurs when new output is yielded to a disconnected client
                print("client disconnected, killing process")
                proc.terminate()

            # wait for proc to finish and get return code
            ret_code = proc.wait()
            print(f"process return code: {ret_code}")

        return read_process
