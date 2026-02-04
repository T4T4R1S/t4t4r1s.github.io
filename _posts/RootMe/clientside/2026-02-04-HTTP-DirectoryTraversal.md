---
layout: post
title: RootMe - Directory Traversal
subtitle: Parameter Tampering to Access Hidden Files
description: RootMe challenge walkthrough - Directory Traversal
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: [Root Me, web server]
tags: [RootMe, CTF, Web, DirectoryTraversal, PathManipulation, ParameterTampering]
author: mustafa_altayeb
date: 2026-02-04 00:11:00 +0000
paginate: true
---

# RootMe – Directory Traversal

**Mission**  
Find the password to solve the challenge.

![](/assets/Rootmeimages/m5.png)

**Analysis**  
- The challenge presents a photo gallery with tabs that change the URL parameter:  
  `?galerie=devices` (or other values).  
- This suggests the `galerie` parameter controls which directory/folder of images is loaded.  
- Likely vulnerable to path manipulation or traversal to access unintended directories/files.

**Solution steps**

1. Manually set the `galerie` parameter to an empty value:  
   `?galerie=`  
   → A new "item" appears in the page (a secret directory name: `86hwnX2r`).  

   ![](/assets/Rootmeimages/m6.png)

2. Use this discovered value as the parameter:  
   `?galerie=86hwnX2r`  
   → The page loads content from that hidden directory.  

   ![](/assets/Rootmeimages/m7.png)

3. Inspect the page source (Ctrl+U) → find a link to a file inside the directory:  
   `http://challenge01.root-me.org/web-serveur/ch15/galerie/86hwnX2r/password.txt`  

4. Access the file directly in your browser → it contains the password/flag for the challenge.

**Key takeaway**  
Web applications that use user-controlled parameters to include files or directories (e.g., `?dir=xxx`) are often vulnerable to directory traversal or unauthorized access. Setting parameters to empty, random, or predictable values can reveal hidden paths. Always inspect source code for leaked file references, and test parameters for path manipulation (e.g., `../`, absolute paths, or empty values).

Finished. Happy Hacking! 

Follow me:  
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)  
- [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>
