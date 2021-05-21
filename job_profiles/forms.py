from django import forms
from django.contrib.auth.models import User

from django_summernote.widgets import SummernoteWidget

from users.models import UserProfile
from .models import Portfolio, EducationDetail, Skill, LanguageKnown


class SummerNoteForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'content': SummernoteWidget(attrs={
                'class': 'control-label font-weight-bold',
            }),
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        # exclude = ['company', 'date_created',
        #            'is_deleted', 'date_updated', 'added_by']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'last_name': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'email': forms.EmailInput(attrs={
                'type': 'email',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
        }

    # Disable Email field for updating
    def __init__(self, *args, ** kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True

    # def __init__(self, company=None, *args, ** kwargs):
    #     super(UpdateUserForm, self).__init__(*args, **kwargs)
    #     if company:
    #         self.fields['email'].queryset = Unit.objects.filter(
    #             company=company, is_deleted=False)


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'gender', 'age',
                  'location', 'profile_img', 'about_me']
        # exclude = ['company', 'date_created',
        #            'is_deleted', 'date_updated', 'added_by']

        widgets = {
            'phone': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'gender': forms.Select(attrs={
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'age': forms.NumberInput(attrs={
                'type': 'number',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'location': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'about_me': forms.Textarea(attrs={
                'class': "form-control",
                'autofocus': 'autofocus',
                'row': 2,
            }),
        }


class AddEducationDetailsForm(forms.ModelForm):
    class Meta:
        model = EducationDetail
        fields = ['education', 'course', 'specialization',
                  'university', 'graduation_year']

        widgets = {
            'education': forms.Select(attrs={
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'course': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
                'placeholder': 'B.Tech',
            }),
            'specialization': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
                'placeholder': 'Computer Science',
            }),
            'university': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
                'placeholder': 'IISC Bangalore',
            }),
            'graduation_year': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
                'placeholder': '2021',
            }),
        }


class AddSkillsForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill', 'proficiency']

        widgets = {
            'skill': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'proficiency': forms.NumberInput(attrs={
                'type': 'number',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
        }


class AddLanguageForm(forms.ModelForm):
    class Meta:
        model = LanguageKnown
        fields = ['language', 'fluency']

        widgets = {
            'language': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'fluency': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
        }
