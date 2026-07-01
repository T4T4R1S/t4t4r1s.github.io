---
title: Notes
layout: page
icon: fas fa-book
order: 4
---

## Cybersecurity Notes Knowledge Base

{% if site.categories.Notes == null or site.categories.Notes.size == 0 %}
  *No notes yet. Check back later!*
{% else %}
  {% assign all_notes = site.categories.Notes | sort: "order" %}
  {% assign subcategories = "" | split: "" %}
  {% for note in all_notes %}
    {% assign subcat = note.categories[1] %}
    {% if subcat %}
      {% assign subcategories = subcategories | push: subcat %}
    {% endif %}
  {% endfor %}
  {% assign categories = subcategories | uniq | sort %}
  <div class="notes-accordion">
  {% for cat in categories %}
    <details class="notes-category">
      <summary class="notes-category-title">
        <span class="notes-category-name">{{ cat }}</span>
        <i class="fas fa-chevron-down notes-category-icon"></i>
      </summary>
      <ul class="notes-list">
        {% for note in all_notes %}
          {% if note.categories[1] == cat %}
            <li class="notes-item">
              <a href="{{ note.url }}">{{ note.title }}</a>
            </li>
          {% endif %}
        {% endfor %}
      </ul>
    </details>
  {% endfor %}
  </div>
{% endif %}
