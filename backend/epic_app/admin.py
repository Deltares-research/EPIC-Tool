from django.contrib import admin

from epic_app.models import Answer, EpicUser, Question

# Register your models here.
admin.site.register(EpicUser)

# In theory this field will not be accessed as it will be a direct csv import.
admin.site.register(Question)

# These are only added until we have a more streamlined way of working.
admin.site.register(Answer)
