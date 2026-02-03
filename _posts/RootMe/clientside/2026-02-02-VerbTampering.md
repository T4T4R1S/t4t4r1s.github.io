---
layout: post
title: RootMe - HTTP Verb Tampering
subtitle: Bypassing Restrictions via HTTP Methods
description: RootMe challenge walkthrough - HTTP - Verb Tampering
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: [Root Me, web server]
tags: [RootMe, CTF, Web, HTTP, VerbTampering, Methods]
author: mustafa_altayeb
date: 2026-02-02 00:05:00 +0000
paginate: true
---

# RootMe – HTTP - Verb Tampering

**Mission**  
Bypass the security establishment.

![](/assets/Rootmeimages/i4.png)

**Analysis**  
- A login form pops up as a window when opening the challenge.  
- Closing the window or attempting normal access results in an `Authorization Required` message.  
- The server likely restricts access based on HTTP method (e.g., only allows certain verbs like GET).

**Solution steps**

1. Start Burp Suite and intercept the initial request (likely a GET).  

2. Change the request method from GET to POST → server responds with `401 Unauthorized`.  

   ![](/assets/Rootmeimages/i5.png)

3. Try other HTTP methods: PATCH, HEAD, PUT, DELETE, etc.  
4. Using **PATCH** method succeeds → password is returned in the response.  

   ![](/assets/Rootmeimages/i5.png)

**Key takeaway**  
Many web applications implement access controls only for common methods (GET/POST) and fail to restrict others like PATCH, PUT, or DELETE. This is a classic **HTTP verb tampering** vulnerability — always test alternative HTTP methods when facing authorization blocks.

Finished. Happy Hacking! 

Follow me:  
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)  
- [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>