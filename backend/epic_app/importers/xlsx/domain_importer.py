import csv
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from django.core.files.uploadedfile import InMemoryUploadedFile
from openpyxl import Workbook

from epic_app.importers.xlsx.base_importer import BaseEpicImporter
from epic_app.models.models import Area, Group, Program


class EpicDomainImporter(BaseEpicImporter):
    """
    Class that contains an importer for all the Epic elements.
    """

    class XlsxLineObject(BaseEpicImporter.XlsxLineObject):
        """
        Maps a XLSX row into a data object that we can better manipulate.
        """

        area: str
        group: str
        program: str
        description: Optional[str]

        @classmethod
        def from_xlsx_row(cls, xlsx_row: Any):
            new_obj = cls()
            new_obj.area = cls.get_valid_cell(xlsx_row, 0)
            new_obj.group = cls.get_valid_cell(xlsx_row, 1)
            new_obj.program = cls.get_valid_cell(xlsx_row, 2)
            new_obj.description = cls.get_valid_cell(xlsx_row, 3)
            return new_obj

    def _cleanup_epic_domain(self):
        """
        Dumps the database for the entities to import.
        """
        Area.objects.all().delete()
        Group.objects.all().delete()
        Program.objects.all().delete()

    def _import_epic_domain(self, areas_dictionary: Dict[str, List[XlsxLineObject]]):
        """
        Imports all the read objects from the csv into the database.

        Args:
            areas_dictionary (Dict[str, List[CsvLineObject]]): Dictionary containing text objects to add in the database.
        """
        programs_to_save = []
        for r_area, r_area_values in areas_dictionary.items():
            # Create new area
            c_area = Area(name=r_area.strip())
            c_area.save()
            read_groups = self.group_entity("group", r_area_values)
            for r_group, r_group_values in read_groups.items():
                # Create new group
                c_group = Group(name=r_group.strip(), area=c_area)
                c_group.save()
                for r_csv_value in r_group_values:
                    # Create new program
                    c_program = Program(
                        name=r_csv_value.program.strip(),
                        description=r_csv_value.description.strip(),
                        group=c_group,
                    )
                    programs_to_save.append(c_program)
        for p in programs_to_save:
            p.save()

    def import_file(self, input_file: Union[InMemoryUploadedFile, Path]):
        self._cleanup_epic_domain()
        line_objects = self._get_xlsx_line_objects(input_file)
        _headers = line_objects.pop(0)
        self._import_epic_domain(self.group_entity("area", line_objects))
