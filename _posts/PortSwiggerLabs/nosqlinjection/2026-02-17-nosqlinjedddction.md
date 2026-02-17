---
layout: post
title: PortSwigger - NoSQL injection Labs
subtitle: Walkthroughs for Labs 1-5
description: PortSwigger Web Security Academy - NoSQL injection labs
image: /assets/image/Portswigger/download.png
category: PortSwigger Labs
tags: [PortSwigger, Server-Side, CommandInjection, CTF, WebSecurity]
author: mustafa_altayeb
date: 2026-02-17 00:00:00 +0000
paginate: true
---

# PortSwigger – NoSQL injection Labs

Just finished the  five NoSQL injection labs on PortSwigger. These are about finding injectable points in web apps, running shell commands, and handling blind injections with time delays or out-of-band tricks. Here's how I solved each one.

## LAB 1: Detecting NoSQL injection

**Analysis**  
 
1)  lab powered by mongoDB 
2) nosql is in product category lab 
3) to solve lab we need to display unreleased products . 

**Steps to solve**  

1) start with detect nosql injection in category parameter by inject `'` in product filter value and i got an error  : 

![alt text](/assets/image/Portswigger/nosqli/image.png)

2) let's assume that the backend condition is : 
```js
if(this.category =='Gifts'){
    // code that appear all product in gifts 
}
```

3) if(this.category =="Gifts`we write ' here and we got an error`") so that we can add a condition with && or || to get all products like : 

```js
if(this.category =='Gifts'){
    // code that appear all product in gifts 
}
```
now we can configure payloads like 
- && '1'='1 
- || '1'='1
- && 1=1
- || 1=1 
- '||1||' `success one `
4) inject category with ||1|| and i got challenge solved :
![alt text](/assets/image/Portswigger/nosqli/image-1.png)

Finished happy hacking!

## LAB 2: Exploiting NoSQL operator injection to bypass authentication

**Analysis**  

1) login functionality powered by MongoDB 
2) nosql injection is in login 
3) MongoDB operators will help us to solve challenge 
4) to solve lab i need to log into application as an administrator 
4) credentials to login wiener:peter


**Steps to solve**  

1) open our account with credentials wiener:peter : 
![alt text](/assets/image/Portswigger/nosqli/image-2.png)

2) intercept login request and send tor repeater after that forward request . 

3) login data send in a json format: 

![alt text](/assets/image/Portswigger/nosqli/image-3.png)

4) Now when i send login request with correct credentials i got '302' code response : 
![alt text](/assets/image/Portswigger/nosqli/image-4.png)

5) if i change this to Uncorrected credentials i got `200` as a response and forwarded to logging page : 

![alt text](/assets/image/Portswigger/nosqli/image-5.png)


5) i try to inject password with $ne operator `$ne`== `not equal ` --> `"$ne":"fakepassword"` i got `302` response code:
![alt text](/assets/image/Portswigger/nosqli/image-6.png)

6) now i'm sure password is vulnerable 

7) i change user name to `administrator` and i got a 200 response code that mean we are forwarded to login page that's mean no user name called administrator : 

![alt text](/assets/image/Portswigger/nosqli/image-7.png)

8) in Mongo operators i find `$regex` that find char by char in username and i start with `a` and i get username `admin3xkmt9yi` :

![alt text](/assets/image/Portswigger/nosqli/image-8.png)

9) i take a cookie in the response and change it in my browser to get admin access and i got it and challenge solved : 

![alt text](/assets/image/Portswigger/nosqli/image-9.png)

go to browser inspect and open application tab to change cookie: 
![alt text](/assets/image/Portswigger/nosqli/image-10.png)

lab correctly solved : 
![alt text](/assets/image/Portswigger/nosqli/image-11.png)
Finished happy hacking!


## LAB 3: Exploiting NoSQL injection to extract data
**Analysis**  

1) login functionality powered by MongoDB 
2) nosql injection is in login 
3) MongoDB operators will help us to solve challenge 
4) extract the password for the administrator user
4) credentials to login wiener:peter

>|hint : password is a lowercase 

**Steps to solve**  

1)open challenge and burp suit and login with credentials that we have and intercept all requests to find /login and /user/lookup?user=wiener: 

![alt text](/assets/image/Portswigger/nosqli/image-14.png)

![alt text](/assets/image/Portswigger/nosqli/image-13.png)

2) trying to inject id with '&&'1'='1 let's explain why 

assume that backend condition is :  
```js
if (username=='wiener *we inject here *'){
    //login
    }
```

so that if we put this payload to id parameter it's success because it's fully completed (don't forget to encode url )

![alt text](/assets/image/Portswigger/nosqli/image-16.png)

3) let's change wiener to administrator :

![alt text](/assets/image/Portswigger/nosqli/image-17.png)

4) find user called administrator and email 

5) back to the seconde request we send to repeater we find data send in username= &&password=

![alt text](/assets/image/Portswigger/nosqli/image-13.png)

6) so that we have a successful condition :

![alt text](/assets/image/Portswigger/nosqli/image-17.png)

7) check regex in username  : 

![alt text](/assets/image/Portswigger/nosqli/image-18.png)

8) assume that we have seen username and password in /login page and we tested username and it's found let's check password with length function :

![alt text](/assets/image/Portswigger/nosqli/image-19.png)

9) now we know that password access  is found let's know exactly number of char in password using burp intruder  :

![alt text](/assets/image/Portswigger/nosqli/image-21.png)

![alt text](/assets/image/Portswigger/nosqli/image-20.png)

10)password is 8 char and from hint in the challenge description all char is lowercase let's use cluster bomb in burp to fuzz this : 
 - set payload to `'%26%26this.password[0]=='a` 
 - add $$ in `0` and `a`
- first payload from 0 to 7 
- second one is from  a-z

![alt text](/assets/image/Portswigger/nosqli/image-22.png)

12)start intruder : 

this is the only first element filter all with length will find 209 length that all we need arrange  the array from 0 t 7 and this is a password 

![alt text](/assets/image/Portswigger/nosqli/image-23.png)

13) now we have an email and password  login in with this credentials and challenge solved ..!

Finished happy hacking!


## LAB 4: Blind NoSQL injection with out-of-band interaction
**Steps to solve**  

in this lab i perform all what i can do but the hidden field for mine is email and i will came back to this challenge after i learn how to solve it and now what's the problem 


---
**Find me online**:  
• TryHackMe: [t4t4r1s](https://tryhackme.com/p/t4t4r1s)  
• HackTheBox: [t4t4r1s](https://app.hackthebox.com/users/2203575)  
• LinkedIn: [Mustafa Altayeb](https://www.linkedin.com/in/t4t4r1s)  
• X: [@mustafa_altayeb](https://x.com/t4t4r1s)

---
<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>