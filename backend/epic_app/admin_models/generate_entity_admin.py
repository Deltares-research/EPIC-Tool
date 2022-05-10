import abc
from typing import List, Union
from wsgiref.simple_server import WSGIRequestHandler

from django import forms
from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.db.models import QuerySet
from django.http import HttpRequest
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


class LnkAdmin(admin.ModelAdmin):
    actions = ["generate_entities"]

    @admin.action(description="Regenerate all Linkages Questions")
    def generate_entities(
        self, request: HttpRequest, queryset: Union[QuerySet, List[LinkagesQuestion]]
    ):
        queryset.all().delete()
        LinkagesQuestion.generate_linkages()
        self.message_user(
            request,
            f"Generated one linkage question per existent program, total: {len(LinkagesQuestion.objects.all())}",
        )

    def changelist_view(self, request: HttpRequest, extra_context=None):
        if "action" in request.POST and request.POST["action"] == "generate_entities":
            # We will automatically select all the entries for deletion.
            post = request.POST.copy()
            for u in LinkagesQuestion.objects.all():
                post.update({ACTION_CHECKBOX_NAME: str(u.id)})
            request._set_post(post)
        return super(LnkAdmin, self).changelist_view(request, extra_context)


class EpicUserInline(admin.TabularInline):
    model = EpicUser
    fields = ("username", "email", "is_staff")


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
