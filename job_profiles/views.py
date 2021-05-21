# import json
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, JsonResponse
# from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from users.models import UserProfile
from .models import Portfolio, EducationDetail, LanguageKnown, Skill, PreferedLocation
from .forms import UpdateUserForm, UpdateUserProfileForm, AddSkillsForm, AddEducationDetailsForm, AddLanguageForm, SummerNoteForm


@login_required(login_url='login')
def home_page(request):
    user = request.user
    userProfile, cteated = UserProfile.objects.get_or_create(user=user)

    userDatas = UserProfile.objects.filter(is_verified=True)

    user_obj_list = []
    for userData in userDatas:
        skills = Skill.objects.filter(user_profile=userData)
        userProfileObj = {
            'userProfile': userData,
            "skills": skills,
        }
        user_obj_list.append(userProfileObj)

    # print("user_obj_list: ", user_obj_list)
    context = {
        "loggedInUser": userProfile,
        "user_obj_list": user_obj_list,
    }

    return render(request, 'job_profiles/home_page.html', context)


# User profile of loggedin User
@login_required(login_url='login')
def user_profile(request):
    user = request.user
    userProfile = get_object_or_404(UserProfile, user=user)

    portfolios = Portfolio.objects.filter(
        user_profile=userProfile).order_by('-created_at')

    educationDetails = EducationDetail.objects.filter(
        user_profile=userProfile).order_by('education')
    languagesKnown = LanguageKnown.objects.filter(
        user_profile=userProfile).order_by('-created_at')
    skills = Skill.objects.filter(
        user_profile=userProfile).order_by('-created_at')
    preferedLocations = PreferedLocation.objects.filter(
        user_profile=userProfile).order_by('-created_at')

    # Sending portfolio Object and Realated Update form in a list
    portfolio_obj_list = []
    for portfolioItem in portfolios:
        portfolioObj = {
            'portfolio': portfolioItem,
            'form': SummerNoteForm(instance=portfolioItem),
        }
        portfolio_obj_list.append(portfolioObj)

    context = {
        "loggedInUser": userProfile,
        "userProfile": userProfile,
        "portfolios": portfolios,
        "portfolio_obj_list": portfolio_obj_list,
        "educationDetails": educationDetails,
        "languagesKnown": languagesKnown,
        "skills": skills,
        "preferedLocations": preferedLocations,

        "userForm": UpdateUserForm(instance=user),
        "userProfileForm": UpdateUserProfileForm(instance=userProfile),
        "educationForm": AddEducationDetailsForm(),
        "skillForm": AddSkillsForm(),
        "languageForm": AddLanguageForm(),
        "summerNoteModelForm": SummerNoteForm(),
    }
    return render(request, 'job_profiles/user_profile.html', context)


@login_required(login_url='login')
def user_profile_by_id(request, pk):
    user = request.user
    loggedInUser = get_object_or_404(UserProfile, user=user)

    userProfile = get_object_or_404(UserProfile, id=pk)

    portfolios = Portfolio.objects.filter(
        user_profile=userProfile).order_by('-created_at')

    educationDetails = EducationDetail.objects.filter(
        user_profile=userProfile).order_by('education')

    languagesKnown = LanguageKnown.objects.filter(
        user_profile=userProfile).order_by('-created_at')

    skills = Skill.objects.filter(
        user_profile=userProfile).order_by('-created_at')

    preferedLocations = PreferedLocation.objects.filter(
        user_profile=userProfile).order_by('-created_at')

    # Sending portfolio Object and Realated Update form in a list
    # update Form not needed
    portfolio_obj_list = []
    for portfolioItem in portfolios:
        portfolioObj = {
            'portfolio': portfolioItem,
            # 'form': SummerNoteForm(instance=portfolioItem),
        }
        portfolio_obj_list.append(portfolioObj)

    context = {
        "loggedInUser": loggedInUser,
        "userProfile": userProfile,
        "portfolio_obj_list": portfolio_obj_list,
        "educationDetails": educationDetails,
        "languagesKnown": languagesKnown,
        "skills": skills,
        "preferedLocations": preferedLocations,
    }
    return render(request, 'job_profiles/user_profile.html', context)


# ---------------------------------************************-------------------------
# PortFolio Related Functions starts
@login_required(login_url='login')
def add_portfolio_content(request):
    # print("POST method: ", request.POST)
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        form = SummerNoteForm(request.POST)
        if form.is_valid():
            # print("Form Valid")
            newPortfolioObj = form.save(commit=False)
            newPortfolioObj.user_profile = userProfile
            newPortfolioObj.save()
        else:
            print("Add Portfolio Form not Valid")

        return redirect('user_profile')


# Update a portfolio of user
@login_required(login_url='login')
def update_portfolio_by_id(request, portfolio_pk):
    if request.method == 'POST':
        portfolio = Portfolio.objects.get(id=pk)
        postForm = SummerNoteForm(request.POST, instance=portfolio)
        if postForm.is_valid():
            postForm.save()
        else:
            print("postForm is not valid")

        return redirect('user_profile')

        # portfolio = Portfolio.objects.get(id=portfolio_pk)
        # title = request.POST['title']
        # content = request.POST['content']
        # portfolio.title = title
        # portfolio.content = content
        # portfolio.save()
        # return redirect('user_profile')


# PortFolio Related Functions ends
# ---------------------------------************************-------------------------


# ---------------------------------************************-------------------------
# UserProfile Update Details starts
@login_required(login_url='login')
def update_job_title(request):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        userProfile.profession_title = request.POST['profession_title']
        userProfile.save()

        return redirect('user_profile')


