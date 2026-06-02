---
layout: post
title: Infinity - SQL Injection - Login_Logic
date: 2026-05-20 00:04:00 +0000
categories: [Writeups, Infinity, "SQL Injection"]
tags:
  - Infinity
author: mustafa_altayeb
subtitle: Manipulating POST Parameters for High Score
description: A walkthrough of exploiting a Boolean-based SQL Injection vulnerability in a login form on Infinity platform. By injecting a true condition into the username field, we bypassed authentication without knowing any credentials.
image: https://infinitylearning-images.s3.eu-west-2.amazonaws.com/images/public/login-logic.webp
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

# Infinity — SQL Injection: Login_Logic

## Overview

A walkthrough of exploiting a Boolean-based SQL Injection vulnerability 
in a login form on Infinity platform. By injecting a true condition into 
the username field, we bypassed authentication without knowing any credentials.

**Vulnerability:** Boolean-based SQL Injection  

---

## Step 1: Identify the Input Field

Open the challenge and locate the Login form input field.

![alt text](/assets/infinity/SQLI/login_logic/image-9.png)


---

## Step 2: Test for SQL Injection

Inject a single quote `'` `"` and i got an error : 
![alt text](/assets/infinity/SQLI/login_logic/image.png)

first let's imagine sql query : 
```sql
SELECT * FROM users WHERE username='User_input' AND password='User Input';
```
if we put `'-- -` in  user name field we can comment password condition and put true condition like 1=1

---

## Step 3: inject form with True boolean operation

Use `'or 1=1 -- -` to find how many columns the original query returns. Increment until result doesn't appears.

![alt text](/assets/infinity/SQLI/login_logic/image-1.png) 

**username** : `' or 1=1-- -`
**Password** : `dummy`

and successfully logged in : 

![alt text](/assets/infinity/SQLI/login_logic/image-2.png)
---

## Key Takeaways

- always try `'` `"` first 
- Boolean based sql injection is hi risk 


---

Happy Hacking!  


Follow me: [LinkedIn](https://www.linkedin.com/in/t4t4r1s/) · [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>


