import json
import os
import mock

from django.forms import Form
from django.test import TestCase, override_settings

from .fields import ReCaptchaField
from .widgets import ReCaptchaHiddenInput


class RecaptchaTestForm(Form):
    recaptcha = ReCaptchaField(widget=ReCaptchaHiddenInput())


class TestRecaptchaForm(TestCase):

    @override_settings(GOOGLE_RECAPTCHA_IS_ACTIVE=False)
    def test_dummy_validation(self):
        # form should validate without a 'g-recaptcha-response'
        form = RecaptchaTestForm({})
        s = self.assertTrue(form.is_valid())
        # NOTE: no mocked response is returned
        self.assertEqual(form.cleaned_data['recaptcha'], {})
        del os.environ['GOOGLE_RECAPTCHA_IS_ACTIVE']

    @mock.patch('requests.post')
    def test_validate_error_invalid_token(self, requests_post):

        recaptcha_response = {'success': False}
        requests_post.return_value.json = lambda: recaptcha_response

        form = RecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertFalse(form.is_valid())

    @mock.patch('requests.post')
    def test_validate_error_lower_score(self, requests_post):

        recaptcha_response = {
            'success': True,
            'score': 0.5
        }
        requests_post.return_value.json = lambda: recaptcha_response

        class RecaptchaTestForm(Form):
            recaptcha = ReCaptchaField(score_threshold=0.7)
        form = RecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['recaptcha'][0], 'reCaptcha score is too low. score: 0.5')

    @mock.patch('requests.post')
    def test_validate_success_higher_score(self, requests_post):
        recaptcha_response = {
            'success': True,
            'score': 0.7,
            'hostname': 'example.com',
            'action': 'click'
        }
        requests_post.return_value.json = lambda: recaptcha_response

        class RecaptchaTestForm(Form):
            recaptcha = ReCaptchaField(score_threshold=0.4)

        form = RecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['recaptcha'].get('score'), 0.7)
        self.assertEqual(form.cleaned_data['recaptcha'].get('hostname'), 'example.com')
        self.assertEqual(form.cleaned_data['recaptcha'].get('action'), 'click')

    @mock.patch('requests.post')
    def test_settings_score_threshold(self, requests_post):
        recaptcha_response = {
            'success': True,
            'score': 0.6
        }
        requests_post.return_value.json = lambda: recaptcha_response

        class RecaptchaTestForm(Form):
            recaptcha = ReCaptchaField()
        form = RecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertTrue(form.is_valid())

    @mock.patch('requests.post')
    @override_settings(GOOGLE_RECAPTCHA_SCORE_THRESHOLD=0.7)
    def test_settings_score_threshold_override_fields(self, requests_post):
        recaptcha_response = {
            'success': True,
            'score': 0.6
        }
        requests_post.return_value.json = lambda: recaptcha_response

        class RecaptchaTestForm(Form):
            recaptcha = ReCaptchaField()

        form = RecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertFalse(form.is_valid())

    @mock.patch('requests.post')
    @override_settings(GOOGLE_RECAPTCHA_SCORE_THRESHOLD=0.7)
    def test_settings_score_threshold_override_each_fields(self, requests_post):
        recaptcha_response = {
            'success': True,
            'score': 0.4
        }
        requests_post.return_value.json = lambda: recaptcha_response

        class RecaptchaTestForm(Form):
            recaptcha = ReCaptchaField()

        class RecaptchaOverrideTestForm(Form):
            recaptcha = ReCaptchaField(score_threshold=0.3)

        form1 = RecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertFalse(form1.is_valid())

        form2 = RecaptchaOverrideTestForm({"g-recaptcha-response": "dummy token"})
        self.assertTrue(form2.is_valid())

    @mock.patch('requests.post')
    def test_validate_success(self, requests_post):
        recaptcha_response = {
            'success': True,
            'score': 0.5
        }
        requests_post.return_value.json = lambda: recaptcha_response

        form = RecaptchaTestForm({"g-recaptcha-response": "dummy token"})
        self.assertTrue(form.is_valid())
