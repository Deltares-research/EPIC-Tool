import abc

from django import forms
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from epic_app.importers import EpicAgencyImporter, EpicDomainImporter, EpicImporter
from epic_app.models.models import (
    Agency,
    Answer,
    Area,
    EpicUser,
    Group,
    Program,
    Question,
)


class CsvImportForm(forms.Form):
    """
    Simple form to allow importing a 'csv' file.

    Args:
        forms (forms.Form): Default Django form.
    """

    csv_file = forms.FileField()


class ImportEntityAdmin(admin.ModelAdmin):
    """
    Overriding of the Area list in the admin page so that we can add our custom import for all the data.
    """

    # Admin pages.
    change_list_template = "import_changelist.html"

    def get_urls(self):
        """
        Extends the default get_urls so we can inject the import-csv on

        Returns:
            List[str]: A list of the urls to load from the admin page.
        """
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        """
        Imports a csv file into the EPIC database structure.

        Args:
            request (HTTPRequest): HTML request.

        Returns:
            HTTPRequest: HTML response.
        """
        if request.method == "POST":
            try:
                self.get_importer().import_csv(request.FILES["csv_file"])
                self.message_user(request, "Your csv file has been imported")
            except:
                self.message_user(
                    request, "It was not possible to import the requested csv file."
                )
            return redirect("..")

        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)

    @abc.abstractmethod
    def get_importer(self) -> EpicImporter:
        raise NotImplementedError("Should be implemented in concrete class.")


class AreaAdmin(ImportEntityAdmin):
    """
    Area admin page to allow CSV import.
    """

    def get_importer(self) -> EpicDomainImporter:
        return EpicDomainImporter()


class AgencyAdmin(ImportEntityAdmin):
    """
    Agency admin page to allow CSV import.
    """

    def get_importer(self) -> EpicAgencyImporter:
        return EpicAgencyImporter()


# Models exposed to the admin page .
admin.site.register(EpicUser)
admin.site.register(Area, AreaAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(Group)
admin.site.register(Program)
admin.site.register(Question)
admin.site.register(Answer)
