# Iris

![Latest Version](https://img.shields.io/pypi/v/iris-templates)
![Downloads](https://img.shields.io/pypi/dm/iris-templates)
![Status](https://img.shields.io/badge/status-alpha-orange)
![License: CC BY-ND 4.0](https://img.shields.io/badge/License-CC%20BY--ND%204.0-lightgrey.svg)

**Iris** is a modern, lightweight Python template engine designed for simplicity, flexibility, and performance. With advanced directive processing, includes, and dynamic context evaluation, Iris provides developers with a seamless way to render dynamic templates efficiently.

---

## 🚀 Key Features

- **Advanced Directives**: Includes support for custom template directives like `@extends`, `@include`, and control structures.
- **Dynamic Context Injection**: Easily pass and process dynamic data into your templates.
- **Flexible Templating**: Supports layout inheritance, template composition, and reusable components.
- **Fast and Lightweight**: Minimal overhead with high performance, designed for Python applications.
- **Safe Evaluation**: Includes built-in safeguards for variable evaluation to ensure template safety.
- **Open for Personal & Commercial Use**: Use Iris freely in personal and commercial projects (not for resale as a standalone product).

---

## 🛠️ How to Use Iris

### Step 1: Install Iris

Install Iris via pip:

```bash
pip install iris-templates
```

### Step 2: Render Your First Template

Create a template file, e.g., `template.html`:

```html
@extends('base.html')

@section('title', 'Welcome to Iris')

@section('content')
    <h1>Hello, {{ user }}!</h1>
@endsection
```

Create a Python script to render the template:

```python
from iris import TemplateEngine

engine = TemplateEngine(template_dir="./templates")
output = engine.render("template.html", {"user": "Alice"})
print(output)
```

### Step 3: Explore More Features

Iris provides advanced features for layout inheritance, template inclusion, and custom directives. For example:

#### Including Other Templates

```html
@include('header.html')

<p>This is the body content.</p>

@include('footer.html')
```

#### Dynamic Control Structures

```html
@if(user.is_admin)
    <p>Welcome, Admin {{ user.name }}!</p>
@else
    <p>Welcome, {{ user.name }}!</p>
@endif
```

---

## 🔍 Project Status

![Issues Closed](https://img.shields.io/github/issues-closed/altxriainc/iris)
![Bug Issues](https://img.shields.io/github/issues/altxriainc/iris/bug)
![Enhancement Issues](https://img.shields.io/github/issues/altxriainc/iris/enhancement)

---

## 📜 License and Usage

Iris is free to use for both personal and commercial projects. However, Iris itself cannot be resold or distributed as a standalone product.

---

## 🤝 Contributors

Developed and maintained by **Altxria Inc.** with contributions from a growing community of passionate developers.

![Contributors](https://contrib.rocks/image?repo=altxriainc/iris)

[See All Contributors](https://github.com/altxriainc/iris/graphs/contributors)

---

## ❤️ Support Iris

If you find Iris useful, consider sponsoring us to support ongoing development and new features!

[![Sponsor Iris](https://img.shields.io/badge/Sponsor-Iris-blue?logo=github-sponsors)](https://github.com/sponsors/altxriainc)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N516SMZ6)
