---
layout: post
title: RootMe - HTTP Headers
subtitle: Custom Header Manipulation
description: RootMe challenge walkthrough - HTTP Headers
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: [Root Me, web server]
tags: [RootMe, CTF, Web, HTTP, Headers]
author: mustafa_altayeb
date: 2026-02-02 00:01:00 +0000
paginate: true
---

# RootMe – HTTP - Headers

**Challenge hint**  
> Content is not the only part of an HTTP response!

![](/assets/Rootmeimages/image7.png)

**Analysis**  
The message clearly tells us that we should look beyond the response body — most likely in the **headers**.

**Solution steps**

1. Intercept the HTTP request using Burp Suite and send it to **Repeater**.  
2. Look at the response headers — you will see this custom header:  

   ```
   Header-RootMe-Admin: none
   ```

   (It does **not** appear in the original request.)

![](/assets/Rootmeimages/image8.png)

3. Add the same header to your **request** with the value `true`:  

   ```
   Header-RootMe-Admin: true
   ```

4. Forward / send the modified request → the password will be returned in the response.

Finished. Happy Hacking! 

Follow me:  
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)  
- [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>
```
