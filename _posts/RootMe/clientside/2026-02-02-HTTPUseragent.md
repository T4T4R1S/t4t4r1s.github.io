---
layout: post
title: RootMe - Backup File
subtitle: Discovering Exposed Backup Files
description: RootMe challenge walkthrough - Backup file
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: Root Me
tags: [RootMe, CTF, Web, BackupFiles, DirectoryEnumeration, SourceCodeLeak]
author: mustafa_altayeb
date: 2026-02-02 00:09:00 +0000
paginate: true
---

# RootMe – Backup file

**Mission**  
Find the username and password to login.

![](/assets/Rootmeimages/m1.png)

**Analysis**  
- The challenge presents a standard login form.  
- No obvious vulnerabilities in the form itself (no SQLi visible, etc.).  
- Common web misconfiguration: developers leave backup files (e.g., `~`, `.bak`, `.old`, `.swp`) on the server, which can expose source code or hardcoded credentials.

**Solution steps**

1. Use a directory/file fuzzer like **dirsearch** to scan for hidden files:  
   ```
   dirsearch -u http://challenge01.root-me.org/web-serveur/ch11/
   ```
   → Key finding: `200` response for `/web-serveur/ch11/index.php~` (843 bytes).

2. Access the backup file directly in your browser:  
   `http://challenge01.root-me.org/web-serveur/ch11/index.php~`

3. Download or view the file → it reveals the source code of `index.php`, including hardcoded username and password.

   ![](/assets/Rootmeimages/m2.png)

4. Use the found credentials to login → challenge solved (password/flag obtained).

**Key takeaway**  
Backup files are a frequent source of information leaks in web applications. Always enumerate common extensions like `~`, `.bak`, `.old`, `.php.bak`, `.php~`, `.swp`, etc. Tools like dirsearch, gobuster, or ffuf are essential for discovering them quickly.

Finished. Happy Hacking! 🔓

Follow me:  
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)  
- [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>
