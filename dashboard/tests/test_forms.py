from django.test import TestCase
from dashboard.forms import FarmerCreationForm, NewExtensionAgentForm

class FarmerFormTest(TestCase):
    def test_farmer_form_valid(self):
        form_data = {
            'firstname': 'Jane',
            'lastname': 'Doe',
            'gender': 'Female',
            'phone_no': '1234567890',
            'partner': 1,  # Assuming a partner with id 1 exists
        }
        form = FarmerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_farmer_form_invalid(self):
        form_data = {
            'firstname': '',  # Empty firstname should make the form invalid
            'lastname': 'Doe',
            'gender': 'Female',
            'phone_no': '1234567890',
            'partner': 1,
        }
        form = FarmerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
