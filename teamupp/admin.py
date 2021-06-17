from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

import teamupp.models as models


# Register your models here.
admin.site.register(models.Placements)
admin.site.register(models.TeamUppUser, UserAdmin)
admin.site.register(models.Company)
admin.site.register(models.Week)
admin.site.register(models.Group)
admin.site.register(models.Project)
