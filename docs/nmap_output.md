# NMap Output

```
$ nmap -A -p- 192.168.232.131
Starting Nmap 7.93 ( https://nmap.org ) at 2023-04-26 22:24 PDT
Stats: 0:01:46 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
NSE Timing: About 99.92% done; ETC: 22:25 (0:00:00 remaining)
Nmap scan report for 192.168.232.131
Host is up (0.00079s latency).
Not shown: 65526 closed tcp ports (conn-refused)
PORT      STATE SERVICE       VERSION
22/tcp    open  ssh           OpenSSH 8.2p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 dc4710fd3c0a43d2de0bc11ad6b39aea (RSA)
|   256 2e0b48f76b66b1378d3d147b279fe1ea (ECDSA)
|_  256 3bde5381037cf5d064b49e316affab66 (ED25519)
80/tcp    open  http          Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
2222/tcp  open  EtherNetIP-1?
| fingerprint-strings:
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, JavaRMI, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NCP, NULL, NotesRPC, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, WMSRequest, X11Probe, afp, giop, ms-sql-s, oracle-tns:
|_    Enter a Command:
3333/tcp  open  dec-notes?
| fingerprint-strings:
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, JavaRMI, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NCP, NULL, NotesRPC, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, WMSRequest, X11Probe, afp, giop, kumo-server, ms-sql-s, oracle-tns:
|_    Enter a username:
33060/tcp open  mysqlx?
| fingerprint-strings:
|   DNSStatusRequestTCP, LDAPSearchReq, NotesRPC, SSLSessionReq, TLSSessionReq, X11Probe, afp:
|     Invalid message"
|_    HY000
33120/tcp open  tcpwrapped
33121/tcp open  tcpwrapped
33122/tcp open  tcpwrapped
33123/tcp open  tcpwrapped
```
