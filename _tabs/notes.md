---
title: Notes
layout: page
icon: fas fa-book
order: 4
---

## Cybersecurity Notes Knowledge Base

{% if site.notes == null or site.notes.size == 0 %}
  *No notes yet. Check back later!*
{% else %}
  {% assign all_notes = site.notes | sort: "order" %}
  {% assign categories = all_notes | map: "category" | uniq | sort %}
  {% for cat in categories %}

### {{ cat }}

  {% assign cat_notes = all_notes | where: "category", cat %}
  {% for note in cat_notes %}
- [{{ note.title }}]({{ note.url }})
  {% endfor %}
  {% endfor %}
{% endif %}
