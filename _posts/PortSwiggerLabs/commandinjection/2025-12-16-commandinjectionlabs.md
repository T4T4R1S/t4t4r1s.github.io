---
layout: post
title: PortSwigger
subtitle: OS Command injection
description: OS Command injection
image: /assets/image/Portswigger/download.png
optimized_image: /assets/image/Portswigger/download.png
category: Portswigger Labs
tags:
  - portswigger
  - server-side
  - OS command injection
author: mustafa_altayeb
date: 2025-12-16 00:00:00 +0000
paginate: true
---

## LAB 1

**Analysis**
 1- Vulnerability in the product stock checker

 2- app -> execute shell and use store IDS parameter

 3- To solve the lab we should execute `whoami` 

**steps to solve**

 ![alt text](/assets/image/Portswigger/commandi/image.png)

Here if i click in check store it's return 55 units and when check network tab i find request send to back end to check stock 

Check the Request Using Burp suit : 

![alt text](/assets/image/Portswigger/commandi/image-1.png)

Now we have 2 parameters like analysis description say 
`productId` `storeId`

Try to add ;whoami to check command injection and success 

![alt text](/assets/image/Portswigger/commandi/image-2.png)

The name of current user in the system is `peter-kEkc4I`


