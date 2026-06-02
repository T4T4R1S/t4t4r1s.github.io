---
layout: post
title: Infinity - SQL Injection - Second Strike
date: 2026-05-20 00:06:00 +0000
categories: [Writeups, Infinity, "SQL Injection"]
tags:
  - Infinity
author: mustafa_altayeb
subtitle: Manipulating POST Parameters for High Score
description: A walkthrough of exploiting Second-Order SQL Injection in an update username feature on Infinity platform. By injecting into an UPDATE query, we escalated  privileges from a regular user to admin without needing to know any credentials.
image: https://infinitylearning-images.s3.eu-west-2.amazonaws.com/images/public/second-strike.webp
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

# Infinity — SQL Injection: Second Strike

## Overview

A walkthrough of exploiting Second-Order SQL Injection in an update username feature on Infinity platform. By injecting into an UPDATE query, we escalated  privileges from a regular user to admin without needing to know any credentials.

**Vulnerability:** Boolean-based SQL Injection  

---
## Step 1: Identify the Input Field

Open the challenge and locate the Login form input field register and login : 

![alt text](/assets/infinity/SQLI/secondstrike/image.png)

![alt text](/assets/infinity/SQLI/secondstrike/image-1.png)

---

## Step 2: Try to predict backend behavior 

first let's imagine sql query : 
```sql
INSERT INTO users (username, password, is_admin) VALUES ('chosen_name','chosen_password',0);
```

all new user is_admin=0 

---

## Step 3:  Try to Predict updata functionality 

```sql
UPDATE users SET username='NEW_USERNAME' WHERE username='CURRENT_USERNAME';
```

we have access to change user name  : 

![alt text](/assets/infinity/SQLI/secondstrike/image-2.png)

i will try to break sql query and put is_admin=1 : 
`t4t4r1s' , is_admin=1 where username='mustafa'--`

`t4t4r1s`: the new username
`,` : to put new query 
`is_admin`=1 : to make our user has admin privilege 
`username`: the old username we create account with it


![alt text](/assets/infinity/SQLI/secondstrike/image-3.png)

enter update username and wait 120 s

and we got it : 
![alt text](/assets/infinity/SQLI/secondstrike/image-4.png)
## Key Takeaways

- SQL Injection doesn't only happen in login or search — any input that touches the database is a target, including profile update features.
- Second-Order SQLi is dangerous because the injection happens at a different point than where the input was entered — harder to detect.
- UPDATE queries can modify more columns than intended — always think about what other fields exist in the same table.

---

Happy Hacking!  


Follow me: [LinkedIn](https://www.linkedin.com/in/t4t4r1s/) · [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>


