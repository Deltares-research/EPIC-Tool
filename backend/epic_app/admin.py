from django.contrib import admin
from epic_app.models import Answer, EpicUser, Question, Area, Group, Program

# Models exposed to the admin page .
admin.site.register(EpicUser)
admin.site.register(Area)
admin.site.register(Group)
admin.site.register(Program)
admin.site.register(Question)
admin.site.register(Answer)
