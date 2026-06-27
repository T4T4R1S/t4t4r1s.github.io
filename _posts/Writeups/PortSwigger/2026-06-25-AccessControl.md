---
layout: post
title: PortSwigger - Access Control vulnerabilities labs
date: 2026-06-25 00:00:00 +0000
categories: [Writeups, PortSwigger, "Access Control"]
tags:
  - LABS
  - Access Control
  - PortSwigger
  - WebSecurity
subtitle: Walkthroughs for Labs 1-13
description: PortSwigger Web Security Academy - Access Control vulnerabilities labs
image: /assets/image/Portswigger/download.png
paginate: true
---
# PortSwigger – Access Control Vulnerabilities Labs
---
## LAB 1 — Unprotected Admin Functionality
> **Level:** `APPRENTICE`

![alt text](image.png)

### Analysis
| | |
|---|---|
| **Vulnerability** | Unprotected admin panel |
| **Goal** | Delete the user carlos |
| **Key Concept** | After enumeration we find a file called `robots.txt` which contains directives to prevent bots from accessing the admin panel. Accessing that path directly gives us a fully functional admin interface |

### Steps

**1.** Start the lab and navigate to `/robots.txt` — it reveals the path `/administrator-panel`:
![alt text](image-1.png)

**2.** Access `/administrator-panel` and find the option to delete users:
![alt text](image-2.png)

**3.** Delete carlos → Solved:
![alt text](image-3.png)

---
## LAB 2 — Unprotected Admin Functionality with Unpredictable URL
> **Level:** `APPRENTICE`

![alt text](image-4.png)

### Analysis
| | |
|---|---|
| **Vulnerability** | Unprotected admin panel |
| **Goal** | Delete the user carlos |
| **Key Concept** | The page contains a JavaScript snippet that routes users based on their role. The admin panel path is embedded in this script and is visible in the page source |

### Steps

**1.** Start the lab, right-click → View Page Source, and find the admin panel path inside a JS block:
![alt text](image-5.png)

**2.** Navigate to the admin panel and delete user carlos → Solved:
![alt text](image-6.png)

---
## LAB 3 — User Role Controlled by Request Parameter
> **Level:** `APPRENTICE`

![alt text](image-7.png)

### Analysis
| | |
|---|---|
| **Vulnerability** | Access control bypass via cookie manipulation |
| **Goal** | Delete user carlos |
| **Key Concept** | The application stores the user's role in a cookie (`Admin=false`). By intercepting the request and changing it to `Admin=true`, the admin panel becomes accessible |

### Steps

**1.** Start the lab and login as `wiener` / `peter`:
![alt text](image-8.png)

**2.** Reload the page and intercept the request with Burp:
![alt text](image-9.png)

**3.** Change `Admin=false` → `Admin=true` and forward the request:
![alt text](image-10.png)
![alt text](image-11.png)

**4.** The admin panel link now appears in the navigation:
![alt text](image-12.png)

**5.** Clicking it shows `Admin interface only available if logged in as an administrator` — the check runs on each request:
![alt text](image-13.png)

**6.** Intercept the next request and again change `Admin=true`:
![alt text](image-14.png)
![alt text](image-15.png)

**7.** Access the admin panel, intercept the delete request, set `Admin=true` again → carlos deleted → Solved:
![alt text](image-16.png)
![alt text](image-17.png)

---
## LAB 4 — User Role Can Be Modified in User Profile
> **Level:** `APPRENTICE`

![alt text](image-18.png)

### Analysis
| | |
|---|---|
| **Vulnerability** | Access control bypass via mass assignment on the update email endpoint |
| **Goal** | Delete user carlos |
| **Key Concept** | When updating the email address, the server response includes a `roleid` field. Sending `"roleid": 2` in the request body causes the server to accept and apply it, escalating our privileges to admin |

### Steps

**1.** Start the lab and login with `wiener` / `peter`:
![alt text](image-19.png)

**2.** Use the update email functionality and intercept the request with Burp:
![alt text](image-20.png)

**3.** Send the request to Repeater:
![alt text](image-21.png)

**4.** The response contains a `roleid` key — add `"roleid": 2` to the request body and resend:
![alt text](image-22.png)

**5.** Go back to the browser — the admin panel link is now visible:
![alt text](image-23.png)

**6.** Click the admin panel and delete user carlos → Solved:
![alt text](image-24.png)

---
## LAB 5 — User ID Controlled by Request Parameter
> **Level:** `APPRENTICE`

![alt text](image-25.png)

### Analysis
| | |
|---|---|
| **Vulnerability** | Horizontal privilege escalation |
| **Goal** | Obtain the API key for user carlos and submit it as the solution |
| **Key Concept** | The account page URL uses a `?id=username` parameter. Changing it to another username loads that user's account page and leaks their API key |

