from pathlib import Path
from typing import Any, List, Optional, Type

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand

from epic_app.importers.xlsx import (
    BaseEpicImporter,
    EpicAgencyImporter,
    EpicDomainImporter,
    EvolutionQuestionImporter,
    KeyAgencyActionsQuestionImporter,
    NationalFrameworkQuestionImporter,
)
from epic_app.models.epic_questions import LinkagesQuestion
from epic_app.models.epic_user import EpicOrganization, EpicUser
from epic_app.tests import test_data_dir


class Command(BaseCommand):
    help = "Sets the default EPIC database with a predefined admin user. If the database already exists then it removes it (and its migrations) and creates one from zero."
    # epic_setup.py -> commands -> management -> epic_app
    epic_app_dir: Path = Path(__file__).parent.parent.parent
    root_dir: Path = epic_app_dir.parent

    def _remove_migrations(self):
        """
        Removes all previous migrations.
        """
        migrations_dir = self.epic_app_dir / "migrations"
        for m_file in migrations_dir.glob("*.py"):
            if m_file.name != "__init__.py":
                self.stdout.write(
                    self.style.WARNING(f"Removing migration file: {m_file.name}")
                )
                m_file.unlink()

    def _cleanup_db(self):
        """
        Removes the current database.
        """
        db_path = self.root_dir / "db.sqlite3"
        if db_path.is_file():
            self.stdout.write(
                self.style.WARNING(f"Removing database file at {db_path}")
            )
            db_path.unlink()
        self._remove_migrations()
        self.stdout.write(
            self.style.SUCCESS("Successfully cleaned up previous database structure.")
        )

    def _import_files(self, test_data_dir: Path):
        """
        Imports all the available files to create a reliable test environment.

        Args:
            test_data_dir (Path): Path to the test directory.
        """

        def import_and_log(filepath: Path, epic_importer: Type[BaseEpicImporter]):
            test_file = test_data_dir / "xlsx" / filepath
            if test_file.is_file():
                self.stdout.write(
                    self.style.MIGRATE_HEADING(f"Importing main data from {test_file}.")
                )
                try:
                    epic_importer().import_file(test_file)
                    self.stdout.write(self.style.SUCCESS("Import successful."))
                except Exception:
                    self.stdout.write(self.style.ERROR(f"Failed to import {filepath}."))
            else:
                self.stdout.write(
                    self.style.ERROR(f"File to import not found at {filepath}")
                )

        import_and_log("initial_epic_data.xlsx", EpicDomainImporter)
        import_and_log("agency_data.xlsx", EpicAgencyImporter)
        import_and_log(
            "nationalframeworkquestions.xlsx", NationalFrameworkQuestionImporter
        )
        import_and_log(
            "keyagencyactionsquestions.xlsx", KeyAgencyActionsQuestionImporter
        )
        import_and_log("evolutionquestions.xlsx", EvolutionQuestionImporter)
        LinkagesQuestion.generate_linkages()
        self.stdout.write(
            self.style.SUCCESS("Generated one linkage question per loaded program.")
        )

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

        create_organization("Nintento", ["Zelda", "Ganon"])
        create_organization("Rebel Alliance", ["Luke", "Leia"])

    def _import_test_db(self):
        if not test_data_dir.is_dir():
            self.stdout.write(
                self.style.ERROR(
                    f"No test data found at {test_data_dir}, database will be empty on start."
                )
            )
        try:
            self._import_files(test_data_dir)
            self._create_dummy_users()
        except Exception as e_info:
            call_command("flush")
            self.stdout.write(
                self.style.ERROR(
                    f"Could not correctly import test data, database will be empty on start. Detail error: {str(e_info)}."
                )
            )

    def _migrate_db(self):
        """
        Creates the current database structure as sqlite3 file.
        """
        call_command("makemigrations")
        call_command("migrate")
        self._import_test_db()

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            self._cleanup_db()
            self._migrate_db()
        except Exception as e_info:
            self.stdout.write(
                self.style.ERROR(f"Error setting up EPIC. Detailed info: {str(e_info)}")
            )
