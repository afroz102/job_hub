# Generated by Django 3.2 on 2021-05-02 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210430_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profession_title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
