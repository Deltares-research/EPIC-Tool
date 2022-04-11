from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models

from epic_app.models.models import Program


class EpicUser(User):
    """
    Defines the properties for a typical user in EpicTool.

    Args:
        User (auth.models.User): Derives directly from the base class User.
    """

    organization: str = models.CharField(max_length=50)
    selected_programs = models.ManyToManyField(
        to=Program, blank=True, related_name="selected_by_users"
    )
