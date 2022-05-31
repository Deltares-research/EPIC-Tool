from pathlib import Path
from typing import Any, List, Optional

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand

from epic_app.tests import test_data_dir


class Command(BaseCommand):
    help = "Sets the default EPIC database. If the database already exists then it removes it (and its migrations) and creates one from zero. Use flag --test to generate dummy EpicUsers and an admin."
    # epic_setup.py -> commands -> management -> epic_app
    epic_app_dir: Path = Path(__file__).parent.parent.parent
    root_dir: Path = epic_app_dir.parent
    default_data_dir: Optional[Path] = None

    def add_arguments(self, parser):
        parser.add_argument(
            "default_files", type=Path, default=test_data_dir / "xlsx", nargs="?"
        )
        parser.add_argument(
            "--test",
            action="store_true",
            help="Sets some dummy users for testing purposes",
        )

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

    def _migrate_db(self, domain_dir: Path, is_test: bool):
        """
        Creates the current database structure as sqlite3 file.
        """
        call_command("makemigrations")
        call_command("migrate")
        call_command("import_epic_domain", domain_dir)
        if is_test:
            call_command("create_dummy_users")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            self._cleanup_db()
            self._migrate_db(options["default_files"], options["test"])
        except Exception as e_info:
            self.stdout.write(
                self.style.ERROR(f"Error setting up EPIC. Detailed info: {str(e_info)}")
            )
