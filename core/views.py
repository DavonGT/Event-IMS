from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm
import json


@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Role-based access control
    if request.user.role == 'admin':
        return render(request, 'core/dashboard.html', {'user_role': 'Admin'})
    elif request.user.role == 'organizer':
        return render(request, 'core/dashboard.html', {'user_role': 'Organizer'})
    elif request.user.role == 'student':
        return render(request, 'core/dashboard.html', {'user_role': 'Student'})
    else:
        return HttpResponseForbidden("You do not have permission to access this page.")  # Handle unknown roles
    



# View to display the dashboard calendar
@login_required
def dashboard(request):
    events = Event.objects.all()
    events_json = json.dumps([
        {
            'name': event.name,
            'date': event.start_datetime.strftime('%Y-%m-%d'),
            'time': event.start_datetime.strftime('%H:%M'),
            'location': event.location,
            'description': event.description
        }
        for event in events
    ])
    return render(request, 'core/events.html', {
        'events_json': events_json,
    })


# View to create a new event
@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            form.save_m2m()
            return redirect('events')
    else:
        form = EventForm()

    return render(request, 'core/add_event.html', {'form': form})


@login_required
def events_list(request):
    events = Event.objects.all()
    return render(request, 'core/events.html', {'events': events})


