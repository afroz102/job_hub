from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_page, name="home"),

    # profie  of loggedIn User
    path('profile/', views.user_profile, name="user_profile"),
    path('profile/<int:pk>/', views.user_profile_by_id, name="user_profile_by_id"),

    # Add Portfolifo
    path('add_portfolio_content/',
         views.add_portfolio_content, name="add_portfolio_content"),
    path('update_portfolio/<int:portfolio_pk>/',
         views.update_portfolio_by_id, name="update_portfolio_by_id"),


    path('update_profession_title/', views.update_job_title,
         name="update_profession_title"),

    path('update_name/', views.update_name, name="update_name"),
    path('update_profile_img/', views.update_profile_img,
         name="update_profile_img"),
    path('update_phone/', views.update_phone, name="update_phone"),
    path('update_location/', views.update_location, name="update_location"),
    path('update_age/', views.update_age, name="update_age"),
    path('update_gender/', views.update_gender, name="update_gender"),
    path('update_about_me/', views.update_about_me, name="update_about_me"),


    path('add_education_details/',
         views.add_education_details, name="add_education_details"),
    path('update_education_details/<int:pk>/',
         views.update_education_details, name="update_education_details"),
    path('delete_education_details/<int:pk>/',
         views.delete_education_details, name="delete_education_details"),

    path('add_new_skill/', views.add_new_skill, name="add_new_skill"),
    path('update_skill/<int:pk>/', views.update_skill, name="update_skill"),
    path('delete_skill/<int:pk>/', views.delete_skill, name="delete_skill"),

    path('add_new_language/', views.add_new_language, name="add_new_language"),
    path('update_language/<int:pk>/',
         views.update_language, name="update_language"),
    path('delete_language/<int:pk>/',
         views.delete_language, name="delete_language"),

    path('add_prefered_location/',
         views.add_prefered_location, name="add_prefered_location"),
    path('delete_prefered_location/<int:pk>/',
         views.delete_prefered_location, name="delete_prefered_location"),

    #     Account Verification request
    path('send_verification_request/',
         views.send_verification_request, name="send_verification_request"),
]
