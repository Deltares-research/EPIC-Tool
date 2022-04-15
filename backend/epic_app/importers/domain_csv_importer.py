import csv
from pathlib import Path
from typing import Dict, List, Optional, Union

from django.core.files.uploadedfile import InMemoryUploadedFile

from epic_app.importers.csv_base_importer import BaseEpicImporter
from epic_app.models.models import Area, Group, Program


class EpicDomainImporter(BaseEpicImporter):
    """
    Class that contains an importer for all the Epic elements.
    """

    class CsvLineObject:
        """
        Maps a CSV row into a data object that we can better manipulate.
        """

        area: str
        group: str
        program: str
        description: Optional[str]

        @classmethod
        def from_dictreader_row(cls, dict_keys: dict, dict_row: dict):
            new_line = cls()
            new_line.area = dict_row.get(dict_keys["area"])
            new_line.group = dict_row.get(dict_keys["group"])
            new_line.program = dict_row.get(dict_keys["program"])
            new_line.description = dict_row.get(dict_keys["description"])
            return new_line

    def _cleanup_epic_domain(self):
        """
        Dumps the database for the entities to import.
        """
        Area.objects.all().delete()
        Group.objects.all().delete()
        Program.objects.all().delete()

    def _import_epic_domain(self, areas_dictionary: Dict[str, List[CsvLineObject]]):
        """
        Imports all the read objects from the csv into the database.

        Args:
            areas_dictionary (Dict[str, List[CsvLineObject]]): Dictionary containing text objects to add in the database.
        """
        for r_area, r_area_values in areas_dictionary.items():
            # Create new area
            c_area = Area(name=r_area)
            c_area.save()
            read_groups = self.group_entity("group", r_area_values)
            for r_group, r_group_values in read_groups.items():
                # Create new group
                c_group = Group(name=r_group, area=c_area)
                c_group.save()
                for r_csv_value in r_group_values:
                    # Create new program
                    c_program = Program(
                        name=r_csv_value.program,
                        description=r_csv_value.description,
                        group=c_group,
                    )
                    c_program.save()

    def import_csv(self, input_csv_file: Union[InMemoryUploadedFile, Path]):
        """
        Imports a csv file saved in memory into the EPIC domain data.

        Args:
            input_csv_file (Union[InMemoryUploadedFile, Path]): File containing EPIC data.
        """
        reader = csv.DictReader(self.get_valid_csv_text(input_csv_file))
        keys = dict(
            area=reader.fieldnames[0],
            group=reader.fieldnames[1],
            program=reader.fieldnames[2],
            description=reader.fieldnames[3],
        )
        line_objects = []
        for row in reader:
            line_objects.append(self.CsvLineObject.from_dictreader_row(keys, row))
        self._cleanup_epic_domain()
        self._import_epic_domain(self.group_entity("area", line_objects))
