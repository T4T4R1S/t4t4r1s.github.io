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

*(coming soon)*

### Steps

*(coming soon)*

---

## LAB 10 — Offline Password Cracking

> **Level:** `PRACTITIONER`

### Analysis

*(coming soon)*

### Steps

*(coming soon)*

---

## LAB 11 — Password Reset Poisoning via Middleware

> **Level:** `PRACTITIONER`

### Analysis

*(coming soon)*

### Steps

*(coming soon)*

---

## LAB 12 — Password Brute-Force via Password Change

> **Level:** `PRACTITIONER`

### Analysis

*(coming soon)*

### Steps

*(coming soon)*

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