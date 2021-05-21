# import json
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


from users.models import UserProfile
from . import calender
from . import gmail


@login_required
def testing_apis(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)

    # print("user_obj_list: ", user_obj_list)
    context = {
        "loggedInUser": userProfile,
    }

    return render(request, 'apis_testing/main_apis_page.html', context)


# Gmail Authorization
@login_required
def authorise_gmail(request):
    service = gmail.run_api(request.user)
    # request.session['active_tab'] = 3
    return redirect('/')


@login_required
# @require_safe
def send_mail(request):
    data = {
        'success': False
    }
    service = gmail.run_api(request.user)
    if request.method == 'GET':
        email = request.GET['email-to']
        subject = request.GET['email-subject']
        body = request.GET['email-body']

        gmail.SendMessage(
            service,
            'me',
            gmail.CreateMessage(
                request.user.email,
                email,
                subject,
                body
            )
        )
        data = {
            'success': True
        }
    return JsonResponse(data)


@login_required
def calenderAPIs(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)

    context = {
        "loggedInUser": userProfile,
    }

    return render(request, 'apis_testing/calenders/calender.html', context)


@csrf_exempt
def fetch_calender_events(request):
    print("Hello")
    if request.method == 'POST':
        # print("x")
        calender_data = calender.getCalenderData()
        # print("calender_data: ", calender_data)
        for data in calender_data:
            print("xyz: ", data)

        return JsonResponse({"calender_data": calender_data})


# Calender Events
def create_calender_event(request):
    if request.method == 'POST':
        event_summary = request.POST['event_summary']
        event_date = request.POST['event_date']
        start_time = request.POST['event_start_time']
        end_time = request.POST['event_end_time']

    return JsonResponse({"msg": "hello"})
