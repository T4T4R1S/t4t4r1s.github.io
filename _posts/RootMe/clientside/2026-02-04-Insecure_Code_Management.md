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
1) find password to login as an admin.
**Analysis**  
1) after start challenge in find a login form to DataBase system .
2) noting interesting  
**Solution steps**

1) using dirsearch i fuzz dirctory and find .git appear more than 6. 
2) Download .git folder with wget -r .
3) open the folder with `gitcoal` 
4) open `config.php` and i find user name and password .

Finished. Happy Hacking! 

Follow me:  
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)  
- [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>
