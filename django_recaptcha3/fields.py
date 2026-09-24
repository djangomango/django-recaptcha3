import logging
from typing import Any

import requests
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .widgets import ReCaptchaHiddenInput

logger = logging.getLogger(__name__)


class ReCaptchaField(forms.CharField):
    """Form field validating Google reCAPTCHA v3 tokens against verify API."""

    def __init__(
        self, *args: Any, attrs: dict[str, Any] | None = None, **kwargs: Any
    ) -> None:
        self._is_active = kwargs.pop("is_active", None)
        self._secret_key = kwargs.pop("private_key", None)
        self._score_threshold = kwargs.pop("score_threshold", None)

        if "widget" not in kwargs:
            kwargs["widget"] = ReCaptchaHiddenInput()

        super().__init__(*args, **kwargs)

    @property
    def is_active(self) -> bool:
        """Return whether reCAPTCHA verification is active."""
        if self._is_active is not None:
            return self._is_active
        return getattr(settings, "GOOGLE_RECAPTCHA_IS_ACTIVE", True)

    @property
    def secret_key(self) -> str:
        """Return secret key from field argument or settings."""
        if self._secret_key is not None:
            return self._secret_key
        return getattr(settings, "GOOGLE_RECAPTCHA_SECRET_KEY", "")

    @property
    def score_threshold(self) -> float:
        """Return minimum passing score threshold."""
        if self._score_threshold is not None:
            return self._score_threshold
        return getattr(settings, "GOOGLE_RECAPTCHA_SCORE_THRESHOLD", 0.5)

    def clean(self, value: Any) -> Any:
        """Validate token with Google verification endpoint."""
        if not self.is_active:
            return {}

        token = value[0] if isinstance(value, list | tuple) and value else value
        response_token = super().clean(token)

        try:
            r = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                {
                    "secret": self.secret_key,
                    "response": response_token,
                },
                timeout=5,
            )
            r.raise_for_status()
        except requests.RequestException as e:
            logger.exception(e)
            raise ValidationError(
                _("Connection to reCaptcha server failed"),
                code="connection_failed",
            ) from e

        json_response = r.json()
        logger.debug(f"Received response from reCaptcha server: {json_response}")

        if bool(json_response.get("success")):
            score = json_response.get("score")
            if (
                self.score_threshold is not None
                and score is not None
                and self.score_threshold > score
            ):
                raise ValidationError(
                    _("reCaptcha score is too low. score: %(score)s"),
                    code="score",
                    params={"score": score},
                )
            return json_response

        error_codes = json_response.get("error-codes", [])
        if (
            "missing-input-secret" in error_codes
            or "invalid-input-secret" in error_codes
        ):
            logger.exception("Invalid reCaptcha secret key detected")
            raise ValidationError(
                _("Connection to reCaptcha server failed"),
                code="invalid_secret",
            )
        elif error_codes:
            raise ValidationError(
                _("reCaptcha invalid or expired, try again"),
                code="expired",
            )
        else:
            logger.exception("No error-codes received from Google reCaptcha server")
            raise ValidationError(
                _("reCaptcha response from Google not valid, try again"),
                code="invalid_response",
            )
