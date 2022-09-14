from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Patient'),
        (2, 'Doctor')
    )

    Profile_Picture = models.ImageField(upload_to='profiles/%Y/%m/%d')
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField(validators=[MinValueValidator(100000), MaxValueValidator(999999)],null=True)
    user_type = models.PositiveIntegerField(choices=USER_TYPE_CHOICES, default=1)

    def __str__(self):
        return f"{self.address}"

class Post(models.Model):
    CATEGORY_CHOICES = (
        (1, 'Mental Health'),
        (2, 'Heart Disease'),
        (3, 'Covid19'),
        (4, 'Immunization'),
    )

    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='posts/%Y/%m/%d')
    category = models.PositiveIntegerField(choices=CATEGORY_CHOICES, default=1)
    content = models.TextField()
    username = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.title}"

class Draft(models.Model):
    CATEGORY_CHOICES = (
        (1, 'Mental Health'),
        (2, 'Heart Disease'),
        (3, 'Covid19'),
        (4, 'Immunization'),
    )

    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='posts/%Y/%m/%d')
    category = models.PositiveIntegerField(choices=CATEGORY_CHOICES, default=1)
    content = models.TextField()
    username = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.title}"

class bookappointment(models.Model):
    doctor_name = models.CharField(max_length=100)
    required_specification = models.CharField(max_length=500)
    appointment_date = models.DateField()
    appointment_start_time = models.TimeField()
    appointment_end_time = models.TimeField()
    username = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.appointment_start_time}"
