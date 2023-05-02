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
	def __init__(self, ip_address, credentials):
		self.ip_address = ip_address
		self.got_root = False
		self.credentials = credentials

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

