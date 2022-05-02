from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from epic_app.models.epic_questions import LinkagesQuestion


class LnkAdmin(admin.ModelAdmin):
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
            path("generate/", self.generate_links),
        ]
        return my_urls + urls

    def generate_links(self, request):
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
