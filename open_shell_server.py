import argparse
import os
import pwd
import socketserver
import sys
from subprocess import Popen, PIPE

def get_username():
	return pwd.getpwuid(os.getuid())[0]

class Pipe(socketserver.StreamRequestHandler):
	def handle(self):
		while True:
			self.wfile.write("$ ".encode())
			shell_command = self.rfile.readline().strip()
			print(f"Running the following command: `{shell_command.decode()}`")

			capture = Popen(shell_command, stdout=PIPE, stderr=PIPE, shell=True)
			std_out, std_err = capture.communicate()
			if isinstance(std_err, bytes):
				std_err = std_err.decode().rstrip()
			if isinstance(std_out, bytes):
				std_out = std_out.decode().rstrip()
			return_code = capture.returncode
			print(f"Return code: {return_code}")
			print(f"std_out: {std_out}")
			print(f"std_err: {std_err}")
			print()

			std_out += "\n"
			if return_code != 0:
				std_out = f"The command '{shell_command.decode()}' exited with a return_code of '{return_code}' and an exit message of '{std_err}'\n"
			self.wfile.write(std_out.encode("utf-8"))

class NServer(socketserver.ThreadingTCPServer):
	daemon_threads = True
	pass

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-p', "--port", help="The port to open the server on.", required=True)
	parser.add_argument('-a', "--any_user", help="Allows the server to start without root privileges.", action="store_true")
	args = parser.parse_args()

	try:
		port = int(args.port)
	except Exception:
		print(f"Invalid port number: `{args.port}`")
		sys.exit(1)

	if not args.any_user:
		username = get_username()
		if username != "root":
			print(f"ERROR: Script started as `{username}` instead of `root`!")
			sys.exit(1)

	try:
		print(f"Attempting to open a shell server on port {port}...")
		wz = NServer(('', port), Pipe)
		print(f"Successfully opened a shell server on port {port}.")
		wz.serve_forever()
	except Exception as err:
		print(f"Failed to start a shell server! Reason: `{err}`")
		sys.exit(1)
