---
layout: post
title: PortSwigger - File upload vulnerabilities Labs
date: 2026-06-03 00:00:00 +0000
categories: [Writeups, PortSwigger, "Authentication"]
tags:
  - LABS
  - Authentication
  - PortSwigger
  - WebSecurity
subtitle: Walkthroughs for Labs 1-6
description: PortSwigger Web Security Academy - Authentication vulnerabilities labs
/assets/labs/authenticationv/image: /assets//assets/labs/authenticationv/image/Portswigger/download.png
paginate: true
---

# PortSwigger – Authentication Vulnerabilities Labs

## LAB 1: Username Enumeration via Different Responses
`APPRENTICE`

![alt text](/assets/labs/authenticationv/image.png)

**Analysis**

Vulnerability:  username enumeration and password brute-force attacks
Goal: enumerate a valid username, brute-force this user's password, then access their account page. 
Key Concept: Different error messages reveal valid usernames — when an invalid username returns `Invalid username` but a valid one returns `Incorrect password` the difference in responses allows an attacker to enumerate valid usernames before brute-forcing the password.
l
**Steps to solve**
 1) Try to login with incorrect credentials and i got `invalid username` : 
 ![alt text](/assets/labs/authenticationv/image-1.png)

 2) In lab description i have 2 list of `usernames passwords` : 
 ![alt text](/assets/labs/authenticationv/image-2.png)

 3)intercept login request with burp and send it to intruder : 

 ![alt text](/assets/labs/authenticationv/image-3.png)

 4) Select user name field and add payload the user name list i got from lab description and start brute force and all response has `incorrect username` except one `americas`: 

 ![alt text](/assets/labs/authenticationv/image-4.png)

5) Now i find valid username let's try  brute force password for this account Change filter to get all redirect 30x and i find the password is password : 
![alt text](/assets/labs/authenticationv/image-5.png)

6) Now login with username `americas` , password `password` Solved :

![alt text](/assets/labs/authenticationv/image-6.png)

---

## LAB 2: 2FA Simple Bypass
`APPRENTICE`

![alt text](/assets/labs/authenticationv/image-7.png)

**Analysis**

- Vulnerability: Bypass 2FA 
- Goal: Carlos's account page
- Key Concept: 2FA can be bypassed by directly navigating to a protected page — if the application doesn't verify that the 2FA step was completed before granting access, an attacker can skip it entirely by jumping straight to the post-login URL after submitting valid credentials.

**Steps to solve**

1) access the lab and login with out account `wiener` `peter` and after login it's need 4-digit code to complete step 2 of login : 

![alt text](/assets/labs/authenticationv/image-8.png)

2) go to email with this button on the top of lab : 
![alt text](/assets/labs/authenticationv/image-9.png)

4) i find code has been sent `1723`: 
![alt text](/assets/labs/authenticationv/image-10.png)

5) and i redirected to my account : 
![alt text](/assets/labs/authenticationv/image-11.png)

6) in url i find the end point is `/my-account` with id =username : 
![alt text](/assets/labs/authenticationv/image-12.png)

7) logout and try to login to carlos account and it's required 4-digit but now i don't have carlos mail : 

![alt text](/assets/labs/authenticationv/image-13.png)

8) after look at the endpoint it's `login2` :
![alt text](/assets/labs/authenticationv/image-14.png)

9) change this endpoint to one we redirected to it after legal login in our account `/my-account`and SOLVED:

![alt text](/assets/labs/authenticationv/image-15.png)

---

## LAB 3: Password Reset Broken Logic
`APPRENTICE`

![alt text](/assets/labs/authenticationv/image-16.png)

**Analysis**

- Vulnerability: Vulnerable password reset functionality
- Goal: reset Carlos's password then log in
- Key Concept: The password reset token is not validated server-side — the application accepts a password reset request even if the token is missing or tampered with, allowing an attacker to reset any user's password by simply changing the `username` parameter in the request.

**Steps to solve**
1) start lab and login to my account `wiener:peter`: 
![alt text](/assets/labs/authenticationv/image-17.png)

