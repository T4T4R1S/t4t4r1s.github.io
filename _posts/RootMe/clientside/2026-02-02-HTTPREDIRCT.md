---
layout: post
title: RootMe - HTTP - Open Redirect
subtitle: Exploiting Open Redirect via MD5 Hash
description: RootMe challenge walkthrough - HTTP - Open Redirect
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: [Root Me, web server]
tags: [RootMe, CTF, Web, HTTP, OpenRedirect, Hashing]
author: mustafa_altayeb
date: 2026-02-02 00:06:00 +0000
paginate: true
---

# RootMe – HTTP - Open Redirect

**Mission**  
Find a way to make a redirection to a domain other than those shown on the web page.

![](/assets/Rootmeimages/i7.png)

**Analysis**  
- The page displays 3 internal links that redirect safely to allowed domains.  
- The redirect is controlled by a parameter (likely `?url=...` or similar) that uses an MD5 hash of the target URL to prevent arbitrary redirects.  
- To exploit the open redirect, compute the MD5 hash of an external URL (e.g., https://google.com) and use it in the request.

**Solution steps**

1. Intercept the request in Burp Suite when clicking one of the legitimate links → observe the redirect parameter contains an MD5 hash.  
2. The hash is the MD5 of the target URL.  
3. Compute the MD5 hash of your desired external URL (e.g., `https://google.com`):  

   ![](/assets/Rootmeimages/i8.png)

   (Example: MD5("https://google.com") = some_hash_value)

4. Replace the original hash in the request parameter with your computed MD5 hash.  
5. Send the modified request → the page redirects to the external site, and the challenge password is revealed.  

   ![](/assets/Rootmeimages/i9.png)



Finished. Happy Hacking! 

Follow me:  
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)  
- [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>