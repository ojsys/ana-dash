from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from dashboard.models import Farmer, Partner

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        Partner.objects.create(name="Test Partner")
        Farmer.objects.create(
            firstname="John",
            lastname="Doe",
            gender="Male",
            partner=Partner.objects.first()
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')
        self.assertContains(response, "John Doe")

    def test_dashboard_update_view(self):
        response = self.client.get(reverse('dashboard_update'), {'start_date': '2023-01-01', 'end_date': '2023-12-31'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'total_farmers': 1})