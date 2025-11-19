from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PrayerMember, PrayerTimeSlot

@admin.register(PrayerMember)
class PrayerMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'created_at']
    search_fields = ['full_name', 'phone_number']
    list_filter = ['created_at']

@admin.register(PrayerTimeSlot)
class PrayerTimeSlotAdmin(admin.ModelAdmin):
    list_display = ['member', 'prayer_time', 'submitted_at']
    list_filter = ['prayer_time', 'submitted_at']
    search_fields = ['member__full_name']
    ordering = ['prayer_time', 'member__full_name']