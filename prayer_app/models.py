from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import RegexValidator

class PrayerMember(models.Model):
    full_name = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class PrayerTimeSlot(models.Model):
    HOUR_CHOICES = [
        ('00:00', '12:00 AM - 1:00 AM'),
        ('01:00', '1:00 AM - 2:00 AM'),
        ('02:00', '2:00 AM - 3:00 AM'),
        ('03:00', '3:00 AM - 4:00 AM'),
        ('04:00', '4:00 AM - 5:00 AM'),
        ('05:00', '5:00 AM - 6:00 AM'),
        ('06:00', '6:00 AM - 7:00 AM'),
        ('07:00', '7:00 AM - 8:00 AM'),
        ('08:00', '8:00 AM - 9:00 AM'),
        ('09:00', '9:00 AM - 10:00 AM'),
        ('10:00', '10:00 AM - 11:00 AM'),
        ('11:00', '11:00 AM - 12:00 PM'),
        ('12:00', '12:00 PM - 1:00 PM'),
        ('13:00', '1:00 PM - 2:00 PM'),
        ('14:00', '2:00 PM - 3:00 PM'),
        ('15:00', '3:00 PM - 4:00 PM'),
        ('16:00', '4:00 PM - 5:00 PM'),
        ('17:00', '5:00 PM - 6:00 PM'),
        ('18:00', '6:00 PM - 7:00 PM'),
        ('19:00', '7:00 PM - 8:00 PM'),
        ('20:00', '8:00 PM - 9:00 PM'),
        ('21:00', '9:00 PM - 10:00 PM'),
        ('22:00', '10:00 PM - 11:00 PM'),
        ('23:00', '11:00 PM - 12:00 AM'),
    ]

    member = models.ForeignKey(PrayerMember, on_delete=models.CASCADE)
    prayer_time = models.CharField(max_length=5, choices=HOUR_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'prayer_time')

    def __str__(self):
        return f"{self.member.full_name} - {self.get_prayer_time_display()}"