from django.urls import path
from . import views
from django.shortcuts import redirect


urlpatterns = [
    path('', views.home, name='home'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('add-event/', views.add_event, name='add_event'),
    path('events_list/<int:organization_id>/', views.events_list, name='events_list_filtered'),
    path('events_list/', views.events_list, name='events_list'),

    # path('view-event/<int:event_id>/', views.view_event, name='view_event'),
    # path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    # path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),


    path('events/<int:event_id>/view/', views.view_event, name='view_event'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('organizations/add/', views.add_organization, name='add_organization'),




    path('admin-dashboard/', views.home, name='admin_dashboard'),
    path('organizer-dashboard/', views.home, name='organizer_dashboard'),
    path('student-dashboard/', views.home, name='student_dashboard'),
    path('logout/', lambda request: redirect('login'), name='logout'),
]
