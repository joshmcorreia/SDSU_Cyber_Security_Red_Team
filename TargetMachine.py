import socket
from BetterLogger import logger
from ExploitDefaultCredentials import ExploitDefaultCredentials
from ChallengeOnePython import ChallengeOnePython
from BackdoorTwoShellPHP import BackdoorTwoShellPHP
from ChallengeTwoUpload import ChallengeTwoUpload
from ChallengeFourLFI import ChallengeFourLFI
from ChallengeFiveSQLi import ChallengeFiveSQLi

COLOR_OKGREEN = '\033[92m'
COLOR_OKBLUE = '\033[94m'
COLOR_ORANGE = '\033[93m'
COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'

class TargetMachine:
	"""
	TargetMachine represents a single student's machine

	Each machine has multiple exploits that can be run on it
	"""
	def __init__(self, ip_address, credentials, parsed_config):
		self.ip_address = ip_address
		self.got_root = False
		self.credentials = credentials
		self.parsed_config = parsed_config

		self.exploits = []
		self.exploits.append(ExploitDefaultCredentials(self.ip_address))
		self.exploits.append(BackdoorTwoShellPHP(self.ip_address))
		self.exploits.append(ChallengeOnePython(self.ip_address))
		self.exploits.append(ChallengeTwoUpload(self.ip_address))
		self.exploits.append(ChallengeFourLFI(self.ip_address))
		self.exploits.append(ChallengeFiveSQLi(self.ip_address))

	def __repr__(self) -> str:
		"""
		Represent the Object as a string
		"""
		return f"{type(self).__name__}({self.ip_address})"

	def test_all_vulnerabilities(self):
		"""
		Tests if the machine is vulnerable

		Returns how many vulnerabilities the target machine has
		"""
		num_vulnerabilities = 0
		for exploit in self.exploits:
			exploit_is_vulnerable = exploit.test_if_vulnerable()
			if exploit_is_vulnerable:
				num_vulnerabilities += 1
		return num_vulnerabilities

	def check_if_root_netcat_server_is_running(self):
		"""
		Returns True if the netcat server is already running and False if not
		"""
		try:
			logger.info(f"{self.ip_address} - Checking if a root netcat server is already running on the target machine...")
			port = self.parsed_config["root_netcat_server_port"]
			logger.debug(f"{self.ip_address} - Connecting to port {port}...")
			socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket_connection.settimeout(3)
			socket_connection.connect((self.ip_address, port))
			socket_connection.settimeout(None)
			logger.debug(f"{self.ip_address} - Successfully connected to port {port}.")
			logger.info(f"{COLOR_OKGREEN}{self.ip_address} - A root netcat server is running on the target machine!{COLOR_END}")
			return True
		except Exception:
			logger.info(f"{COLOR_FAIL}{self.ip_address} - A root netcat server is not currently running on the target machine.{COLOR_END}")
			return False
