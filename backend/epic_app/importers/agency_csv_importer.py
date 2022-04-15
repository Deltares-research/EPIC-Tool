import csv
from pathlib import Path
from typing import Dict, List, Union

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import ValidationError

from epic_app.importers.csv_base_importer import BaseEpicImporter
from epic_app.models.models import Agency, Program


class EpicAgencyImporter(BaseEpicImporter):
    class CsvLineObject:
        """
        Maps a CSV row into a data object that we can better manipulate.
        """

        agency: str
        program: str

        @classmethod
        def from_dictreader_row(cls, dict_keys: dict, dict_row: dict):
            new_line = cls()
            new_line.agency = dict_row.get(dict_keys["agency"])
            new_line.program = dict_row.get(dict_keys["program"])
            return new_line

    def _import_agencies(self, agencies_dictionary: Dict[str, List[CsvLineObject]]):
        missing_programs = []
        for agency_csvobjs in agencies_dictionary.values():
            for csv_obj in agency_csvobjs:
                if Program.get_program_by_name(csv_obj.program.lower()) is None:
                    missing_programs.append(csv_obj.program)
        if any(missing_programs):
            str_mp = ", ".join(set(missing_programs))
            raise ValidationError(
                f"The provided programs do not exist in the current database: \n{str_mp}"
            )

        # Remove all previous agency objects.
        Agency.objects.all().delete()
        for agency_name, agency_csvobj in agencies_dictionary.items():
            c_agency = Agency(name=agency_name)
            c_agency.save()
            for csvobj in agency_csvobj:
                existing_program: Program = Program.get_program_by_name(csvobj.program)
                existing_program.agencies.add(c_agency)

    def import_csv(self, input_csv_file: Union[InMemoryUploadedFile, Path]):
        """
        Imports saved Agencies into the database and adds the relationships to existent Programs.

        Args:
            input_csv_file (Union[InMemoryUploadedFile, Path]): File containing EPIC Agencies.
        """
        reader = csv.DictReader(self.get_valid_csv_text(input_csv_file))
        keys = dict(
            agency=reader.fieldnames[0],
            program=reader.fieldnames[1],
        )
        line_objects = []
        for row in reader:
            line_objects.append(self.CsvLineObject.from_dictreader_row(keys, row))

        self._import_agencies(self.group_entity("agency", line_objects))
