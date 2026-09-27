---
layout: post
title: Down
date: 2026-09-23 00:00:00 +0000
categories: [Writeups, HackTheBox, HTB-Easy]
tags:
  - HTB
  - HackTheBox
  - Linux
  - WebEnumeration
  - PrivilegeEscalation
subtitle: HackTheBox Writeup - Down
description: Walkthrough of the Down machine – enumerating the web application to gain an initial foothold as www-data, discovering an encrypted-password file owned by the user aleks for lateral movement, and escalating to root.
image: https://cdn.services-k8s.prod.aws.htb.systems/content/machines/avatar/<REPLACE-WITH-DOWN-AVATAR-ID>.png
optimized_image: https://cdn.services-k8s.prod.aws.htb.systems/content/machines/avatar/<REPLACE-WITH-DOWN-AVATAR-ID>.png
paginate: true

---

# Recon 

Start with nmap scan to identify running services 

```bash

┌──🦊 T4T4R1S  IP ➜  10.211.55.3   ~/machines/down
└─👀 ➜ nmap -p- --min-rate 1000 -oA nmap_down 10.129.234.87
Starting Nmap 7.95 ( https://nmap.org ) at 2026-09-21 18:42 EEST
Host is up (0.19s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
Nmap done: 1 IP address (1 host up) scanned in 73.36 seconds

┌──🦊 T4T4R1S  IP ➜  10.211.55.3   ~/machines/down
└─👀 ➜ nmap -p22,80 -sCV -oN deep_down 10.129.234.87
Starting Nmap 7.95 ( https://nmap.org ) at 2026-09-21 18:43 EEST
Nmap scan report for 10.129.234.87
Host is up (0.16s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 f6:cc:21:7c:ca:da:ed:34:fd:04:ef:e6:f9:4c:dd:f8 (ECDSA)
|_  256 fa:06:1f:f4:bf:8c:e3:b0:c8:40:21:0d:57:06:dd:11 (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-server-header: Apache/2.4.52 (Ubuntu)
|_http-title: Is it down or just me?
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP
```

**Findings**

- **ssh (22)** : ssh running on port 22 version 8.9p1
- Http 80 : apache httpd version 2.4.52

## SSH enumurtion 

I searched for ssh version to see if it has vulnerabilities in this version with searchsploit and no vulnerabilities founded in this version : 

```bash
┌──🦊 T4T4R1S  IP ➜  10.211.55.3   ~/machines/down
└─👀 ➜ searchsploit  8.9p1
Exploits: No Results
Shellcodes: No Results
```

## Web enueration 

i started with discover web application on port 80 : 