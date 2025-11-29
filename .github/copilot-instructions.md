## 🏗️ Project Overview

Movezz is a **Django-based social media platform** for sports enthusiasts, developed as part of the **Pemrograman Berbasis Platform (PBP)** course.  
It consists of multiple Django apps (modules) that handle different social features such as Feeds, Profiles, Messaging, Marketplace, Broadcast, and Authentication.

The project emphasizes:

- **Modular Django architecture**
- **Clean, readable, and  maintainable code**
- **Consistency across modules**

---

## 🧩 Django Module Structure

| Module                | Purpose                           |
| --------------------- | --------------------------------- |
| `feeds_module/`       | Timeline and post sharing         |
| `profile_module/`     | User profiles and connections     |
| `message_module/`     | Chat and messaging                |
| `marketplace_module/` | Sports goods marketplace          |
| `broadcast_module/`   | Public sports event announcements |
| `auth_module/`        | Registration and authentication   |
| `common/`             | Shared utilities and base logic   |

> Each module should remain self-contained, reusable, and communicate via Django models and URLs.

---

## ⚙️ General Coding Style

- Follow **PEP8** and **Django best practices**.
- Use **type hints** for all Python functions.
- Use **docstrings** for every class, function, and model.
- Prefer **function based view (fbv)**.
- Each model must define:
  - `Meta` class for table naming.
  - `__str__` method for readability.
  - Proper `related_name` for relationships.

Example:

```python
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    sport_type = models.CharField(max_length=50, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.sport_type}"
```

---


## 🧑‍💻 Django Best Practices

- Avoid writing business logic in `views.py`; use helper or service layers.
- Group similar functions in dedicated files (`utils.py`, `services.py`, `selectors.py`).
- Use `forms.py` for HTML forms and validation logic.
- Organize templates under each module (`templates/<module_name>/`).

---

## 💬 Comment & Prompt Style for Copilot

When prompting Copilot, use clear contextual comments.

**Example 1 — Model**

```python
# Create a Django model for a user's sports post with image and caption support
```

**Example 2 — View**

```python
# Implement a class-based view to list all posts from followed users
```

**Example 3 — Serializer (if using DRF)**

```python
# Write a serializer for Post that includes username and profile image
```

**Example 4 — Test**

```python
# Write a Django TestCase to verify that posts appear in correct order
```

---

## 🧪 Testing Conventions

- Use Django’s built-in `TestCase`.
- Include at least:

  - One test per model
  - One test per view

- Test both **success** and **failure** cases.

Example:

```python
from django.test import TestCase
from feeds_module.models import Post, User

class PostModelTests(TestCase):
    def test_str_method(self):
        user = User.objects.create(username="name")
        post = Post.objects.create(user=user, content="Morning run!", sport_type="Running")
        self.assertIn("Running", str(post))
```

---

## 🧰 Utilities & Helpers

- Use `common/` for shared utilities.
- Keep utility functions pure and reusable.
- Avoid circular imports between modules.

---

## 🌍 Environment & Deployment

- Use `.env` for local configuration and `.env.production` for deployment.
- Always use environment variables for credentials and API keys.
- For CI/CD, configure builds in `.github/workflows/deploy.yml`.

---

## 🧠 Copilot Context Tips

To improve Copilot predictions:

1. Keep this file **open** in VS Code while coding.
2. Write meaningful comments before typing code.
3. Use consistent function and variable names across modules.
4. Open multiple related files (e.g. `models.py`, `views.py`, and `urls.py`) — Copilot uses open tabs as context.

---

## 🪶 Example Directory Summary

```
movezz/
├── auth_module/
├── broadcast_module/
├── common/
├── feeds_module/
├── marketplace_module/
├── message_module/
├── profile_module/
├── static/
├── templates/
└── movezz/  # main settings and URL routing
```

---

## 💡 Additional Notes for Copilot

- Prefer **Tailwind CSS classes** when generating HTML templates.
- When suggesting JavaScript snippets, keep them minimal and integrated with Django templates.
- Avoid writing business logic in templates.
- Generate secure and maintainable code — no hardcoded secrets or credentials.


---

## 🎨 Styling & Frontend Guidelines

### 🧩 Frameworks Used

* **TailwindCSS v4** (via CDN)
* **DaisyUI v5** for UI components
* **Lucide Icons** for consistent icons
* **Google Fonts (Lato)** for typography

### 🧱 Base HTML Template

All pages extend a base layout similar to:

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    {% block meta %}{% endblock meta %}
    <title>Movezz</title>

    <!-- Tailwind CSS -->
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>

    <!-- DaisyUI -->
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5/themes.css" rel="stylesheet" />

    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>

    <!-- Lato Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Lato:wght@100;300;400;700;900&display=swap"
      rel="stylesheet"
    />

    <!-- Global CSS -->
    <link rel="stylesheet" href="{% static 'css/global.css' %}" />
  </head>
  <body class="flex flex-col min-h-screen bg-base-200 text-base-content transition-all duration-300">
    {% include "navbar.html" %}
    <main class="flex-1 w-full px-4 sm:px-6 lg:px-8 py-6">
      <div class="max-w-7xl mx-auto">{% block content %}{% endblock %}</div>
    </main>
  </body>
</html>
```

### 🌈 TailwindCSS Theme

* Defined in `static/css/global.css` using DaisyUI’s `@plugin "daisyui/theme"` syntax.
* The default theme uses **light mode** with a neutral color palette.
* Colors defined in OKLCH format for consistent tone and contrast.
* Use **DaisyUI components** (`btn`, `card`, `input`, `navbar`, etc.) whenever possible.
* Prefer **utility-first** Tailwind classes for layout and spacing (`flex`, `grid`, `gap`, `px`, `py`).

Example components:

```html
<!-- Button -->
<button class="btn btn-primary">Post</button>

<!-- Card -->
<div class="card bg-base-100 shadow-md">
  <div class="card-body">
    <h2 class="card-title">New Activity</h2>
    <p>Join your friends in a 5K run this weekend!</p>
  </div>
</div>
```

### 🖋️ Typography

* Use **Lato** across all components.
* Font weights (`lato-regular`, `lato-bold`, etc.) defined in `global.css`.
* Keep text sizes responsive using Tailwind’s `text-*` utilities.

Example:

```html
<h1 class="text-2xl font-bold lato-bold text-primary">Welcome back, Aldo!</h1>
```

### 📐 Layout & Responsiveness

* Use responsive design utilities (`sm:`, `md:`, `lg:`).
* Maximum container width: `max-w-7xl mx-auto`.
* Apply spacing consistently with `px-4 sm:px-6 lg:px-8`.
* Use `flex` or `grid` for layout alignment.

### 🪄 Animation & Interaction

* Use Tailwind transitions (`transition-all duration-300`) for smooth UI.
* Use `hover:` states for interactivity.
* Avoid heavy JavaScript — prefer pure CSS or lightweight AlpineJS if needed.

---


## 🧭 Final Notes for Copilot

* Always use **Tailwind v4 + DaisyUI v5 syntax**.
* Avoid inline styles — use utility classes.
* Use **semantic HTML** and **Django templating** (`{% block %}`, `{% include %}`).
* Prefer lightweight, elegant UI consistent with Movezz’s minimalist aesthetic.


---

✨ _These instructions are meant to guide GitHub Copilot to maintain consistency, readability, and Django best practices across the Movezz codebase._
