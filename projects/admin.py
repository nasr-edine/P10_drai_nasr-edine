from django.contrib import admin

from projects.models import Contributor, Project

# Register your models here.
admin.site.register(Project)
admin.site.register(Contributor)
