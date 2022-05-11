from __future__ import annotations

from typing import List

from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string

from epic_app.models.models import Program


class EpicOrganization(models.Model):
    name: str = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

    def generate_users(self, n_users: int) -> List[EpicUser]:
        """
        Creates 'n' `EpicUser` objects that belong to this `EpicOrganization`

        Args:
            n_users (int): Number of users to create.

        Returns:
            List[EpicUser]: List of created `EpicUsers`
        """

        def create_epic_user() -> EpicUser:
            """
            Creates an epic user with a random unique username and a matching (lowercase) password.

            Returns:
                EpicUser: Generated `EpicUser`.
            """
            epic_username: str = (
                f"{get_random_string(length=7)}{len(EpicUser.objects.all())}"
            )
            epic_user = EpicUser(username=epic_username, organization=self)
            epic_user.set_password(epic_username.lower())
            epic_user.save()
            return epic_user

        return [create_epic_user() for n in range(0, n_users)]


class EpicUser(User):
    """
    Defines the properties for a typical user in EpicTool.

    Args:
        User (auth.models.User): Derives directly from the base class User.
    """

    is_advisor = models.BooleanField(default=False)
    organization = models.ForeignKey(
        to=EpicOrganization,
        on_delete=models.CASCADE,
        related_name="organization_users",
        blank=True,
        null=True,
    )
