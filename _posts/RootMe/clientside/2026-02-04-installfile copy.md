---
layout: post
title: RootMe - Install File
subtitle: Discovering Exposed Installation Scripts
description: RootMe challenge walkthrough - Install File
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: [Root Me, web server]
tags: [RootMe, CTF, Web, InstallFile, DirectoryEnumeration, Misconfiguration]
author: mustafa_altayeb
date: 2026-02-04 00:09:00 +0000
paginate: true
---

# RootMe – Install File

**Mission**  
Find the password to solve the challenge.

**Analysis**  
- The challenge starts with an empty page (no visible content).  
- Inspecting the page source reveals an HTML comment:  
  ```
  <!-- /web-serveur/ch6/phpbb -->
  ```
  This hints at a hidden directory (likely a phpBB forum installation path).

**Solution steps**

1. Navigate to the hinted path:  
   `http://challenge01.root-me.org/web-serveur/ch6/phpbb/`  
   → Another empty page appears.

2. Run directory enumeration with **dirsearch**:  
   ```
   dirsearch -u http://challenge01.root-me.org/web-serveur/ch6/phpbb/
   ```
   → Key finding: `200` response for `/web-serveur/ch6/phpbb/install/` (12KB).

   ![](/assets/Rootmeimages/m3.png)

3. Access the installation directory:  
   `http://challenge01.root-me.org/web-serveur/ch6/phpbb/install/`  
   → Lists files, including `install.php`.

4. Open `install.php` directly in your browser:  
   → The script is still accessible (common post-installation misconfiguration).  
   → It displays the hardcoded password or flag for the challenge.

   ![](/assets/Rootmeimages/m4.png)


Finished. Happy Hacking! 

Follow me:  
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)  
- [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>
