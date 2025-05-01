from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Event, Organization
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
        print(form)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            form.save_m2m()
            return redirect('events_list')
    else:
        form = EventForm()

    return render(request, 'core/add_event.html', {'form': form})


@login_required
def events_list(request, organization_id=None):
    organizations = Organization.objects.all()
    events = Event.objects.all()

    if organization_id:
        events = events.filter(organization_id=organization_id)
        selected_organization_id = organization_id
    else:
        selected_organization_id = None

    return render(request, 'core/events.html', {
        'events': events,
        'organizations': organizations,
        'selected_organization_id': selected_organization_id,
    })

def view_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'core/view_event.html', {'event': event})

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('events_list')

def edit_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'core/edit_event.html', {'form': form})
