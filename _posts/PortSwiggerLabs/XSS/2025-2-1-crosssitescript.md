---
layout: post
title: PortSwigger
subtitle: Cross Site Script (XSS)
description: Cross Site Script(XSS)
image: /assets/image/Portswigger/download.png
optimized_image: /assets/image/Portswigger/download.png
category: Portswigger Labs
tags:
  - portswigger
  - client-side
  - Cross Site Script(XSS)
author: mustafa_altayeb
date: 2025-12-16 00:00:00 +0000
paginate: true
---

## LAB 1 (Reflected XSS into HTML context with nothing encoded)

**Analysis**

1) lab contains reflected xss
2) to solve we need to exec `alert` function

**steps to solve**

1- after access the lab i find search input and it's display what i write to screen .

![](/assets/image/Portswigger/xss/image.png)

2- Execute basic payload `<img src=x onerror=alert(0)>` it's success 


Finished..Happy hacking!

## LAB 2 (Stored XSS into HTML context with nothing encoded)

**Analysis**

1) lab contains reflected xss
2) to solve we need to exec `alert` function

**steps to solve**
1) search in the lab for input field after click view post i find a full form to post comment .
2) I Post an email with special words to see how browser will handle it .
![](/assets/image/Portswigger/xss/image3.png)
3) it's appear in comments names and comment .
![](/assets/image/Portswigger/xss/image4.png)
4) Execute basic payload in comment field and name field  `<img src=x onerror=alert(0)>` it's success 
![](/assets/image/Portswigger/xss/image5.png)

Finished..Happy hacking!

#LAB 3 (DOM XSS in document.write sink using source location.search)

**Analysis**
1) lab contain Dom based XSS in search query.
2) To solve it we need to exec `alert` function.

**steps to solve**

1) By locking in js code after search we find the text we write putted in img src (search query) 
![](/assets/image/Portswigger/xss/image7.png)

2) To make alert work we need to inject it with 
                                     - `">` to close search query
                                     - any payload like `<img src=x onerror=alert(0)>`
![](/assets/image/Portswigger/xss/image8.png)

Finished.. Happy Hacking!


## LAB 3  DOM XSS in innerHTML sink using source location.search

**Analysis**

1) lab contains a DOM-based cross-site scripting vulnerability in the search blog functionality 
2) add the content to the page with innerHTML 

**steps to solve**

1) by see the page source i find the js code that take our search and find what match 
2) after that call function `doSearchQuery()` that take findings and put it in the element by `innerHtml` 
3) by inject the search query with `<svg onload='alert(t4t4r1s)'>` message alerted .

Finished.. Happy Hacking! 



## LAB 4 DOM XSS in jQuery anchor href attribute sink using location.search source

**Analysis**

1) DOM-based xss --> feedback page
2) to solve the lab we need to alert document.cookie

**steps to solve**


1) analysis the page and i find `returnPath` param take the path to submit feedback 
2) put a string to param and i see inspect the href take what i write and put it as a link `<a id="backLink" href="/ds">Back</a>`
3) I tried to inject the form it self and it's not vulnerable 
4) after check the param `returnPath` and give it `javascript:alert(document.cookie)` it's run and lab has been solved .

Finished.. Happy Hacking! 

## LAB 5