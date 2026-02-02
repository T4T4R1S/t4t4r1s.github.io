---
layout: post
title: HTTP - User-agent
subtitle: HTTP - User-agent
description: HTTP - User-agent
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
optimized_image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: Root Me
tags:
  - RootME
  - HTML - web TECH
  - Find Password
author: mustafa_altayeb
date: 2026-02-02 00:00:00 +0000
paginate: true
---

# HTTP - User-agent - RootMe
![](/assets/Rootmeimages/image4.png)

**Analysis**

1. When opening the challenge it says we are not admin because we don't use the admin browser.

![](/assets/Rootmeimages/image5.png)

2. So we need to know the user agent that admin uses to solve the challenge.

**Solution steps**

1. I intercepted the request on Burp and deleted user agent and it still did not work.

2. After that I wrote user-agent: admin and guess what, it worked successfully.

![](/assets/Rootmeimages/image6.png)


**Finished.. Happy hacking!**


<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>

Follow me:
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)
- [X](https://x.com/T4T4R1S)



---