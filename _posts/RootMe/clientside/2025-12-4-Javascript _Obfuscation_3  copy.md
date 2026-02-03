---
layout: post
title: RootMe
subtitle: Javascript - Obfuscation 3
description: Javascript - Obfuscation 3
image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
optimized_image: https://www.root-me.org/IMG/logo/siteon0.svg?1637496509
category: [Root Me , web client]
tags:
  - RootME
  - JS - web clint
  - Find Password
author: mustafa_altayeb
date: 2025-12-04 00:00:00 +0000
paginate: true
---

# Javascript - Obfuscation 3 - RootMe

- **when start challenge this alert window will open to say "Enter Password (if you enter it wrong will say FAUX PASSWORD HAHA :(   so that let's kill this challenge )    )"**

![](/assets/Rootmeimages/image.png)

## open source code and i find this  js code 
```js
function dechiffre(pass_enc){
var pass = "70,65,85,88,32,80,65,83,83,87,79,82,68,32,72,65,72,65";
var tab = pass_enc.split(',');
var tab2 = pass.split(',');var i,j,k,l=0,m,n,o,p = "";i = 0;j = tab.length;
k = j + (l) + (n=0);
n = tab2.length;
for(i = (o=0); i < (k = j = n); i++ ){o = tab[i-l];p += String.fromCharCode((o = tab2[i]));
if(i == 5)break;}
for(i = (o=0); i < (k = j = n); i++ ){
o = tab[i-l];
if(i > 5 && i < k-1)
p += String.fromCharCode((o = tab2[i]));
}
p += String.fromCharCode(tab2[17]);
pass = p;return pass;
}
String["fromCharCode"](dechiffre("\x35\x35\x2c\x35\x36\x2c\x35\x34\x2c\x37\x39\x2c\x31\x31\x35\x2c\x36\x39\x2c\x31\x31\x34\x2c\x31\x31\x36\x2c\x31\x30\x37\x2c\x34\x39\x2c\x35\x30"));

h = window.prompt('Entrez le mot de passe / Enter password');
alert( dechiffre(h) );
```

- after trying to understand it i take some steps but look at this 
```js
\x35\x35\x2c\x35\x36\x2c\x35\x34\x2c\x37\x39\x2c\x31\x31\x35\x2c\x36\x39\x2c\x31\x31\x34\x2c\x31\x31\x36\x2c\x31\x30\x37\x2c\x34\x39\x2c\x35\x30
```
Hexadecimal !! 

let's use function in js call `unescape()` thats's  _computes a new string in which hexadecimal escape sequences are replaced with the characters that they represent_ (MDN site say this )

after use it i find some numbers :
```js
unescape("\x35\x35\x2c\x35\x36\x2c\x35\x34\x2c\x37\x39\x2c\x31\x31\x35\x2c\x36\x39\x2c\x31\x31\x34\x2c\x31\x31\x36\x2c\x31\x30\x37\x2c\x34\x39\x2c\x35\x30")

'55,56,54,79,115,69,114,116,107,49,50'
```
some numbers :) ;

- in my few steps to understand the code i find this method `String.fromCharCode()` which static method returns a _string_ created from the specified sequence of UTF-16 code units (MDN again :) )

by use it i find the password :
```js
String.fromCharCode(55,56,54,79,115,69,114,116,107,49,50)

'786OsErtk12'
```

 
Finished. Happy Hacking!



<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>

Follow me:
- [LinkedIn](https://www.linkedin.com/in/t4t4r1s/)
- [X](https://x.com/T4T4R1S)

---
