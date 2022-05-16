import csv
from pathlib import Path
from typing import Dict, List, Union

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import ValidationError

from epic_app.importers.xlsx.base_importer import BaseEpicImporter
from epic_app.models.models import Agency, Program


class EpicAgencyImporter(BaseEpicImporter):
    class XlsxLineObject(BaseEpicImporter.XlsxLineObject):
        agency: str
        program: str

        @classmethod
        def from_xlsx_row(cls, xlsx_row):
            new_line = cls()
            new_line.agency = cls.get_valid_cell(xlsx_row, 0)
            new_line.program = cls.get_valid_cell(xlsx_row, 1)
            return new_line

    def _validate(
        self,
        xlsx_line_objects: List[XlsxLineObject],
    ) -> List[str]:
        errors_found = []
        n_line_addition = 2  # Excluded header + start enumerate is 0.
        for n_line, xlsx_line in enumerate(xlsx_line_objects):
            if not Program.objects.filter(name__iexact=xlsx_line.program).exists():
                error_line = n_line + n_line_addition
                errors_found.append(
                    f"  - Line {error_line}. Program: '{xlsx_line.program}' does not exist."
                )
        return errors_found

    def _import_agencies(self, agencies_dictionary: Dict[str, List[XlsxLineObject]]):
        # Remove all previous agency objects.
        Agency.objects.all().delete()
        for agency_name, agency_csvobj in agencies_dictionary.items():
            c_agency = Agency(name=agency_name)
            c_agency.save()
            for csvobj in agency_csvobj:
                existing_program: Program = Program.get_program_by_name(csvobj.program)
                existing_program.agencies.add(c_agency)

    def import_file(self, input_file: Union[InMemoryUploadedFile, Path]):
        """
        Imports saved Agencies into the database and adds the relationships to existent Programs.

        Args:
            input_file (Union[InMemoryUploadedFile, Path]): File containing EPIC Agencies.
        """
        Agency.objects.all().delete()
        line_objects = self._get_xlsx_line_objects(input_file)
        _headers = line_objects.pop(0)
        errors_found = self._validate(line_objects)
        if any(errors_found):
            raise ValidationError(errors_found)
        self._import_agencies(self.group_entity("agency", line_objects))