### Steps

**1.** Start the lab and login as `wiener` — observe the account page URL:
![alt text](image-26.png)

**2.** Intercept the request with Burp:
![alt text](image-27.png)

**3.** Send to Repeater and change the `id` parameter to `carlos`:
![alt text](image-28.png)

**4.** The response contains carlos's API key — copy and submit it → Solved:
![alt text](image-29.png)
![alt text](image-30.png)

---
## LAB 6 — User ID Controlled by Request Parameter, with Unpredictable User IDs
> **Level:** `APPRENTICE`

![alt text](image-31.png)

### Analysis
| | |
|---|---|
| **Vulnerability** | Horizontal privilege escalation |
| **Goal** | Find the GUID for carlos, then submit his API key as the solution |
| **Key Concept** | User IDs are GUIDs, not usernames. By finding a blog post authored by carlos and clicking his name, the GUID is exposed in the URL. Substituting it in the account page URL leaks his API key |

### Steps

**1.** Start the lab and login as `wiener`:
![alt text](image-32.png)

**2.** Browse the blog and find a post authored by carlos:
![alt text](image-33.png)

**3.** Click on carlos's name and intercept the request — the GUID is visible in the URL:
![alt text](image-34.png)

**4.** Copy the GUID and use it in the `?id=` parameter on the account page:
![alt text](image-35.png)

**5.** Submit the API key → Solved:
![alt text](image-36.png)

---
## LAB 7 — User ID Controlled by Request Parameter with Data Leakage in Redirect
> **Level:** `APPRENTICE`

![alt text](image-37.png)

### Analysis
| | |
|---|---|
| **Vulnerability** | Sensitive information leaked in the body of a redirect response |
| **Goal** | Obtain the API key for user carlos and submit it as the solution |
| **Key Concept** | When changing the `id` parameter to another user, the application issues a `302` redirect to the login page — but the response body still contains the target user's account page, including their API key |

### Steps

**1.** Start the lab and login as `wiener` / `peter`:
![alt text](image-38.png)

**2.** Reload the account page and intercept the request with Burp:
![alt text](image-39.png)

**3.** Send to Repeater and change the `id` parameter to `carlos`:
![alt text](image-40.png)

**4.** The server returns a `302` redirect, but the full account page is in the response body:
![alt text](image-41.png)

**5.** Use the Render tab to view the page — carlos's API key is visible:
![alt text](image-42.png)

**6.** Copy the API key, submit it → Solved:
![alt text](image-43.png)

---
## LAB 8 — User ID Controlled by Request Parameter with Password Disclosure
> **Level:** `APPRENTICE`

![alt text](image-44.png)

### Analysis
| | |
|---|---|
| **Vulnerability** | Horizontal privilege escalation leading to password disclosure |
| **Goal** | Retrieve the administrator's password, then log in and delete user carlos |
| **Key Concept** | The account page populates the password field with the user's actual password. By changing the `id` parameter to `administrator`, we can read the pre-filled password from the response |

### Steps

**1.** Start the lab and login with `wiener` / `peter`:
![alt text](image-45.png)

**2.** Reload the account page and intercept the request with Burp:
![alt text](image-46.png)

**3.** Send to Repeater and change the `id` parameter to `administrator` — the response contains a masked password field:
![alt text](image-47.png)

**4.** Switch to the Pretty view to read the plaintext password:
![alt text](image-48.png)

**5.** Login as `administrator` with that password, navigate to the admin panel, delete carlos → Solved:
![alt text](image-49.png)

---
## LAB 9 — Insecure Direct Object References
> **Level:** `APPRENTICE`

### Analysis
| | |
|---|---|
| **Vulnerability** | |
| **Goal** | |
| **Key Concept** | |

### Steps

---
## LAB 10 — URL-Based Access Control Can Be Circumvented
> **Level:** `PRACTITIONER`

### Analysis
| | |
|---|---|
| **Vulnerability** | |
| **Goal** | |
| **Key Concept** | |

### Steps

---
## LAB 11 — Method-Based Access Control Can Be Circumvented
> **Level:** `PRACTITIONER`

### Analysis
| | |
|---|---|
| **Vulnerability** | |
| **Goal** | |
| **Key Concept** | |

### Steps

---
## LAB 12 — Multi-Step Process with No Access Control on One Step
> **Level:** `PRACTITIONER`

### Analysis
| | |
|---|---|
| **Vulnerability** | |
| **Goal** | |
| **Key Concept** | |

### Steps

---
## LAB 13 — Referer-Based Access Control
> **Level:** `PRACTITIONER`

### Analysis
| | |
|---|---|
| **Vulnerability** | |
| **Goal** | |
| **Key Concept** | |

### Steps

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