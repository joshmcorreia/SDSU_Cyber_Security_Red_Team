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

	def __check_login(self, username, password):
		"""
		Returns True if we successfully got root, and returns False otherwise
		"""
		try:
			logger.info(f"Connecting to {username}@{self.ip_address}...")
			ssh_client = paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh_client.connect(self.ip_address, username=username, password=password, timeout=5)
			logger.info(f"{COLOR_OKGREEN}Successfully connected to {username}@{self.ip_address}{COLOR_END}")
			return True
		except paramiko.AuthenticationException as err:
			logger.info(f"{COLOR_FAIL}Failed to connect to {username}@{self.ip_address}. The user most likely changed their password!{COLOR_END}")
			return False
		except Exception as err:
			logger.info(f"{COLOR_FAIL}Failed to connect to {username}@{self.ip_address}{COLOR_END}")
			return False

	def check_all_logins(self, return_when_root=True):
		"""
		Tries to connect using all default credentials

		return_when_root: If set to False, all logins will be checked regardless of whether or not we successfully got root
		"""
		for credential in self.credentials:
			try:
				logged_in = self.__check_login(username=credential["username"], password=credential["password"])
				is_sudo_user = credential['sudo_user']
				if logged_in and (is_sudo_user == True):
					logger.info(f"{COLOR_OKBLUE}Successfully got root on {self.ip_address}{COLOR_END}")
					if return_when_root:
						break
			except Exception as err:
				pass
