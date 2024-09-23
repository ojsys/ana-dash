from django import forms
from .models import CustomUser, Farmer, Partner, Event, ExtensionAgent, Dissemination
from django.contrib.auth.forms import UserCreationForm


class SimpleSignupForm(UserCreationForm):
    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        
    ]
    
    COUNTRY_CHOICES = [
        ('', 'Select a Country'),
        ('NG', 'Nigeria'),
        ('TZ', 'Tanzania'),
        ('GH', 'Ghana'),
        # Add more countries as needed
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('email','firstname', 'lastname', 'gender', 'organization', 'country', 'state', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'class': 'form-control'})

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if gender == '':
            raise forms.ValidationError("Please select a gender.")
        return gender

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if country == '':
            raise forms.ValidationError("Please select a country.")
        return country




class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['partner', 'firstname', 'lastname', 'gender', 'phone_no', 'own_phone', 
                  'crops', 'crops_other', 'farm_area', 'area_unit', 'cassava', 'yam', 
                  'maize', 'rice', 'sorghum']
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')]),
            'own_phone': forms.CheckboxInput(),
            'cassava': forms.CheckboxInput(),
            'yam': forms.CheckboxInput(),
            'maize': forms.CheckboxInput(),
            'rice': forms.CheckboxInput(),
            'sorghum': forms.CheckboxInput(),
        }

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'country', 'partnerfull', 'sector', 'partner_type', 'vc_segmain', 
                  'vc_segs', 'integrated', 'mel_data', 'input_supply', 'production', 
                  'digital_services', 'marketing_processing', 'financial_services', 
                  'research', 'policy_regulation']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['partner', 'firstname', 'lastname', 'designation', 'gender', 'phone_no', 
                  'country', 'event', 'hasc1', 'hasc2', 'city', 'venue', 'lat', 'lon', 
                  'startdate', 'enddate', 'usecase', 'format', 'titlefull', 'title', 'topics']
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')]),
            'startdate': forms.DateInput(attrs={'type': 'date'}),
            'enddate': forms.DateInput(attrs={'type': 'date'}),
        }

class ExtensionAgentForm(forms.ModelForm):
    class Meta:
        model = ExtensionAgent
        fields = ['user', 'phone_no', 'phone_no2', 'whatsapp', 'age', 'education', 
                  'designation', 'type_org', 'org', 'area_level', 'hasc1', 'hasc2', 
                  'no_farmers', 'certified', 'use_case', 'format', 'tools']
        widgets = {
            'whatsapp': forms.CheckboxInput(),
            'certified': forms.CheckboxInput(),
        }

class DisseminationForm(forms.ModelForm):
    class Meta:
        model = Dissemination
        fields = ['firstNameEN', 'surNameEN', 'phoneNrEN', 'country', 'city', 'orgEN', 
                  'partner', 'event', 'title', 'startdate', 'participant_list', 
                  'farmers_M', 'farmers_F']
        widgets = {
            'startdate': forms.DateInput(attrs={'type': 'date'}),
            'participant_list': forms.CheckboxInput(),
        }