---
layout: post
title: RootMe - Insecure Code Management
subtitle: Recovering Credentials from Git History
description: RootMe challenge walkthrough - Exposed .git
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: [Root Me, web server]
tags: [RootMe, CTF, Web, GitExposure, SourceCodeLeak, DirectoryEnumeration, CredentialRecovery]
author: mustafa_altayeb
date: 2026-02-04 00:12:00 +0000
paginate: true
---

# RootMe – Insecure Code Management

**Mission**  
Find the password to login as admin.

![](/assets/Rootmeimages/m8.png)

**Analysis**  
- The challenge presents a login form for a "Database system."  
- No obvious vulnerabilities in the form (no SQLi, weak creds guessing, etc.).  
- Nothing interesting on the surface → time for reconnaissance and directory fuzzing.

**Solution steps**

1. Run **dirsearch** to enumerate directories and files:  
   ```
   dirsearch -u http://challenge01.root-me.org/web-serveur/ch61/
   ```
   → Multiple `200` responses for `.git/` paths (e.g., `.git/HEAD`, `.git/config`, `.git/index`, etc.) → the entire `.git` directory is exposed!

2. Download the full `.git` repository recursively using **wget**:  
   ```
   wget -r http://challenge01.root-me.org/web-serveur/ch61/.git
   ```

3. Open the downloaded repository with a Git GUI tool like **git-cola** (`apt install git-cola` or use SourceTree, GitKraken):  
   - Browse commit history.  
   - Find a commit that modified `config.php`.  
   - View the diff or revert/undo the commit to see the original code.

4. In the history, discover the diff in `config.php`:  

   ```php
   <?php
       $username = "admin";
   -   $password = "s3cureP@ssw0rd";
   +   $password = "0c25a741349bfdcc1e579c8cd4a931fca66bdb49b9f042c4d92ae1bfa3176d8c";
   diff --git a/index.html b/index.html
   new file mode 100644
   ```

   → The original admin password is revealed: `s3cureP@ssw0rd`.

5. Use the recovered credentials to login → challenge solved.

**Key takeaway**  
Exposed `.git` directories are a critical misconfiguration that allows attackers to download the entire source code repository, including commit history. This often leaks sensitive data like hardcoded credentials, API keys, or old passwords. Never leave `.git` accessible on production servers — use `.gitignore`, proper web server config (deny `.git`), or remove it entirely after deployment. Tools like dirsearch, gobuster, or GitTools (git-dumper) are great for detecting and exploiting this.

Finished. Happy Hacking! 

Follow me:  
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)  
- [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>
