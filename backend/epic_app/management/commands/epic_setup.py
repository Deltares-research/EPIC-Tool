from pathlib import Path
from typing import Any, Optional

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand

from epic_app.importers import EpicAgencyImporter, EpicDomainImporter
from epic_app.importers.csv_base_importer import BaseEpicImporter
from epic_app.importers.question_csv_importer import (
    EvolutionQuestionImporter,
    NationalFrameworkQuestionImporter,
)
from epic_app.models.epic_questions import LinkagesQuestion
from epic_app.models.epic_user import EpicUser
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

        def import_and_log(filepath: Path, epic_importer: BaseEpicImporter):
            test_file = test_data_dir / filepath
            if test_file.is_file():
                self.stdout.write(
                    self.style.MIGRATE_HEADING(f"Importing main data from {test_file}.")
                )
                epic_importer().import_csv(test_file)
                self.stdout.write(self.style.SUCCESS("Import successful."))

        import_and_log("initial_epic_data.csv", EpicDomainImporter)
        import_and_log("agency_data.csv", EpicAgencyImporter)
        import_and_log(
            "nationalframeworkquestions.csv", NationalFrameworkQuestionImporter
        )
        import_and_log("evolutionquestions.csv", EvolutionQuestionImporter)
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
        def create_user(user_name: str, user_org: str):
            c_user = EpicUser(username=user_name, organization=user_org)
            # Use the same username but with lowercase (it's a test!)
            c_user.set_password(user_name.lower())
            c_user.save()

        create_user("Zelda", "Nintendo")
        create_user("Ganon", "Nintendo")
        create_user("Luke", "Rebel Alliance")
        create_user("Leia", "Rebel Alliance")
        self.stdout.write(
            self.style.SUCCESS(
                "Created some 'dummy' users: 'Zelda', 'Ganon', 'Luke' and 'Leia'. Their passwords match the lowercase username."
            )
        )

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
