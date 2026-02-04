---
layout: post
title: RootMe - Hidden Include & Backup
subtitle: Discovering Credentials via HTML Comments and Backup Files
description: RootMe challenge walkthrough - Hidden Include & Backup
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: [Root Me, web server]
tags: [RootMe, CTF, Web, SourceCodeLeak, HTMLComments, BackupFiles, DirectoryEnumeration]
author: mustafa_altayeb
date: 2026-02-04 00:10:00 +0000
paginate: true
---

# RootMe – Hidden Include & Backup

**Mission**  
Find the password to solve the challenge.

**Analysis**  
- The challenge loads an empty page with no visible content.  
- Inspecting the page source reveals an HTML comment hinting at an included file:  
  ```
  <!-- include("admin/pass.html") -->
  ```
  This suggests the page might dynamically include `admin/pass.html`, but it's not loading properly (or is empty on purpose).

**Solution steps**

1. Directly access the hinted path:  
   `http://challenge-url/admin/pass.html`  
   → Nothing interesting appears (likely empty or restricted).

2. Navigate to the parent directory:  
   `http://challenge-url/admin/`  
   → This reveals a backup file (common naming like `admin.php~`, `admin.bak`, `.admin.swp`, etc., or perhaps `admin.txt`).

3. Open the backup file → it contains `admin.txt` (or similar) with the hardcoded password: **LINUX**.

Finished. Happy Hacking! 

Follow me:  
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)  
- [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>
