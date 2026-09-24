# Django-Recaptcha3

A Django package providing seamless integration for Google reCAPTCHA v3 in forms and templates, with configurable score thresholds and bot protection.

---

## Installation

```bash
pip install git+https://github.com/djangomango/django-recaptcha3.git@0.1.0
```

Or add to your `requirements.txt`:

```txt
git+https://github.com/djangomango/django-recaptcha3.git@0.1.0
```

Add `django_recaptcha3` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "django_recaptcha3",
    ...
]
```

---

## Configuration

Configure your Google reCAPTCHA v3 keys in `settings.py`:

```python
GOOGLE_RECAPTCHA_IS_ACTIVE = True
GOOGLE_RECAPTCHA_SITE_KEY = "your-public-site-key"
GOOGLE_RECAPTCHA_SECRET_KEY = "your-private-secret-key"
GOOGLE_RECAPTCHA_DEFAULT_ACTION = "generic"
GOOGLE_RECAPTCHA_SCORE_THRESHOLD = 0.5
```

---

## Usage

### 1. Form & Widget

Add `ReCaptchaField` to your Django form:

```python
from django import forms
from django_recaptcha3 import ReCaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField(score_threshold=0.5)
```

In your view:

```python
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data["captcha"].get("score")
            # Process contact form...
```

### 2. Templates

Load the `recaptcha3` template tag library and initialize reCAPTCHA:

```html
{% load recaptcha3 %}
<html>
  <head>
    {% recaptcha_init %}
    {% recaptcha_ready action_name='contact' %}
  </head>
  <body>
    <form action="" method="post">
      {% csrf_token %}
      {{ form }}
      <button type="submit">Submit</button>
    </form>
  </body>
</html>
```

### 3. Disabling in Tests

Disable external API calls during unit tests by setting:

```python
GOOGLE_RECAPTCHA_IS_ACTIVE = False
```

---

## License

Licensed under the **GNU Lesser General Public License v2.1 (LGPLv2.1)**.
