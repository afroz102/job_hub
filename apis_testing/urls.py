from django.urls import path

from . import views


urlpatterns = [
    path('testing_apis/', views.testing_apis, name='testing_apis'),

    #     Gmail APIs
    path('gmail/authorise/', views.authorise_gmail, name='authorise'),
    path('send/mail/', views.send_mail),

    #     Calender APIs
    path('testing_apis/calander/', views.calenderAPIs, name='calender_api'),

    path('fetch_calender_events/',
         views.fetch_calender_events, name='fetch_calender_events'),


]
