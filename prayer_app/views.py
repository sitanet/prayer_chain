from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from .models import PrayerMember, PrayerTimeSlot
from .forms import RegistrationForm, TimeSelectionForm

def register_view(request):
    # Check if user already has an active session
    member_id = request.session.get('member_id')
    if member_id:
        try:
            member = PrayerMember.objects.get(id=member_id)
            messages.info(request, f'You are already registered as {member.full_name}. You can select additional prayer times.')
            return redirect('select_time')
        except PrayerMember.DoesNotExist:
            # Clear invalid session
            del request.session['member_id']
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            member = form.save()
            request.session['member_id'] = member.id
            # Set session to expire when browser closes
            request.session.set_expiry(0)
            messages.success(request, 'Registration successful! Now select your prayer time.')
            return redirect('select_time')
    else:
        form = RegistrationForm()
    
    return render(request, 'prayer_app/register.html', {'form': form})

def select_time_view(request):
    member_id = request.session.get('member_id')
    if not member_id:
        messages.error(request, 'Please register first.')
        return redirect('register')
    
    member = get_object_or_404(PrayerMember, id=member_id)
    
    if request.method == 'POST':
        form = TimeSelectionForm(request.POST, member=member)
        if form.is_valid():
            time_slot = form.save(commit=False)
            time_slot.member = member
            time_slot.save()
            messages.success(request, 'Prayer time selected successfully!')
            return redirect('success')
    else:
        form = TimeSelectionForm(member=member)
    
    # Check if member has already selected all 24 hours
    selected_count = PrayerTimeSlot.objects.filter(member=member).count()
    can_select_more = selected_count < 24
    
    context = {
        'form': form,
        'member': member,
        'selected_count': selected_count,
        'can_select_more': can_select_more
    }
    
    return render(request, 'prayer_app/select_time.html', context)

def success_view(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('register')
    
    member = get_object_or_404(PrayerMember, id=member_id)
    selected_times = PrayerTimeSlot.objects.filter(member=member).order_by('prayer_time')
    
    context = {
        'member': member,
        'selected_times': selected_times
    }
    
    return render(request, 'prayer_app/success.html', context)

def report_view(request):
    # Create a structured data format for the template
    hour_choices = dict(PrayerTimeSlot.HOUR_CHOICES)
    prayer_schedule = []
    
    for time_value, time_display in PrayerTimeSlot.HOUR_CHOICES:
        # Get members for this specific time slot
        members = PrayerMember.objects.filter(
            prayertimeslot__prayer_time=time_value
        ).distinct()
        
        prayer_schedule.append({
            'time_value': time_value,
            'time_display': time_display,
            'members': members,
            'count': members.count()
        })
    
    # Get summary statistics
    total_members = PrayerMember.objects.count()
    total_commitments = PrayerTimeSlot.objects.count()
    covered_hours = PrayerTimeSlot.objects.values('prayer_time').distinct().count()
    
    context = {
        'prayer_schedule': prayer_schedule,
        'total_members': total_members,
        'total_commitments': total_commitments,
        'covered_hours': covered_hours,
        'hour_choices': hour_choices
    }
    
    return render(request, 'prayer_app/report.html', context)

def home_view(request):
    # Don't clear session data - let users continue where they left off
    member_id = request.session.get('member_id')
    if member_id:
        try:
            member = PrayerMember.objects.get(id=member_id)
            return redirect('select_time')
        except PrayerMember.DoesNotExist:
            del request.session['member_id']
    
    return redirect('register')

def new_registration_view(request):
    # Clear session and start fresh (admin use only)
    if 'member_id' in request.session:
        del request.session['member_id']
    messages.info(request, 'Starting new registration session.')
    return redirect('register')