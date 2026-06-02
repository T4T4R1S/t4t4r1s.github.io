---
title: Learning Path
layout: page
icon: fas fa-graduation-cap
order: 7
---

## Structured Learning Paths

{% if site.learning_path == null or site.learning_path.size == 0 %}
  *No topics yet. Check back later!*
{% else %}
  {% assign all_items = site.learning_path | sort: "order" %}
  {% assign categories = all_items | map: "category" | uniq %}
  {% for cat in categories %}

### {{ cat }}

  {% assign cat_items = all_items | where: "category", cat %}
  {% for item in cat_items %}
- [{{ item.title }}]({{ item.url }})
  {% endfor %}
  {% endfor %}
{% endif %}
