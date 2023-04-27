# nmapAutomator Scan Results

```
$./nmapAutomator.sh -H 192.168.199.129 -t Vulns

Running a Vulns scan on 192.168.199.129

Host is likely running Linux


---------------------Starting Port Scan-----------------------



PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http



---------------------Starting Vulns Scan-----------------------

Running CVE scan on common ports



PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
| vulners: 
|   cpe:/a:apache:http_server:2.4.41: 
|     	PACKETSTORM:171631	7.5	https://vulners.com/packetstorm/PACKETSTORM:171631	*EXPLOIT*
|     	CVE-2022-31813	7.5	https://vulners.com/cve/CVE-2022-31813
|     	CVE-2022-23943	7.5	https://vulners.com/cve/CVE-2022-23943
|     	CVE-2022-22720	7.5	https://vulners.com/cve/CVE-2022-22720
|     	CVE-2021-44790	7.5	https://vulners.com/cve/CVE-2021-44790
|     	CVE-2021-39275	7.5	https://vulners.com/cve/CVE-2021-39275
|     	CVE-2021-26691	7.5	https://vulners.com/cve/CVE-2021-26691
|     	CVE-2020-11984	7.5	https://vulners.com/cve/CVE-2020-11984
|     	CNVD-2022-73123	7.5	https://vulners.com/cnvd/CNVD-2022-73123
|     	CNVD-2022-03225	7.5	https://vulners.com/cnvd/CNVD-2022-03225
|     	CNVD-2021-102386	7.5	https://vulners.com/cnvd/CNVD-2021-102386
|     	1337DAY-ID-38427	7.5	https://vulners.com/zdt/1337DAY-ID-38427	*EXPLOIT*
|_    	1337DAY-ID-34882	7.5	https://vulners.com/zdt/1337DAY-ID-34882	*EXPLOIT*
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel



Running Vuln scan on common ports
This may take a while, depending on the number of detected services..



PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
| vulners: 
|   cpe:/a:openbsd:openssh:8.2p1: 
|     	CVE-2020-15778	6.8	https://vulners.com/cve/CVE-2020-15778
|     	C94132FD-1FA5-5342-B6EE-0DAF45EEFFE3	6.8	https://vulners.com/githubexploit/C94132FD-1FA5-5342-B6EE-0DAF45EEFFE3	*EXPLOIT*
|     	10213DBE-F683-58BB-B6D3-353173626207	6.8	https://vulners.com/githubexploit/10213DBE-F683-58BB-B6D3-353173626207	*EXPLOIT*
|     	CVE-2020-12062	5.0	https://vulners.com/cve/CVE-2020-12062
|     	CVE-2021-28041	4.6	https://vulners.com/cve/CVE-2021-28041
|     	CVE-2021-41617	4.4	https://vulners.com/cve/CVE-2021-41617
|     	CVE-2020-14145	4.3	https://vulners.com/cve/CVE-2020-14145
|     	CVE-2016-20012	4.3	https://vulners.com/cve/CVE-2016-20012
|_    	CVE-2021-36368	2.6	https://vulners.com/cve/CVE-2021-36368
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-csrf: 
| Spidering limited to: maxdepth=3; maxpagecount=20; withinhost=192.168.199.129
|   Found the following possible CSRF vulnerabilities: 
|     
|     Path: http://192.168.199.129:80/
|     Form id: 
|     Form action: /index.php
|     
|     Path: http://192.168.199.129:80/index.php
|     Form id: 
|_    Form action: /index.php
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-enum: 
|   /robots.txt: Robots file
|   /info.php: Possible information file
|_  /images/: Potentially interesting directory w/ listing on 'apache/2.4.41 (ubuntu)'
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
| http-phpself-xss: 
|   VULNERABLE:
|   Unsafe use of $_SERVER["PHP_SELF"] in PHP files
|     State: VULNERABLE (Exploitable)
|       PHP files are not handling safely the variable $_SERVER["PHP_SELF"] causing Reflected Cross Site Scripting vulnerabilities.
|              
|     Extra information:
|       
|   Vulnerable files with proof of concept:
|     http://192.168.199.129/index.php/%27%22/%3E%3Cscript%3Ealert(1)%3C/script%3E
|   Spidering limited to: maxdepth=3; maxpagecount=20; withinhost=192.168.199.129
|     References:
|       https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)
|_      http://php.net/manual/en/reserved.variables.server.php
|_http-dombased-xss: Couldn't find any DOM based XSS.
|_http-vuln-cve2017-1001000: ERROR: Script execution failed (use -d to debug)
| http-internal-ip-disclosure: 
|_  Internal IP Leaked: 127.0.1.1
| vulners: 
|   cpe:/a:apache:http_server:2.4.41: 
|     	PACKETSTORM:171631	7.5	https://vulners.com/packetstorm/PACKETSTORM:171631	*EXPLOIT*
|     	CVE-2022-31813	7.5	https://vulners.com/cve/CVE-2022-31813
|     	CVE-2022-23943	7.5	https://vulners.com/cve/CVE-2022-23943
|     	CVE-2022-22720	7.5	https://vulners.com/cve/CVE-2022-22720
|     	CVE-2021-44790	7.5	https://vulners.com/cve/CVE-2021-44790
|     	CVE-2021-39275	7.5	https://vulners.com/cve/CVE-2021-39275
|     	CVE-2021-26691	7.5	https://vulners.com/cve/CVE-2021-26691
|     	CVE-2020-11984	7.5	https://vulners.com/cve/CVE-2020-11984
|     	CNVD-2022-73123	7.5	https://vulners.com/cnvd/CNVD-2022-73123
|     	CNVD-2022-03225	7.5	https://vulners.com/cnvd/CNVD-2022-03225
|     	CNVD-2021-102386	7.5	https://vulners.com/cnvd/CNVD-2021-102386
|     	1337DAY-ID-38427	7.5	https://vulners.com/zdt/1337DAY-ID-38427	*EXPLOIT*
|     	1337DAY-ID-34882	7.5	https://vulners.com/zdt/1337DAY-ID-34882	*EXPLOIT*
|     	FDF3DFA1-ED74-5EE2-BF5C-BA752CA34AE8	6.8	https://vulners.com/githubexploit/FDF3DFA1-ED74-5EE2-BF5C-BA752CA34AE8	*EXPLOIT*
|     	CVE-2021-40438	6.8	https://vulners.com/cve/CVE-2021-40438
|     	CVE-2020-35452	6.8	https://vulners.com/cve/CVE-2020-35452
|     	CNVD-2022-03224	6.8	https://vulners.com/cnvd/CNVD-2022-03224
|     	8AFB43C5-ABD4-52AD-BB19-24D7884FF2A2	6.8	https://vulners.com/githubexploit/8AFB43C5-ABD4-52AD-BB19-24D7884FF2A2	*EXPLOIT*
|     	4810E2D9-AC5F-5B08-BFB3-DDAFA2F63332	6.8	https://vulners.com/githubexploit/4810E2D9-AC5F-5B08-BFB3-DDAFA2F63332	*EXPLOIT*
|     	4373C92A-2755-5538-9C91-0469C995AA9B	6.8	https://vulners.com/githubexploit/4373C92A-2755-5538-9C91-0469C995AA9B	*EXPLOIT*
|     	0095E929-7573-5E4A-A7FA-F6598A35E8DE	6.8	https://vulners.com/githubexploit/0095E929-7573-5E4A-A7FA-F6598A35E8DE	*EXPLOIT*
|     	CVE-2022-28615	6.4	https://vulners.com/cve/CVE-2022-28615
|     	CVE-2021-44224	6.4	https://vulners.com/cve/CVE-2021-44224
|     	CVE-2022-22721	5.8	https://vulners.com/cve/CVE-2022-22721
|     	CVE-2020-1927	5.8	https://vulners.com/cve/CVE-2020-1927
|     	CVE-2022-30556	5.0	https://vulners.com/cve/CVE-2022-30556
|     	CVE-2022-29404	5.0	https://vulners.com/cve/CVE-2022-29404
|     	CVE-2022-28614	5.0	https://vulners.com/cve/CVE-2022-28614
|     	CVE-2022-26377	5.0	https://vulners.com/cve/CVE-2022-26377
|     	CVE-2022-22719	5.0	https://vulners.com/cve/CVE-2022-22719
|     	CVE-2021-36160	5.0	https://vulners.com/cve/CVE-2021-36160
|     	CVE-2021-34798	5.0	https://vulners.com/cve/CVE-2021-34798
|     	CVE-2021-33193	5.0	https://vulners.com/cve/CVE-2021-33193
|     	CVE-2021-30641	5.0	https://vulners.com/cve/CVE-2021-30641
|     	CVE-2021-26690	5.0	https://vulners.com/cve/CVE-2021-26690
|     	CVE-2020-9490	5.0	https://vulners.com/cve/CVE-2020-9490
|     	CVE-2020-1934	5.0	https://vulners.com/cve/CVE-2020-1934
|     	CVE-2020-13950	5.0	https://vulners.com/cve/CVE-2020-13950
|     	CVE-2019-17567	5.0	https://vulners.com/cve/CVE-2019-17567
|     	CNVD-2022-73122	5.0	https://vulners.com/cnvd/CNVD-2022-73122
|     	CNVD-2022-53584	5.0	https://vulners.com/cnvd/CNVD-2022-53584
|     	CNVD-2022-53582	5.0	https://vulners.com/cnvd/CNVD-2022-53582
|     	CNVD-2022-03223	5.0	https://vulners.com/cnvd/CNVD-2022-03223
|     	CVE-2020-11993	4.3	https://vulners.com/cve/CVE-2020-11993
|     	1337DAY-ID-35422	4.3	https://vulners.com/zdt/1337DAY-ID-35422	*EXPLOIT*
|     	CVE-2023-27522	0.0	https://vulners.com/cve/CVE-2023-27522
|     	CVE-2023-25690	0.0	https://vulners.com/cve/CVE-2023-25690
|     	CVE-2022-37436	0.0	https://vulners.com/cve/CVE-2022-37436
|     	CVE-2022-36760	0.0	https://vulners.com/cve/CVE-2022-36760
|_    	CVE-2006-20001	0.0	https://vulners.com/cve/CVE-2006-20001
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel




---------------------Finished all scans------------------------


Completed in 1 minute(s) and 13 second(s)

```
