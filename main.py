import paramiko
import yaml
import os
import sys
sys.path.append("..")
from BetterLogger import BetterLogger

filename = os.path.basename("main.py")
logger = BetterLogger(logger_name=filename).logger

COLOR_OKGREEN = '\033[92m'
COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'

def read_config_file():
	logger.debug("Reading config file...")
	with open("config.yaml", 'r') as file_in:
		parsed_config = yaml.safe_load(file_in)
	logger.debug("Successfully read config file")
	return parsed_config

def check_login(ip_address, username, password):
	"""
	Returns True if we successfully got root, and returns False otherwise
	"""
	try:
		logger.info(f"Connecting to {username}@{ip_address}...")
		ssh_client = paramiko.SSHClient()
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_client.connect(ip_address, username=username, password=password, timeout=5)
		logger.info(f"{COLOR_OKGREEN}Successfully connected to {username}@{ip_address}{COLOR_END}")
		return True
	except paramiko.AuthenticationException as err:
		logger.info(f"{COLOR_FAIL}Failed to connect to {username}@{ip_address}. The user most likely changed their password!{COLOR_END}")
		return False
	except Exception as err:
		logger.info(f"{COLOR_FAIL}Failed to connect to {username}@{ip_address}{COLOR_END}")
		return False

def check_all_logins(config, return_when_root=True):
	"""
	Tries to connect to all IPs with default credentials

	return_when_root: If set to False, all logins will be checked regardless of whether or not we successfully got root
	"""
	ips = config["ips"]
	credentials = config["credentials"]
	for ip in ips:
		for credential in credentials:
			try:
				got_root = check_login(ip_address=ip, username=credential["username"], password=credential["password"])
				if return_when_root:
					if got_root:
						break
			except Exception as err:
				pass