@login_required(login_url='login')
def update_name(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()

    return redirect('user_profile')


@login_required(login_url='login')
def update_profile_img(request):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        userProfile.profile_img = request.FILES['profile_img']
        userProfile.save()

    return redirect('user_profile')


@login_required(login_url='login')
def update_phone(request):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        userProfile.phone = request.POST['phone']
        userProfile.save()

    return redirect('user_profile')


@login_required(login_url='login')
def update_location(request):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        userProfile.location = request.POST['location']
        userProfile.save()

    return redirect('user_profile')


@login_required(login_url='login')
def update_age(request):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        userProfile.age = request.POST['age']
        userProfile.save()

    return redirect('user_profile')


@login_required(login_url='login')
def update_gender(request):
    if request.method == 'POST':
        print(request.POST)
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        userProfile.gender = request.POST['gender']
        userProfile.save()

    return redirect('user_profile')


@login_required(login_url='login')
def update_about_me(request):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        about_me_text = request.POST['about_me']
        userProfile.about_me = about_me_text
        userProfile.save()

    return redirect('user_profile')


# UserProfile Update Details ends
# ---------------------------------************************-------------------------


# ---------------------------------************************-------------------------
# Education Details starts
@login_required(login_url='login')
def add_education_details(request):
    # print("POST method: ", request.POST)
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        form = AddEducationDetailsForm(request.POST)
        if form.is_valid():
            print("Form Valid")
            newEducationObj = form.save(commit=False)
            newEducationObj.user_profile = userProfile
            newEducationObj.save()
        else:
            print("AddEducationDetailsForm Form not Valid")

        return redirect('user_profile')


@login_required(login_url='login')
def update_education_details(request, pk):
    if request.method == 'POST':
        try:
            educationDetailsObj = EducationDetail.objects.get(id=pk)

        except EducationDetail.DoesNotExist:
            raise Http404()

        educationDetailsObj.course = request.POST['course']
        educationDetailsObj.specialization = request.POST['specialization']
        educationDetailsObj.university = request.POST['university']
        educationDetailsObj.graduation_year = request.POST['graduation_year']
        educationDetailsObj.save()

        return redirect('user_profile')


@login_required(login_url='login')
def delete_education_details(request, pk):
    # print("request.POST: ", request.POST, pk)
    if request.method == 'POST':
        try:
            educationDetailsObj = EducationDetail.objects.get(id=pk)
        except EducationDetail.DoesNotExist:
            raise Http404()

        educationDetailsObj.delete()
        # print(educationDetailsObj, " Deleted")

        return redirect('user_profile')

# Education Details ends
# ---------------------------------************************-------------------------


# ---------------------------------************************-------------------------
# Skills Details starts
@login_required(login_url='login')
def add_new_skill(request):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        form = AddSkillsForm(request.POST)
        if form.is_valid():
            # print("Form Valid")
            newSkillObj = form.save(commit=False)
            newSkillObj.user_profile = userProfile
            newSkillObj.save()

    return redirect('user_profile')


@login_required(login_url='login')
def update_skill(request, pk):
    if request.method == 'POST':
        try:
            skillObj = Skill.objects.get(id=pk)
        except Skill.DoesNotExist:
            raise Http404()

        skillObj.skill = request.POST['skill']
        skillObj.proficiency = request.POST['proficiency']
        skillObj.save()

    return redirect('user_profile')


@login_required(login_url='login')
def delete_skill(request, pk):
    if request.method == 'POST':
        try:
            skillObj = Skill.objects.get(id=pk)
        except Skill.DoesNotExist:
            raise Http404()

        skillObj.delete()

    return redirect('user_profile')

# Education Details ends
# ---------------------------------************************-------------------------


# ---------------------------------************************-------------------------
# Language Details starts
@login_required(login_url='login')
def add_new_language(request):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        form = AddLanguageForm(request.POST)
        if form.is_valid():
            print("Form Valid")
            newlanguageObj = form.save(commit=False)
            newlanguageObj.user_profile = userProfile
            newlanguageObj.save()

    return redirect('user_profile')


@login_required(login_url='login')
def update_language(request, pk):
    if request.method == 'POST':
        try:
            languageObj = LanguageKnown.objects.get(id=pk)
        except LanguageKnown.DoesNotExist:
            raise Http404()

        languageObj.language = request.POST['language']
        languageObj.fluency = request.POST['fluency']
        languageObj.save()

        return redirect('user_profile')


@login_required(login_url='login')
def delete_language(request, pk):
    if request.method == 'POST':
        try:
            languageObj = LanguageKnown.objects.get(id=pk)
        except LanguageKnown.DoesNotExist:
            raise Http404()

        languageObj.delete()

    return redirect('user_profile')

# Language Details ends
# ---------------------------------************************-------------------------


# ---------------------------------************************-------------------------
# Location Details ends
@login_required(login_url='login')
def add_prefered_location(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    PreferedLocation.objects.create(
        user_profile=userProfile,
        prefered_location=request.POST['prefered_location']
    )
    return redirect('user_profile')


@login_required(login_url='login')
def delete_prefered_location(request, pk):
    if request.method == 'POST':
        try:
            locationObj = PreferedLocation.objects.get(id=pk)
        except PreferedLocation.DoesNotExist:
            raise Http404()

        locationObj.delete()
    return redirect('user_profile')

# Location Details ends
# ---------------------------------************************-------------------------


# ---------------------------------************************-------------------------
# Send Account verification request to admin
@login_required(login_url='login')
def send_verification_request(request):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        userProfile.sent_for_verification = True
        userProfile.save()

    return redirect('user_profile')
