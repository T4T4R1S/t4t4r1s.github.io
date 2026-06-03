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
/assets/labs/authenticationv/image: /assets/image/Portswigger/download.png
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

### Analysis

*(coming soon)*

### Steps

*(coming soon)*

---

## LAB 6 — Broken Brute-Force Protection, IP Block

> **Level:** `PRACTITIONER`

### Analysis

*(coming soon)*

### Steps

*(coming soon)*

---

## LAB 7 — Username Enumeration via Account Lock

> **Level:** `PRACTITIONER`

### Analysis

*(coming soon)*

### Steps

*(coming soon)*

---

## LAB 8 — 2FA Broken Logic

> **Level:** `PRACTITIONER`

### Analysis

*(coming soon)*

### Steps

*(coming soon)*

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