from django.contrib import admin
from epic_app.models import Answer, EpicUser, Question

# Models exposed to the admin page .
admin.site.register(EpicUser)
admin.site.register(Question)
admin.site.register(Answer)
