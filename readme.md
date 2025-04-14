# TinyWebapp

**TinyWebapp** is a lightweight WebDriver-like interface that works on devices where traditional Selenium is unsupported. It provides a fast, resource-efficient alternative for interacting with web content through a custom Android APK or PC Java app.

---

## Features

- Works without needing Selenium
- Built-in Android APK and Java app support
- Lightweight and portable
- Ideal for automation on mobile or restricted environments

---

## Usage
from TinyWebapp import update_url, inject_js, current_url, get_progress, get_app, get_java

update_url("https://example.com")
inject_js("alert('Hello')")
print(current_url())
print(get_progress())
get_app("MyApp.apk")
get_java("MyApp.java")

---

## Installation

```bash
pip install TinyWebapp

