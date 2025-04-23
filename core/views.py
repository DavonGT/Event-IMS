from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect unauthenticated users to the login page

    # Role-based access control
    if request.user.role == 'admin':
        return render(request, 'core/home.html', {'user_role': 'Admin'})
    elif request.user.role == 'organizer':
        return render(request, 'core/home.html', {'user_role': 'Organizer'})
    elif request.user.role == 'student':
        return render(request, 'core/home.html', {'user_role': 'Student'})
    else:
        return HttpResponseForbidden("You do not have permission to access this page.")  # Handle unknown roles