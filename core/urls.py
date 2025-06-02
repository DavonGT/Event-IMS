from django.urls import path
from . import views
from django.shortcuts import redirect


urlpatterns = [
    path('calendar/', views.calendar, name='calendar'),
    path('', views.events_dashboard, name='events_dashboard'),

    path('get-events-by-month', views.get_events_by_month, name='get_events_by_month'),

    # path('dashboard/', views.dashboard, name='dashboard'),
    path('add-event/', views.add_event, name='add_event'),
    path('add-activity/', views.add_activity, name='add_activity'),
    path('events_list/<int:organization_id>/', views.events_list, name='events_list_filtered'),
    path('events_list/', views.events_list, name='events_list'),

    path('activities_list/<int:college_id>/', views.activities_list, name='activities_list_filtered'),
    path('activities_list/', views.activities_list, name='activities_list'),

    path('upload_files/', views.upload_file_view, name='upload_files'),

    # path('view-event/<int:event_id>/', views.view_event, name='view_event'),
    # path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    # path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('events/<int:event_id>/view/', views.view_event, name='view_event'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('organizations/add/', views.add_organization, name='add_organization'),

    path('activity/<int:activity_id>/delete/', views.delete_activity, name='delete_activity'),
    path('activity/<int:activity_id>/view/', views.view_activity, name='view_activity'),
    path('activity/<int:activity_id>/edit/', views.edit_activity, name='edit_activity'),
    path('college/add/', views.add_college, name='add_college'),

    path('profile/', views.profile, name='profile'),
    path('profile/edit/<int:user_id>/', views.edit_profile, name='edit_profile'),


    # path('admin-dashboard/', views.home, name='admin_dashboard'),
    # path('organizer-dashboard/', views.home, name='organizer_dashboard'),
    # path('student-dashboard/', views.home, name='student_dashboard'),
    path('logout/', lambda request: redirect('login'), name='logout'),
]
