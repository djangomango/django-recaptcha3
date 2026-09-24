from typing import Any

from django.forms.widgets import Input


class ReCaptchaHiddenInput(Input):
    """Hidden input widget capturing Google reCAPTCHA client token response."""

    input_type = "hidden"
    template_name = "recaptcha_hidden_input.html"

    def value_from_datadict(
        self, data: dict[str, Any], files: Any, name: str
    ) -> list[str | None]:
        """Extract reCAPTCHA response token from submitted form data."""
        return [data.get("g-recaptcha-response", None)]
