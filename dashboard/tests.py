from django.test import TestCase
from django.urls import reverse
from .models import Farmer, Partner

class DashboardTestCase(TestCase):
    def setUp(self):
        Partner.objects.create(name="Test Partner")
        Farmer.objects.create(firstname="John", lastname="Doe", partner=Partner.objects.first())

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Partner")
        self.assertContains(response, "John Doe")