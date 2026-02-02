---
layout: post
title: RootMe - HTTP Cookies
subtitle: Manipulating Cookies for Admin Access
description: RootMe challenge walkthrough - HTTP - Cookies
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: Root Me
tags: [RootMe, CTF, Web, HTTP, Cookies, Authentication]
author: mustafa_altayeb
date: 2026-02-02 00:04:00 +0000
paginate: true
---

# RootMe – HTTP - Cookies

**Mission**  
Get all emails from Bob.

![](/assets/Rootmeimages/i2.png)

**Analysis**  
- There's a basic script that collects emails from users.  
- Trying to access all emails fails because we are not an admin (access restricted by role).

**Solution steps**

1. Open Developer Tools → go to the **Application** tab → **Cookies** section.  
2. Look for the cookie that likely controls user role (value is set to `visitor`).  

   ![](/assets/Rootmeimages/i3.png)

3. Edit the cookie value and change it from `visitor` to `admin`.  
4. Refresh/reload the page → the restricted content (all emails / password) now appears.

Finished. Happy Hacking! 🔓

Follow me:  
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)  
- [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>