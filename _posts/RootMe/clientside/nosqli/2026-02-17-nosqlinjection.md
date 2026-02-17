---
layout: post
title: RootMe - NoSql Injection Challenges
subtitle: Walkthroughs for Web-Client NoSqli Labs
description: RootMe challenge walkthroughs - NoSql Injection Authentication, String, Numeric, Error, Time Based, Blind
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: [Root Me, web server]
tags: [RootMe, CTF, Web, NoSqlInjection, Authentication, Blind, TimeBased, UnionBased]
author: mustafa_altayeb
date: 2026-02-17 00:09:00 +0000
paginate: true
---

## RootMe  – NoSql Injection Challenges (Web-Client)

Just solved a bunch of NoSQL Injection challenges on RootMe.  
These challenges focus on discovering injection points in web applications and exploiting them manually or using tools like NoSQLMap to extract credentials.

Below are my quick notes and walkthroughs for each challenge.

---

/assets/Rootmeimages/nosql/image

## 1. NoSQL Injection – Authentication

![Authentication Challenge](/assets/Rootmeimages/nosql/image.png)

### Mission
1. Find the username of the hidden user.

---

### Solution Steps

1. Start the challenge and locate the login form:

   ![Login Form](/assets/Rootmeimages/nosql/image-1.png)

2. Open Burp Suite, intercept the request, and send it to Repeater:

   ![Burp Repeater](/assets/Rootmeimages/nosql/image-2.png)

3. Inject login parameters using the `$ne` (not equal) operator.  
   The response confirms: "I'm admin".

   ![Admin Response](/assets/Rootmeimages/nosql/image-3.png)

4. Since we need the hidden user, modify the payload to exclude `admin`:

   ![Exclude Admin](/assets/Rootmeimages/nosql/image-4.png)

5. The response returns "I'm test", which is not the hidden user.  
   Use `$nin` (not in) to exclude multiple known users and retrieve the flag:

   ![Hidden User Flag](/assets/Rootmeimages/nosql/image-5.png)

> [!abstract]
> Tip:  
> `$nin` requires an array, so always use square brackets `[]`.

Finished.

---

## 2. NoSQL Injection – Blind

![Blind Challenge](/assets/Rootmeimages/nosql/image-6.png)

### Mission
1. Retrieve the flag for the challenge `nosqlblind`.

---

### Solution Steps

1. Open the challenge and identify the two fields:
   - `challenge name`
   - `flag`

   ![Challenge Fields](/assets/Rootmeimages/nosql/image-7.png)

2. Enter `nosqlblind` as the challenge name and a random value in the flag field.  
   Intercept the request using Burp Suite and send it to Repeater:

   ![Intercepted Request](/assets/Rootmeimages/nosql/image-8.png)

3. After testing multiple operators, the successful one is `$regex`.  
   Use the payload:

```

[$regex]=.{1}

```

The injection works when the length is correct.

![Regex Injection](/assets/Rootmeimages/nosql/image-10.png)

4. Send the request to Intruder:

![Intruder Setup](/assets/Rootmeimages/nosql/image-11.png)

5. Modify the payload to brute-force character by character:
- Add `^` after `.{1}`
- Use payloads: `a-z`, `A-Z`, `0-9`, `. , @ # _`

When the response message changes to "yeah......", it means the guess is correct.

![Valid Character Found](/assets/Rootmeimages/nosql/image-10.png)

6. Start extracting the flag:

- First character: `3`

  ![First Char](/assets/Rootmeimages/nosql/image-12.png)

  Add it to the payload:

  ![Payload Update](/assets/Rootmeimages/nosql/image-13.png)

- Second character: `@`

  ![Second Char](/assets/Rootmeimages/nosql/image-14.png)

  Update payload again:

  ![Payload Update](/assets/Rootmeimages/nosql/image-15.png)

7. Repeat the process to retrieve the full flag:

```

3@sY_...........n

```

Finished..Happy Hacking..!

---
Follow me:  
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)  
- [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>
