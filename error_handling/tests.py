from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse

from .views import custom_404_handler, custom_500_handler


class ErrorHandlingViewTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_custom_404_handler_redirects_to_error_page(self):
        request = self.factory.get('/missing-page/')
        response = custom_404_handler(request, exception=Exception('missing'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/error-handling/404/')

    def test_custom_500_handler_redirects_to_error_page(self):
        request = self.factory.get('/broken-page/')
        response = custom_500_handler(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/error-handling/500/')
