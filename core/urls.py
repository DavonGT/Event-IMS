from django.urls import path
from . import views
from django.shortcuts import redirect


urlpatterns = [
    path('', views.home, name='home'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('add-event/', views.add_event, name='add_event'),
    path('events_list/', views.events_list, name='events_list'),



    path('admin-dashboard/', views.home, name='admin_dashboard'),
    path('organizer-dashboard/', views.home, name='organizer_dashboard'),
    path('student-dashboard/', views.home, name='student_dashboard'),
    path('logout/', lambda request: redirect('login'), name='logout'),
]
