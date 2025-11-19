from django import forms
from django.core.exceptions import ValidationError
from .models import PrayerMember, PrayerTimeSlot

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = PrayerMember
        fields = ['full_name', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number (e.g., +1234567890)'
            }),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if PrayerMember.objects.filter(phone_number=phone_number).exists():
            raise ValidationError(
                'This phone number is already registered. Each person can only register once.'
            )
        return phone_number

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if PrayerMember.objects.filter(full_name__iexact=full_name).exists():
            raise ValidationError(
                'This name is already registered. Each person can only register once.'
            )
        return full_name

class TimeSelectionForm(forms.ModelForm):
    class Meta:
        model = PrayerTimeSlot
        fields = ['prayer_time']
        widgets = {
            'prayer_time': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        member = kwargs.pop('member', None)
        super().__init__(*args, **kwargs)
        
        if member:
            # Get already selected times for this member
            selected_times = PrayerTimeSlot.objects.filter(member=member).values_list('prayer_time', flat=True)
            # Filter out already selected times
            available_choices = [choice for choice in PrayerTimeSlot.HOUR_CHOICES if choice[0] not in selected_times]
            self.fields['prayer_time'].choices = available_choices