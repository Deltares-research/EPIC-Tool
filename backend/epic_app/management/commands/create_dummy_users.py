from pathlib import Path
from typing import Any, List, Optional

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand

from epic_app.models.epic_user import EpicOrganization, EpicUser


class Command(BaseCommand):
    help = "Generates dummy EpicUsers and a dummy admin with their usernames matching the password."

    def _create_superuser(self):
        """
        Creates an admin 'superuser' with classic 'admin'/'admin' user/pass.
        """
        # Create an admin user.
        admin_user = User(
            username="admin",
            email="admin@testdb.com",
            first_name="Star",
            last_name="Lord",
        )
        admin_user.set_password("admin")
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        self.stdout.write(
            self.style.SUCCESS("Created superuser: 'admin', password: 'admin'.")
        )

    def _create_dummy_users(self):
        try:
            self._create_superuser()
        except:
            call_command("createsuperuser")

        # Create a few basic users.
        def create_user(user_name: str, user_org: EpicOrganization):
            c_user = EpicUser(username=user_name, organization=user_org)
            # Use the same username but with lowercase (it's a test!)
            c_user.set_password(user_name.lower())
            c_user.save()

        def create_organization(organization_name: str, user_names: List[str]):
            epic_org = EpicOrganization.objects.create(name=organization_name)
            for name in user_names:
                create_user(name, epic_org)
            self.stdout.write(
                self.style.SUCCESS(
                    "Created organization: '{}' with users: {}.".format(
                        organization_name, ", ".join([f"'{n}'" for n in user_names])
                    )
                    + " Their passwords match the lowercase username."
                )
            )

        create_organization("Deltares", ["Zelda", "Ganon"])
        create_organization("Rebel Alliance", ["Luke", "Leia"])

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            self._create_dummy_users()
        except Exception as e_info:
            self.stdout.write(
                self.style.ERROR(f"Error setting up EPIC. Detailed info: {str(e_info)}")
            )
