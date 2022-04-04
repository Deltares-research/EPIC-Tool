from django.contrib import admin
from django import forms
from django.shortcuts import redirect, render
from django.urls import path
from epic_app.models import Answer, EpicUser, Question, Area, Group, Program
import csv

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class AreaAdmin(admin.ModelAdmin):
    """
    Overriding of the Area list in the admin page so that we can add our custom import for all the data.
    """
    # Admin pages.
    change_list_template = "areas_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(csv_file)
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

# Models exposed to the admin page .
admin.site.register(EpicUser)
admin.site.register(Area, AreaAdmin)
admin.site.register(Group)
admin.site.register(Program)
admin.site.register(Question)
admin.site.register(Answer)