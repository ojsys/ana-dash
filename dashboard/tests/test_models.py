from django.test import TestCase
from dashboard.models import Farmer, Partner, Event, ExtensionAgent

class FarmerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Partner.objects.create(name="Test Partner")
        Farmer.objects.create(
            firstname="John",
            lastname="Doe",
            gender="Male",
            phone_no="1234567890",
            partner=Partner.objects.first()
        )

    def test_farmer_creation(self):
        farmer = Farmer.objects.get(id=1)
        self.assertEqual(farmer.firstname, "John")
        self.assertEqual(farmer.lastname, "Doe")
        self.assertEqual(str(farmer), "John Doe")

class PartnerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Partner.objects.create(name="Test Partner", country="Nigeria")

    def test_partner_creation(self):
        partner = Partner.objects.get(id=1)
        self.assertEqual(partner.name, "Test Partner")
        self.assertEqual(partner.country, "Nigeria")
        self.assertEqual(str(partner), "Test Partner")