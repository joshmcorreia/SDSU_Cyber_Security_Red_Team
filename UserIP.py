from BetterLogger import logger
from ExploitDefaultCredentials import ExploitDefaultCredentials
from ChallengeOnePython import ChallengeOnePython
from ChallengeTwoShellPHP import ChallengeTwoShellPHP

COLOR_OKGREEN = '\033[92m'
COLOR_OKBLUE = '\033[94m'
COLOR_ORANGE = '\033[93m'
COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'

class UserIP:
	"""
	UserIP represents a single student's machine

	Each machine has multiple exploits that can be run on it
	"""
	def __init__(self, ip_address, credentials, public_ssh_key_to_inject):
		self.ip_address = ip_address
		self.got_root = False
		self.credentials = credentials
		self.public_ssh_key_to_inject = public_ssh_key_to_inject

		self.exploits = []
		self.exploits.append(ExploitDefaultCredentials(self.ip_address))
		self.exploits.append(ChallengeOnePython(self.ip_address))
		self.exploits.append(ChallengeTwoShellPHP(self.ip_address))

	def __repr__(self) -> str:
		"""
		Represent the Object as a string
		"""
		return f"{type(self).__name__}({self.ip_address})"
