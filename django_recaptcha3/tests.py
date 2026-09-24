import os
from unittest import mock

from django.forms import Form
from django.test import TestCase, override_settings

from .fields import ReCaptchaField
from .widgets import ReCaptchaHiddenInput


class RecaptchaTestForm(Form):
    """Test form for validating default reCAPTCHA field binding."""

    recaptcha = ReCaptchaField(widget=ReCaptchaHiddenInput())


class TestRecaptchaForm(TestCase):
    """Test suite verifying reCAPTCHA form validation logic and error handling."""

    @override_settings(GOOGLE_RECAPTCHA_IS_ACTIVE=False)
    def test_dummy_validation(self) -> None:
        """Verify form validates without token when reCAPTCHA is inactive."""
        form = RecaptchaTestForm({})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["recaptcha"], {})
        if "GOOGLE_RECAPTCHA_IS_ACTIVE" in os.environ:
            del os.environ["GOOGLE_RECAPTCHA_IS_ACTIVE"]

    @mock.patch("requests.post")
    def test_validate_error_invalid_token(self, requests_post: mock.MagicMock) -> None:
        """Verify validation failure when Google verification indicates invalid token."""
        recaptcha_response = {"success": False}
        requests_post.return_value.json = lambda: recaptcha_response

        form = RecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertFalse(form.is_valid())

    @mock.patch("requests.post")
    def test_validate_error_lower_score(self, requests_post: mock.MagicMock) -> None:
        """Verify validation failure when received score is beneath threshold."""
        recaptcha_response = {"success": True, "score": 0.5}
        requests_post.return_value.json = lambda: recaptcha_response

        class CustomRecaptchaTestForm(Form):
            """Custom test form with specific threshold."""

            recaptcha = ReCaptchaField(score_threshold=0.7)

        form = CustomRecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["recaptcha"][0], "reCaptcha score is too low. score: 0.5"
        )

    @mock.patch("requests.post")
    def test_validate_success_higher_score(self, requests_post: mock.MagicMock) -> None:
        """Verify validation success when received score meets threshold."""
        recaptcha_response = {
            "success": True,
            "score": 0.7,
            "hostname": "example.com",
            "action": "click",
        }
        requests_post.return_value.json = lambda: recaptcha_response

        class CustomRecaptchaTestForm(Form):
            """Custom test form with specific threshold."""

            recaptcha = ReCaptchaField(score_threshold=0.4)

        form = CustomRecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["recaptcha"].get("score"), 0.7)
        self.assertEqual(form.cleaned_data["recaptcha"].get("hostname"), "example.com")
        self.assertEqual(form.cleaned_data["recaptcha"].get("action"), "click")

    @mock.patch("requests.post")
    def test_settings_score_threshold(self, requests_post: mock.MagicMock) -> None:
        """Verify validation against default score threshold."""
        recaptcha_response = {"success": True, "score": 0.6}
        requests_post.return_value.json = lambda: recaptcha_response

        class CustomRecaptchaTestForm(Form):
            """Custom test form with default settings threshold."""

            recaptcha = ReCaptchaField()

        form = CustomRecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertTrue(form.is_valid())

    @mock.patch("requests.post")
    @override_settings(GOOGLE_RECAPTCHA_SCORE_THRESHOLD=0.7)
    def test_settings_score_threshold_override_fields(
        self, requests_post: mock.MagicMock
    ) -> None:
        """Verify setting override enforces higher threshold requirement."""
        recaptcha_response = {"success": True, "score": 0.6}
        requests_post.return_value.json = lambda: recaptcha_response

        class CustomRecaptchaTestForm(Form):
            """Custom test form under overridden threshold settings."""

            recaptcha = ReCaptchaField()

        form = CustomRecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertFalse(form.is_valid())

    @mock.patch("requests.post")
    @override_settings(GOOGLE_RECAPTCHA_SCORE_THRESHOLD=0.7)
    def test_settings_score_threshold_override_each_fields(
        self, requests_post: mock.MagicMock
    ) -> None:
        """Verify field-level threshold overrides global settings threshold."""
        recaptcha_response = {"success": True, "score": 0.4}
        requests_post.return_value.json = lambda: recaptcha_response

        class DefaultTestForm(Form):
            """Default test form under overridden threshold settings."""

            recaptcha = ReCaptchaField()

        class OverrideTestForm(Form):
            """Test form overriding threshold at field level."""

            recaptcha = ReCaptchaField(score_threshold=0.3)

        form1 = DefaultTestForm({"g-recaptcha-response": "dummy token"})
        self.assertFalse(form1.is_valid())

        form2 = OverrideTestForm({"g-recaptcha-response": "dummy token"})
        self.assertTrue(form2.is_valid())

    @mock.patch("requests.post")
    def test_validate_success(self, requests_post: mock.MagicMock) -> None:
        """Verify successful token validation flow."""
        recaptcha_response = {"success": True, "score": 0.5}
        requests_post.return_value.json = lambda: recaptcha_response

        form = RecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertTrue(form.is_valid())
