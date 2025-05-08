import json
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Organization
from .forms import EventForm, UploadFileForm, OrganizationForm
from django.views.decorators.http import require_GET
from openpyxl import load_workbook

@login_required
def home(request):
    events = Event.objects.all()
    organizations = Organization.objects.all()
    events_json = [
        {
            'name': event.name,
            'date': event.start_datetime.strftime('%Y-%m-%d'),
            'time': event.start_datetime.strftime('%H:%M'),
            'location': event.location,
            'description': event.description,
            'type': event.event_type,
            'organization': event.organization.name,

        }
        for event in events
    ]

    if not request.user.is_authenticated:
        return redirect('login')

    # Role-based access control
    if request.user.role:
        return render(request, 'core/dashboard.html', {
        "events_json": json.dumps(events_json, cls=DjangoJSONEncoder),
        'user_role': str(request.user.role).title(),
        'organizations': organizations
    })
    else:
        return HttpResponseForbidden("You do not have permission to access this page.")  # Handle unknown roles
    
    
# View to display the dashboard calendar
@login_required
def dashboard(request):
    events = Event.objects.all()
    events_json = [
        {
            'name': event.name,
            'date': event.start_datetime.strftime('%Y-%m-%d'),
            'time': event.start_datetime.strftime('%H:%M'),
            'location': event.location,
            'description': event.description
        }
        for event in events
    ]
    print(events_json)
    return render(request, 'core/events.html', {
        "events_json": json.dumps(events_json, cls=DjangoJSONEncoder),
        'user_role': str(request.user.role).title(),
    })

# View to create a new event
@login_required
def add_event(request):
    print(request.method)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            form.save_m2m()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('events_list')
        else:
            print(form.errors)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('core/partials/event_form.html', {'form': form}, request=request)
                return JsonResponse({'success': False, 'html': html})

    form = EventForm()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('core/partials/event_form.html', {'form': form}, request=request)
        return JsonResponse({'html': html})

    return render(request, 'core/events.html', {'form': form})

@login_required
def events_list(request, organization_id=None):
    organizations = Organization.objects.all()
    events = Event.objects.all()
    print(organizations)

    if organization_id:
        events = events.filter(organization_id=organization_id)
        selected_organization_id = organization_id
    else:
        selected_organization_id = None

    return render(request, 'core/events.html', {
        'events': events,
        'organizations': organizations,
        'selected_organization_id': selected_organization_id,
        'user_role': str(request.user.role).title(),
    })







def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the user is the host of the event
    if request.user != event.host:
        messages.error(request, "You do not have permission to delete this event.")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX request
            return JsonResponse({'error': 'Permission Denied'}, status=403)
        return redirect('events_list')

    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully.")
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX request
            return JsonResponse({'message': 'Event deleted successfully.', 'redirect_url': '/events/'})  # Redirect URL after delete

    # If the request is AJAX, return the delete modal HTML
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX request
        html = render(request, 'core/partials/delete_event_modal.html', {'event': event}).content.decode('utf-8')
        return JsonResponse({'html': html})

    return redirect('events_list')




def view_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('core/partials/view_event_modal.html', {'event': event})
        return HttpResponse(html)
    
    return render(request, 'core/events.html', {'event': event})

def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        print(form)
        if form.is_valid():
            print("hello")
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Event updated successfully'})
            return redirect('events_list')
    
    else:
        form = EventForm(instance=event)
    return render(request, 'core/partials/edit_event_modal.html', {'form': form, 'event': event})

# events/views.py


def add_organization(request):
    if request.method == 'POST':
        print('POST')
        form = OrganizationForm(request.POST)
        if form.is_valid():
            print('valid')
            form.save()
            return redirect('events_list')  # Change to your preferred redirect
    else:
        form = OrganizationForm()

    return render(request, 'core/partials/add_org_modal.html', {'form': form})



@require_GET
@login_required
def get_events_by_month(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    if not month or not year:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    events = Event.objects.filter(start_datetime__year=year, start_datetime__month=month)
    data = {}
    for event in events:
        org = event.organization.acronym
        if org not in data:
            data[org] = []
        data[org].append({
            'name': event.name,
            'date': event.start_datetime.strftime('%m.%d.%y'),
            'description': event.description,
            'location': event.location,
            'type': event.event_type,
        })

    return JsonResponse({'events_by_org': data})


def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            organization_file = request.FILES.get('organization_file')
            event_file = request.FILES.get('event_file')

            if organization_file:
                wb = load_workbook(organization_file)
                sheet = wb.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    Organization.objects.create(name=row[0], acronym=row[1], description=row[2])

            if event_file:
                wb = load_workbook(event_file)
                sheet = wb.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    organization_acronym = row[0]
                    organization = Organization.objects.get(acronym=organization_acronym,)
                    print(organization.id)
                    print(row[1], row[2], row[3], row[4], row[5], row[6])
                    name = row[1].replace("'","").replace("`","")

                    Event.objects.create(organization_id=organization.id, name=name, description=row[2], location=row[3], start_datetime=row[4], end_datetime=row[5], event_type=row[6], host=request.user)

            return redirect('events_list')
    else:
        form = UploadFileForm()

    return render(request, 'core/partials/upload_file.html', {
        'form': form,
        'user_role': str(request.user.role).title(),})
