from typing import Any

from django import template
from django.conf import settings
from django.template.loader import get_template

register = template.Library()


def return_empty_context(*args: Any, **kwargs: Any) -> str:
    """Return empty string for inactive reCAPTCHA tag rendering."""
    return ""


@register.simple_tag
def recaptcha_key() -> str:
    """Return configured public Google reCAPTCHA site key."""
    return getattr(settings, "GOOGLE_RECAPTCHA_SITE_KEY", "")


def recaptcha_init(public_key: str | None = None) -> dict[str, Any]:
    """Build template context for initializing Google reCAPTCHA JavaScript API."""
    return {
        "public_key": public_key or getattr(settings, "GOOGLE_RECAPTCHA_SITE_KEY", ""),
        "language": getattr(settings, "GOOGLE_RECAPTCHA_LANGUAGE", None),
        "google_api_host": getattr(
            settings, "RECAPTCHA_FRONTEND_PROXY_HOST", "https://www.google.com"
        ),
    }


def recaptcha_ready(
    public_key: str | None = None,
    action_name: str | None = None,
    custom_callback: str | None = None,
) -> dict[str, Any]:
    """Build template context for executing reCAPTCHA when API is ready."""
    return {
        "public_key": public_key or getattr(settings, "GOOGLE_RECAPTCHA_SITE_KEY", ""),
        "action_name": action_name
        or getattr(settings, "GOOGLE_RECAPTCHA_DEFAULT_ACTION", "homepage"),
        "custom_callback": custom_callback,
    }


def recaptcha_execute(
    public_key: str | None = None,
    action_name: str | None = None,
    custom_callback: str | None = None,
) -> dict[str, Any]:
    """Build template context for programmatically triggering reCAPTCHA execution."""
    return {
        "public_key": public_key or getattr(settings, "GOOGLE_RECAPTCHA_SITE_KEY", ""),
        "action_name": action_name
        or getattr(settings, "GOOGLE_RECAPTCHA_DEFAULT_ACTION", "homepage"),
        "custom_callback": custom_callback,
    }


if getattr(settings, "GOOGLE_RECAPTCHA_IS_ACTIVE", False):
    register.inclusion_tag(get_template("recaptcha_init.html"))(recaptcha_init)
    register.inclusion_tag(get_template("recaptcha_ready.html"))(recaptcha_ready)
    register.inclusion_tag(get_template("recaptcha_execute.html"))(recaptcha_execute)
else:
    register.simple_tag(return_empty_context, name="recaptcha_init")
    register.simple_tag(return_empty_context, name="recaptcha_ready")
    register.simple_tag(return_empty_context, name="recaptcha_execute")
