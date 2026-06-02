---
layout: post
title: Infinity - SQL Injection - Opengate
date: 2026-05-20 00:07:00 +0000
categories: [Writeups, Infinity, "SQL Injection"]
tags:
  - Infinity
author: mustafa_altayeb
subtitle: Manipulating POST Parameters for High Score
description: A walkthrough of exploiting SQL Injection in a login form on Infinity platform. By injecting a boolean condition and switching comment syntax from -- to `#`, we bypassed authentication and gained access to the application.
image: https://infinitylearning-images.s3.eu-west-2.amazonaws.com/Learning-Path-Challenge-Images/Opengate.webp
tag:
  - Infinity
  - Web_Security
  - SQLI
  - infinity
  - CTF
  - Web
  - HTTP
  - POST
  - SQLi
paginate: true
---

# Infinity — SQL Injection: Opengate

## Overview

A walkthrough of exploiting SQL Injection in a login form on Infinity platform. 
By injecting a boolean condition and switching comment syntax from -- to #, 
we bypassed authentication and gained access to the application.

**Vulnerability:** Authentication Bypass via SQLi  

---


## Step 1: Identify the Input Field

Open the challenge and locate the Login form input field.

![alt text](/assets/infinity/SQLI/Opengate/image.png)

---

## Step 2: Test for SQL Injection

I try user name admin and it's taken and tried to inject `'` and i have an error :

![alt text](/assets/infinity/SQLI/Opengate/image-1.png)

first let's imagine sql query :
```sql
SELECT * FROM users WHERE username='User_input' AND password='User Input';
```

we can inject boolean condition `admin' or 1=1--` and try to login with it and i got a new error :

![alt text](/assets/infinity/SQLI/Opengate/image-2.png)

I tried to use `#` instead of `--` and it worked :

![alt text](/assets/infinity/SQLI/Opengate/image-3.png)

---

## Key Takeaways

- Comment syntax varies by database — `--` works on MSSQL and PostgreSQL, `#` works on MySQL. If one fails, try the other.
- Always test different comment styles before assuming the injection failed.
- Boolean-based login bypass is one of the simplest and most impactful SQLi attacks — one payload gives full access.

---

Happy Hacking!  

Follow me: [LinkedIn](https://www.linkedin.com/in/t4t4r1s/) · [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>


