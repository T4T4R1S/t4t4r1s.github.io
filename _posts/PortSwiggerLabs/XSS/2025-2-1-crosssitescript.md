---
layout: post
title: PortSwigger
subtitle: Cross Site Scripting (XSS)
description: Cross Site Scripting (XSS)
image: /assets/image/Portswigger/download.png
optimized_image: /assets/image/Portswigger/download.png
category: PortSwigger Labs
tags:
  - portswigger
  - client-side
  - Cross Site Scripting (XSS)
author: mustafa_altayeb
date: 2026-01-20 00:00:00 +0000
paginate: true
---

## LAB 1 (Reflected XSS into HTML context with nothing encoded)

**Analysis**

1. Lab contains reflected XSS
2. To solve, we need to execute the `alert` function

**Steps to solve**

1. After accessing the lab, I found a search input that displays what I write on the screen.

![](/assets/image/Portswigger/xss/image.png)

2. Executed basic payload: `<img src=x onerror=alert(0)>` → success

**Finished.. Happy hacking!**

## LAB 2 (Stored XSS into HTML context with nothing encoded)

**Analysis**

1. Lab contains stored XSS
2. To solve, we need to execute the `alert` function

**Steps to solve**

1. Searched the lab for input fields; after clicking "view post", found a full comment form.
2. Posted a comment with special words to test how the browser handles it.

![](/assets/image/Portswigger/xss/image3.png)

3. It appeared in the commenter's name and comment body.

![](/assets/image/Portswigger/xss/image4.png)

4. Executed basic payload in both comment and name fields: `<img src=x onerror=alert(0)>` → success

![](/assets/image/Portswigger/xss/image5.png)

**Finished.. Happy hacking!**

## LAB 3 (DOM XSS in document.write sink using source location.search)

**Analysis**

1. Lab contains DOM-based XSS in the search query.
2. To solve, we need to execute the `alert` function.

**Steps to solve**

1. Inspected the JavaScript code; after searching, found the search term inserted into an `img src` via `document.write`.

![](/assets/image/Portswigger/xss/image7.png)

2. To make the alert work, injected:  
   `"><img src=x onerror=alert(0)>`  
   (closing the attribute and adding the payload)

![](/assets/image/Portswigger/xss/image8.png)

**Finished.. Happy hacking!**

## LAB 4 (DOM XSS in innerHTML sink using source location.search)

**Analysis**

1. Lab contains a DOM-based XSS vulnerability in the search blog functionality.
2. Content is added to the page using `innerHTML`.

**Steps to solve**

1. Viewed the page source and found the JavaScript code that processes the search query.
2. It calls the function `doSearchQuery()` which inserts findings via `innerHTML`.
3. Injected into the search query: `<svg onload=alert('t4t4r1s')>` → alert popped up.

**Finished.. Happy hacking!**

## LAB 5 (DOM XSS in jQuery anchor href attribute sink using location.search source)

**Analysis**

1. DOM-based XSS on the feedback page.
2. Goal: execute `alert(document.cookie)`.

**Steps to solve**

1. Analyzed the page and found the `returnPath` parameter controls the redirect path after submitting feedback.
2. Inserted a test string into the parameter and inspected the href of the "Back" link:  
   `<a id="backLink" href="/ds">Back</a>`
3. Tried injecting into the form itself → not vulnerable.
4. Set the `returnPath` parameter to:  
   `javascript:alert(document.cookie)`  
   → the link executed the JavaScript when clicked → lab solved.

**Finished.. Happy hacking!**