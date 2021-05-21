# Generated by Django 3.2 on 2021-04-30 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_userprofile_portfolio_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='languageknown',
            name='user_profile',
        ),
        migrations.RemoveField(
            model_name='preferedlocation',
            name='user_profile',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='user_profile',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='portfolio_content',
        ),
        migrations.DeleteModel(
            name='EducationDetail',
        ),
        migrations.DeleteModel(
            name='LanguageKnown',
        ),
        migrations.DeleteModel(
            name='PreferedLocation',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]