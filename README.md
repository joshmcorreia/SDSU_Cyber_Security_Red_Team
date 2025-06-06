# SDSU Cyber Security Red Team - CS574

## Purpose
As leader of the SDSU CS574 Cyber Security Red Team I have made a bunch of custom tools for attacking students' systems. I am publishing this publicly so that students who have completed the course are able to learn from the tools that I created.

I originally took this course in 2019 and was assigned to Red Team because of some of the real-world applications I demonstrated to the professor, Peter Bartoli. Ever since graduating I have been great friends with Peter and I continue to lead the Red Team every semester.

---

## Prerequisites:
Before running these scripts, install [uv](https://github.com/astral-sh/uv):
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Using HiveMind:

### Colored log explanation:
- BLUE - indicates that a root shell was successfully started
- GREEN - indicates something was successful
- YELLOW - indicates that the exploit/vulnerability has been patched by the student
- PINK - indicates that the exploit/vulnerability has been incorrectly patched, so the intended functionality is no longer present
- RED - indicates that something went wrong, such as a connection timed out or the target machine is offline

### Starting a Python shell:
```
$ cd ~/SDSU_Cyber_Security_Red_Team
$ uv run python3
```

### Instantiating Hivemind (in the Python shell):
```
from HiveMind import HiveMind
hivemind = HiveMind()
hivemind.add_ips_from_roster_to_database()
hivemind.convert_database_ips_to_target_machines()
```

### Ping all target machines:
```
hivemind.ping_all_target_machines()
```

### Test all target machines for vulnerabilities:
```
hivemind.test_all_machines_for_vulnerabilities()
```

### Run Hellevator on all target machines:
```
hivemind.run_hellevator_on_all_target_machines()
```

### Check if Hellevator has run on all target machines:
```
hivemind.check_for_hellevator_on_all_target_machines()
```

### Install the salt minion on all target machines:
```
hivemind.install_salt_minion_on_all_target_machines()
```

## Hellevator

`hellevator.sh` elevates privileges using whatever method necessary and then creates a user with SSH keys. This script completely bypasses the need to know the user's password because in most cases the students have already changed the passwords. It is meant to be downloaded from the internet and then run as a local user. I created this script because it's easiest to have every exploit call the same code.

The name is a reference to a Hell Elevator in Terraria.

---

## System Vulnerabilities
This section highlights the vulnerabilities that I have found on the defense lab system. These CVEs may or may not be patched by updating the system, I will have to test them out in the future.

### CVE-2021-3156 (Baron Samedit)
**Type:** local

**Fixed by updating:** ?

### CVE 2021-4034 (PwnKit)
**Type:** local

**Fixed by updating:** ?
