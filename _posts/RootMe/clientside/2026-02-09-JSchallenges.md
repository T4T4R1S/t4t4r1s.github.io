---
layout: post
title: RootMe - JavaScript Challenges
subtitle: Walkthroughs for Web-Client JS Labs
description: RootMe challenge walkthroughs - JavaScript Source, Obfuscation, and Authentication
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: [Root Me , web client]
tags: [RootMe, CTF, Web, JavaScript, Obfuscation, Authentication, SourceAnalysis]
author: mustafa_altayeb
date: 2026-02-09 00:09:00 +0000
paginate: true
---

# RootMe – JavaScript Challenges (Web-Client)

Just solved a bunch of beginner JavaScript challenges on RootMe. These are all about inspecting client-side code to find hidden passwords or bypass auth. Here's my quick notes for each one.

## 1. Javascript - Source

**Mission**  
Get the password to login.

**Analysis**  
- Page shows a login prompt in an alert box.  

  ![](/assets/Rootmeimages/jsimage/image1.png)

- Need to find the hidden password somewhere in the source.

**Solution steps**  
- Inspect the page (right-click → View Source or Ctrl+U) → check the `<head>` section.  
- Found a JS script with an if-statement checking the password: `123456azerty`.  

  ![](/assets/Rootmeimages/jsimage/image2.png)

- Enter that in the prompt → logged in!

## 2. Javascript - Obfuscation 1

**Mission**  
Get the password to login.

**Analysis**  
- Again, a login alert pops up.  

  ![](/assets/Rootmeimages/jsimage/image.png)

- Password is hidden/obfuscated in the code.

**Solution steps**  
- Inspect page → found JS in `<head>`.  

  ![](/assets/Rootmeimages/jsimage/image-1.png)

- The password looks URL-encoded.  
- Decode it using Burp Suite's Decoder (or any online tool).  

  ![](/assets/Rootmeimages/jsimage/image-2.png)

- Decoded to: `cpasbiendurpassword`.  
- Use that to login.

## 3. Javascript - Obfuscation 2

**Mission**  
Get the password to login.

**Analysis**  
- Login alert like before.  

  ![](/assets/Rootmeimages/jsimage/image.png)

- Code is more obfuscated this time.

**Solution steps**  
- Inspect page → JS script in `<head>`.  

  ![](/assets/Rootmeimages/jsimage/image-3.png)

- Password is double URL-encoded → decode twice in Burp.  

  ![](/assets/Rootmeimages/jsimage/image-4.png)

- Then it's a `String.fromCharCode()` call (MDN says it builds strings from char codes).  
- Run the codes: `String.fromCharCode(104,68,117,102,106,100,107,105,49,53,54)` → gets you the password.  

  ![](/assets/Rootmeimages/jsimage/image-5.png)

## 4. Javascript - Authentication

**Mission**  
Bypass or find credentials for login.

**Analysis**  
- Simple login page.  

  ![](/assets/Rootmeimages/jsimage/image-6.png)

**Solution steps**  
- View page source → spotted a linked JS file.  

  ![](/assets/Rootmeimages/jsimage/image-7.png)

- Open the JS file → it has the auth logic with username and password hardcoded.  

  ![](/assets/Rootmeimages/jsimage/image-8.png)

- Use those creds to login.

## 5. Javascript - Authentication 2

**Mission**  
Login as admin or something similar.

**Analysis**  
- Webpage with a login button.  

  ![](/assets/Rootmeimages/jsimage/image-9.png)

- Clicking it pops an alert for credentials.  

  ![](/assets/Rootmeimages/jsimage/image-10.png)

**Solution steps**  
- Inspect page → found a linked JS file.  

  ![](/assets/Rootmeimages/jsimage/image-11.png)

- Open the file → credentials are right there in plain text.  

  ![](/assets/Rootmeimages/jsimage/image-12.png)

- Enter them in the prompt → success.

Follow me:  
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)  
- [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>