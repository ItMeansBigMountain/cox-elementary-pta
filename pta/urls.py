
from django.urls import path
from . import views
app_name='pta'
urlpatterns=[
    path('', views.home, name='home'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('newsletter/<slug:slug>/', views.newsletter_detail, name='newsletter_detail'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcements/<int:pk>/print/', views.announcement_print, name='announcement_print'),
    path('events/', views.events, name='events'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('join-pta/', views.join_pta, name='join_pta'),
    path('resources/', views.resources, name='resources'),
    path('fundraising/', views.fundraising, name='fundraising'),
    path('about-contact/', views.about_contact, name='about_contact'),
]