2) logout and click forget password write username and click submit : 
![alt text](/assets/labs/authenticationv/image-18.png)

3) go to Email Client from button on the top of the page: 
![alt text](/assets/labs/authenticationv/image-19.png)

4) Copy link and start burp to store all traffic: 
![alt text](/assets/labs/authenticationv/image-20.png)

5) after open link set new password page appear : 
![alt text](/assets/labs/authenticationv/image-21.png)

6) intercept request and put new password : 
![alt text](/assets/labs/authenticationv/image-22.png)

7) From previous image the password set using user name send request to repeater and try to change it to victim username in my case is `carlos` and it's success: 
![alt text](/assets/labs/authenticationv/image-23.png)
 
 8) now try to login with password i set and username carlos and SOLVED: 

 ![alt text](/assets/labs/authenticationv/image-24.png)

---

## LAB 4: Username Enumeration via Subtly Different Responses
`PRACTITIONER`
![alt text](/assets/labs/authenticationv/image-26.png)
**Analysis**

- Vulnerability: Vulnerable to user enumeration 
- Goal: find valid username and password
- Key Concept: The username and password is vulnerable to brute force attack but here the developer mistake is `.` if the username is valid it's  not appear in the response and if password and username is invalid `.` appear 


**Steps to solve**
1) Download username list and password list to use it in our attack : 
![alt text](/assets/labs/authenticationv/image-25.png)

2) login with invalid username and password and intercept request int burp and send it to intruder : 

![alt text](/assets/labs/authenticationv/image-27.png)

3) now let's start brute force username with list i just downloaded : 
![alt text](/assets/labs/authenticationv/image-28.png)

4)if lock at all response in got `Invalid username or password.` i will do negative search on it to see different responses: 
`filter`
![alt text](/assets/labs/authenticationv/image-29.png)

5) i found one username the `.` after password doesn't appear and it's alpha: 

![alt text](/assets/labs/authenticationv/image-30.png)

5) now i have valid username i will brute force password for this username using the list i downloaded and intruder : 
![alt text](/assets/labs/authenticationv/image-31.png)

6) filter output with 30x `forward` : 
![alt text](/assets/labs/authenticationv/image-32.png)

7) i got one password `jessica` try to login and it's SOLVED: 

![alt text](/assets/labs/authenticationv/image-33.png)
---

## LAB 5: Username Enumeration via Response Timing
`PRACTITIONER`

**Analysis**

**Steps to solve**

---

## LAB 6: Broken Brute-Force Protection, IP Block
`PRACTITIONER`

**Analysis**

**Steps to solve**

---

## LAB 7: Username Enumeration via Account Lock
`PRACTITIONER`

**Analysis**

**Steps to solve**

---

## LAB 8: 2FA Broken Logic
`PRACTITIONER`

**Analysis**

**Steps to solve**

---

## LAB 9: Brute-Forcing a Stay-Logged-In Cookie
`PRACTITIONER`

**Analysis**

**Steps to solve**

---

## LAB 10: Offline Password Cracking
`PRACTITIONER`

**Analysis**

**Steps to solve**

---

## LAB 11: Password Reset Poisoning via Middleware
`PRACTITIONER`

**Analysis**

**Steps to solve**

---

## LAB 12: Password Brute-Force via Password Change
`PRACTITIONER`

**Analysis**

**Steps to solve**

---

## LAB 13: Broken Brute-Force Protection, Multiple Credentials per Request
`EXPERT`

**Analysis**

**Steps to solve**

---

## LAB 14: 2FA Bypass Using a Brute-Force Attack
`EXPERT`

**Analysis**

**Steps to solve**

---

**Finished — Happy Hacking!**

---
**Find me online**:  
• TryHackMe: [t4t4r1s](https://tryhackme.com/p/t4t4r1s)  
• HackTheBox: [t4t4r1s](https://app.hackthebox.com/users/2203575)  
• LinkedIn: [Mustafa Eltayeb](https://www.linkedin.com/in/t4t4r1s)  
• X: [@mustafa_altayeb](https://x.com/t4t4r1s)

---
<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>


