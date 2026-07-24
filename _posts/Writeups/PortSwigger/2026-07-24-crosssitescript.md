---
layout: post
title: PortSwigger - Cross-Site Scripting (XSS) vulnerabilities labs
date: 2026-07-24 00:00:00 +0000
categories: [Writeups, PortSwigger, "Cross-Site Scripting"]
tags:
  - LABS
  - XSS
  - Cross-Site Scripting
  - PortSwigger
  - WebSecurity
subtitle: Walkthroughs for Labs 1-30
description: PortSwigger Web Security Academy - Cross-Site Scripting (XSS) vulnerabilities labs
/assets/labs/xsss/image: /assets//assets/labs/xsss/image/Portswigger/download.png
paginate: true
---
# PortSwigger – Cross-Site Scripting (XSS) Vulnerabilities Labs
---
## LAB 1 — Reflected XSS into HTML Context with Nothing Encoded
> **Level:** `APPRENTICE`

![alt text](/assets/labs/xsss/image.png)

### Analysis
| | |
|---|---|
| **Vulnerability** | Reflected XSS |
| **Goal** | Trigger an `alert()` in the browser |
| **Key Concept** | User input is reflected directly into the HTML response with no encoding or sanitization — injecting `<script>alert(1)</script>` executes immediately |
| **Key Takeaway** | The simplest form of XSS — if input appears in the page unchanged, the browser treats it as HTML/JS |

### Steps

1) the lab contain search input to find anything in blog when i write word on it it's appear on the page : 
![alt text](/assets/labs/xsss/image-1.png)

2) if i go to source code i see that it's appear in `h1` tag  : 
![alt text](/assets/labs/xsss/image-2.png)

3) i will close this tag and start script tag to write java script with `'</h1><script>alert(1)</script>` an i got alert SOLVED: 
![alt text](/assets/labs/xsss/image-3.png)

---
## LAB 2 — Stored XSS into HTML Context with Nothing Encoded
> **Level:** `APPRENTICE`
![alt text](/assets/labs/xsss/image-4.png)
### Analysis
| | |
|---|---|
| **Vulnerability** | Stored XSS |
| **Goal** | Trigger an `alert()` when any user views the page |
| **Key Concept** | Malicious input is saved to the database and rendered unsanitized on every page load — the payload persists and fires for every visitor |
| **Key Takeaway** | Stored XSS is more dangerous than reflected — it requires no user interaction beyond visiting the page |

### Steps
1) start lab and click view any post and write a comment like this : 
![alt text](/assets/labs/xsss/image-5.png)

2) after submit comment it's appear on the page : 
![alt text](/assets/labs/xsss/image-6.png)

3) it's appear in 2 places i will inject script after anchor element `<a>` and that's name input not work `</a><script>alert(1)</script>`: 
![alt text](/assets/labs/xsss/image-7.png)

4) try to inject comment it self and it's work SOLVED no need to anchor element but i don't change last inject: 
![alt text](/assets/labs/xsss/image-8.png)

---
## LAB 3 — DOM XSS in `document.write` Sink Using Source `location.search`
> **Level:** `APPRENTICE`

![alt text](/assets/labs/xsss/image-9.png)

### Analysis
| | |
|---|---|
| **Vulnerability** | DOM-based XSS |
| **Goal** | Trigger an `alert()` via a DOM sink |
| **Key Concept** | JavaScript reads `location.search` and passes it to `document.write()` without sanitization — breaking out of the HTML context with `">` allows injecting arbitrary tags |
| **Key Takeaway** | DOM XSS happens entirely in the browser; the server never sees or sends the payload — classic source-to-sink flow |

### Steps

1) first search for anything like `t4t4r1s` and it's appear in search :
![alt text](/assets/labs/xsss/image-10.png) 

2) right click and view page source and see that we have function take query as a parameter we can change query to break syntax  : 
![alt text](/assets/labs/xsss/image-11.png)

3) `document.write('<img src="/resources//assets/labs/xsss/images/tracker.gif?searchTerms='+query+'">');` we can change our input to break /assets/labs/xsss/image like 
`><img src="sdfsd" onload=alert(1)/>`:

![alt text](/assets/labs/xsss/image-12.png)

4) got an alert. SOLVED : 
![alt text](/assets/labs/xsss/image-13.png)


---
## LAB 4 — DOM XSS in `innerHTML` Sink Using Source `location.search`
> **Level:** `APPRENTICE`

![alt text](/assets/labs/xsss/image-14.png)

### Analysis
| | |
|---|---|
| **Vulnerability** | DOM-based XSS |
| **Goal** | Trigger an `alert()` via `innerHTML` |
| **Key Concept** | `innerHTML` does not execute `<script>` tags but does execute event handlers — payloads like `<img src=x onerror=alert(1)>` bypass this restriction |
| **Key Takeaway** | `innerHTML` is a dangerous sink; always use `textContent` or proper sanitization when inserting user-controlled data into the DOM |

### Steps

1) start lab and click view page source  and i see our search query is used in innerHTML to include data: 

![alt text](/assets/labs/xsss/image-15.png)

2) inject any js code and got alert `<img src=sdf onerror=alert(1)>` js will search for link sdf and it's wrong link so that it will trigger onerror event and we will got alert: 

![alt text](/assets/labs/xsss/image-16.png)

---
## LAB 5 — DOM XSS in jQuery Anchor `href` Attribute Sink Using `location.search` Source
> **Level:** `APPRENTICE`

![alt text](/assets/labs/xsss/image-17.png)

### Analysis
| | |
|---|---|
| **Vulnerability** | DOM-based XSS via jQuery |
| **Goal** | Trigger an `alert()` when the "back" link is clicked |
| **Key Concept** | jQuery sets the `href` attribute of an anchor tag using `location.search` — injecting `javascript:alert(1)` as the value causes code execution on click |
| **Key Takeaway** | `href` attributes accept `javascript:` URIs; sinks that set link targets are exploitable even without HTML tag injection |

### Steps
1) start lab and go to submit feed back : 
![alt text](/assets/labs/xsss/image-18.png)

2) in the link is see `returnpath=/ `: 
![alt text](/assets/labs/xsss/image-22.png)

3) add any value after / and inspect page i find what i type after / included in button href :

![alt text](/assets/labs/xsss/image-23.png)

4) now i can inject any js code i will use alert to solve the lab `javascript:alert(1)` and SOLVED : 
![alt text](/assets/labs/xsss/image-24.png)
---


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