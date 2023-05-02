# SDSU Cyber Security Red Team - CS574

## Purpose
As leader of the SDSU CS574 Cyber Security Red Team I have made a bunch of custom tools for attacking students' systems. I am publishing this publicly so that students who have completed the course are able to learn from the tools that I created.

I originally took this course in 2019 and was assigned to Red Team because of some of the real-world applications I demonstrated to the professor, Peter Bartoli. Ever since graduating I have been great friends with Peter and I continue to lead the Red Team every semester.

---

## Using HiveMind:

### Starting a Python shell:
```
cd ~/SDSU_Cyber_Security_Red_Team
python3
```

### Instantiating Hivemind (in the Python shell):
```
from HiveMind import HiveMind
hivemind = HiveMind()
hivemind.add_new_target_machines_from_config()
hivemind.add_new_target_machines_from_ip_list()

```

### Update the list of target machines:
```
hivemind.add_new_target_machines_from_ip_list()
```

### Testing all machines for vulnerabilities:
```
hivemind.test_all_machines_for_vulnerabilities()
```

### Starting a root netcat server on all target machines:
```
hivemind.start_root_netcat_server_on_all_machines()
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
