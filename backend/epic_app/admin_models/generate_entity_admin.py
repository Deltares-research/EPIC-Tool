import abc
from typing import List
from wsgiref.simple_server import WSGIRequestHandler

from django import forms
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from epic_app.models.epic_questions import LinkagesQuestion
from epic_app.models.epic_user import EpicOrganization, EpicUser


class GenerateEntityAdmin(admin.ModelAdmin):
    # Admin pages.
    change_list_template = "generate_changelist.html"

    def get_urls(self):
        """
        Extends the default get_urls so we can inject the generate 'x' logic.

        Returns:
            List[str]: A list of the urls to load from the admin page.
        """
        urls = super().get_urls()
        my_urls = [
            path("generate/", self.generate_entities),
        ]
        return my_urls + urls

    @abc.abstractmethod
    def generate_entities(self, request):
        raise NotImplementedError("Implement in concrete classes.")


class LnkAdmin(GenerateEntityAdmin):
    def generate_entities(self, request):
        """
        Generates all `LinkagesQuestion` entries based on the existing `Programs`.

        Args:
            request (HTTPRequest): HTML request.

        Returns:
            HTTPRequest: HTML response.
        """
        if request.method == "GET":
            LinkagesQuestion.objects.all().delete()
            LinkagesQuestion.generate_linkages()
            self.message_user(
                request, "Generated one linkage question per existent program"
            )
        return redirect("..")


class EpicUserInline(admin.StackedInline):
    model = EpicUser
    fields = ("username",)


class EpicOrganizationAdmin(GenerateEntityAdmin):
    inlines = [
        EpicUserInline,
    ]

    class EpicUserGenerateForm(forms.Form):
        selected_org = forms.ModelChoiceField(queryset=EpicOrganization.objects.all())
        n_epic_users = forms.IntegerField(required=True, label="Number of users")

    def generate_entities(self, request: WSGIRequestHandler):
        """
        Generates all `LinkagesQuestion` entries based on the existing `Programs`.

        Args:
            request (HTTPRequest): HTML request.

        Returns:
            HTTPRequest: HTML response.
        """
        if request.method == "POST":
            # try:
            #     self.get_importer().import_file(request.FILES["xlsx_file"])
            #     self.message_user(request, "Your xlsx file has been imported")
            # except:
            #     self.message_user(
            #         request, "It was not possible to import the requested xlsx file."
            #     )
            epic_org: EpicOrganization = EpicOrganization.objects.filter(
                pk=request.POST["selected_org"]
            ).first()
            gen_users: List[EpicUser] = epic_org.generate_users(
                int(request.POST["n_epic_users"])
            )
            user_list = ", ".join([g_user.username for g_user in gen_users])
            self.message_user(
                request,
                f"Generated the following Epic Users with matching lowercase password for {epic_org.name}: \n {user_list}",
            )
            return redirect("..")

        form = self.EpicUserGenerateForm()
        payload = {"form": form}
        return render(request, "admin/populate_epicusers_form.html", payload)
