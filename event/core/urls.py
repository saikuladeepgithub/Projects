from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index,name='index'),
    path('student/',views.student,name='student'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('faculty/',views.faculty,name='faculty'),
    path('facultylogin/',views.facultylogin,name='facultylogin'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/chat/', views.event_chat, name='event_chat'),
    path('event/<int:event_id>/unregister/', views.unregister_volunteer, name='unregister_volunteer'),
    path('submit-event/', views.submit_event_proposal, name='submit_event_proposal'),
    path('events-analysis/', views.events_analysis, name='events_analysis'),
    path('gallery/',views.gallery,name='gallery'),
    path('gallery/<int:event_id>/',views.gallery_images,name='gallery_images'),
]
