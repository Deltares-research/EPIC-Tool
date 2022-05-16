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
        reference: Optional[str]
        reference_link: Optional[str]

        @classmethod
        def from_xlsx_row(cls, xlsx_row: Any):
            new_obj = cls()
            new_obj.area = cls.get_valid_cell(xlsx_row, 0)
            new_obj.group = cls.get_valid_cell(xlsx_row, 1)
            new_obj.program = cls.get_valid_cell(xlsx_row, 2)
            new_obj.description = cls.get_valid_cell(xlsx_row, 3)
            new_obj.reference = cls.get_valid_cell(xlsx_row, 4)
            new_obj.reference_link = cls.get_valid_cell(xlsx_row, 5)
            return new_obj

        def to_epic_program(self) -> Program:
            epic_area, _ = Area.objects.get_or_create(name=self.area.strip)
            epic_group, _ = Group.objects.get_or_create(
                name=self.group.strip(), area=epic_area
            )
            return Program(
                name=self.program.strip(),
                description=self.description.strip(),
                reference_description=self.reference.strip(),
                reference_link=self.reference_link,
                group=epic_group,
            )

    def _cleanup_epic_domain(self):
        """
        Dumps the database for the entities to import.
        """
        Area.objects.all().delete()
        Group.objects.all().delete()
        Program.objects.all().delete()

    def import_file(self, input_file: Union[InMemoryUploadedFile, Path]):
        self._cleanup_epic_domain()
        line_objects: List[self.XlsxLineObject] = self._get_xlsx_line_objects(
            input_file
        )
        _headers = line_objects.pop(0)
        list(map(lambda x: x.to_epic_program().save(), line_objects))
