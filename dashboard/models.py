from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

GENDER_CHOICES = [
    ('Male','Male'),
    ('Female','Female'),
]

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    organization = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def __str__(self):
        return self.email

    

class Partner(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    partnerfull = models.CharField(max_length=100, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    partner_type = models.CharField(max_length=100, blank=True)
    vc_segmain = models.CharField(max_length=100, blank=True)
    vc_segs = models.CharField(max_length=100, blank=True)
    integrated = models.BooleanField(default=True, null=True)
    mel_data = models.BooleanField(default=False, null=True)
    input_supply = models.BooleanField(default=False, null=True)
    production = models.BooleanField(default=False, null=True)
    digital_services = models.BooleanField(default=False, null=True)
    marketing_processing = models.BooleanField(default=False, null=True)
    financial_services = models.BooleanField(default=False, null=True)
    research = models.BooleanField(default=False, null=True)
    policy_regulation = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name

class Farmer(models.Model):
    partner = models.CharField(max_length=100, null=True, blank=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    own_phone = models.BooleanField(default=False, null=True, blank=True)
    crops = models.CharField(max_length=50, blank=True, null=True)
    crops_other = models.CharField(max_length=50, blank=True, null=True)
    farm_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    area_unit = models.CharField(max_length=50, blank=True, null=True)
    cassava = models.BooleanField(default=False, null=True, blank=True)
    yam = models.BooleanField(default=False, null=True, blank=True)
    maize = models.BooleanField(default=False, null=True, blank=True)
    rice = models.BooleanField(default=False, null=True, blank=True)
    sorghum = models.BooleanField(default=False, null=True, blank=True)
    index = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class ExtensionAgent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=20)
    phone_no2 = models.CharField(max_length=20, blank=True)
    whatsapp = models.BooleanField(default=False)
    age = models.IntegerField(null=True)
    education = models.CharField(max_length=100, null=True)
    designation = models.CharField(max_length=100)
    type_org = models.CharField(max_length=100)
    org = models.ForeignKey(Partner, on_delete=models.CASCADE)
    area_level = models.IntegerField(null=True)
    hasc1 = models.CharField(max_length=120, null=True)
    hasc2 = models.CharField(max_length=120, null=True)
    no_farmers = models.IntegerField(null=True)
    date_added = models.DateField(auto_now_add=True)
    certified = models.BooleanField(default=False)
    use_case = models.CharField(max_length=100, blank=True)
    format = models.CharField(max_length=100, blank=True)
    tools = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname}"

class Event(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_no = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    event = models.CharField(max_length=100)
    hasc1 = models.CharField(max_length=120, null=True)
    hasc2 = models.CharField(max_length=120, null=True)
    city = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    lat = models.CharField(max_length=100, null=True)
    lon = models.CharField(max_length=100, null=True)
    date_added = models.DateField(auto_now_add=True)
    startdate = models.DateField()
    enddate = models.DateField()
    usecase = models.CharField(max_length=50, blank=True)
    format = models.CharField(max_length=50, blank=True)
    titlefull = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    topics = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.title} - {self.startdate}"

class Dissemination(models.Model):
    today = models.DateTimeField(auto_now_add=True)
    firstNameEN = models.CharField(max_length=255, blank=True)
    surNameEN = models.CharField(max_length=255, blank=True)
    phoneNrEN = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    orgEN = models.CharField(max_length=255, blank=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.TextField(blank=True)
    startdate = models.DateField()
    participant_list = models.BooleanField(default=False)
    farmers_M = models.IntegerField(default=0)
    farmers_F = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.event} - {self.startdate}"