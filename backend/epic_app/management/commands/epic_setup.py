from pathlib import Path
from typing import Any, Optional

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


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
                    self.style.NOTICE(f"Removing migration file: {m_file.name}")
                )
                m_file.unlink()

    def _cleanup_db(self):
        """
        Removes the current database.
        """
        db_path = self.root_dir / "db.sqlite3"
        if db_path.is_file():
            self.stdout.write(self.style.NOTICE(f"Removing database file at {db_path}"))
            db_path.unlink()
        self._remove_migrations()
        self.stdout.write(
            self.style.SUCCESS("Successfully cleaned up previous database structure.")
        )

    def _migrate_db(self):
        """
        Creates the current database structure as sqlite3 file.
        """
        call_command("makemigrations")
        call_command("migrate")
        call_command("createsuperuser")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            self._cleanup_db()
            self._migrate_db()
        except Exception as e_info:
            self.stdout.write(
                self.style.ERROR(f"Error setting up EPIC. Detailed info: {str(e_info)}")
            )
