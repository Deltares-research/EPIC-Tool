from pathlib import Path
from typing import Any, Optional, Type

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


class Command(BaseCommand):
    help = "Imports all the available Epic files within the provided directory, replacing the previous related tables for the Epic domain."

    def add_arguments(self, parser):
        parser.add_argument("domain_files", type=Path, nargs="?")

    def _import_files(self, import_files_dir: Path):
        """
        Imports all the available files to create a reliable test environment.

        Args:
            import_files_dir (Path): Path to the test directory.
        """

        def import_and_log(filepath: Path, epic_importer: Type[BaseEpicImporter]):
            import_file = import_files_dir / filepath
            if import_file.is_file():
                self.stdout.write(
                    self.style.MIGRATE_HEADING(
                        f"Importing main data from {import_file}."
                    )
                )
                try:
                    epic_importer().import_file(import_file)
                    self.stdout.write(self.style.SUCCESS("Import successful."))
                except Exception as err_info:
                    self.stdout.write(self.style.ERROR(f"Failed to import {filepath}."))
                    self.stdout.write(
                        self.style.ERROR_OUTPUT("\n".join(err_info.messages))
                    )
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

    def _import_epic_db(self, data_dir: Path):
        if not data_dir.is_dir():
            self.stdout.write(
                self.style.ERROR(
                    f"No data found at {data_dir}, database will be empty on start."
                )
            )
        try:
            self._import_files(data_dir)
        except Exception as e_info:
            call_command("flush")
            self.stdout.write(
                self.style.ERROR(
                    f"Could not correctly import data, database will be empty on start. Detail error: {str(e_info)}."
                )
            )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            self._import_epic_db(options["domain_files"])
        except Exception as e_info:
            self.stdout.write(
                self.style.ERROR(
                    f"Error importing EPIC domain. Detailed info: {str(e_info)}"
                )
            )
