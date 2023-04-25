# SDSU Cyber Security Red Team - CS574

## Purpose
As leader of the SDSU CS574 Cyber Security Red Team I have made a bunch of custom tools for attacking students' systems. I am publishing this publicly so that students who have completed the course are able to learn from the tools that I created.

I originally took this course in 2019 and was assigned to Red Team because of some of the real-world applications I demonstrated to the professor, Peter Bartoli. Ever since graduating I have been great friends with Peter and I continue to lead the Red Team every semester.

---

## How to use it
This repo is meant to be used from a Python shell (REPL). This allows the user to interact with the machines in real time which fits better in a red team setting.

1. Open up a terminal and go to this directory
    ```
    $ cd ~/SDSU_Cyber_Security_Red_Team
    ```
2. Launch a Python shell:
    ```
    $ python3
    ```
3. Load the main file:
    ``` python3
    >>> exec(open("main.py").read())
    ```
4. Load the config file:
    ``` python3
    config = read_config_file()
    ips = config["ips"]
    credentials = config["credentials"]
    ```

---

## Vulnerabilities
This section highlights the vulnerabilities that I have found on the defense lab system. These CVEs may or may not be patched by updating the system, I will have to try 

### CVE-2021-3156 (Baron Samedit)
**Type:** local
**Fixed by updating:** ?

### CVE 2021-4034 (PwnKit)
**Type:** local
**Fixed by updating:** ?
