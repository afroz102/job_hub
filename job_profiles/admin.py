from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Portfolio, Skill, EducationDetail, LanguageKnown, PreferedLocation


class PortfolioAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(EducationDetail)
admin.site.register(LanguageKnown)
admin.site.register(Skill)
admin.site.register(PreferedLocation)
