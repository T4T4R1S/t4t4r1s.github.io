---
layout: page
title: Writeups
icon: fas fa-flag
order: 1
permalink: /writeups/
---

## Writeups

<ul>
{% for post in site.categories.Writeups %}
  <li><span>{{ post.date | date: "%B %d, %Y" }}</span> &raquo; <a href="{{ post.url }}">{{ post.title }}</a></li>
{% endfor %}
</ul>
