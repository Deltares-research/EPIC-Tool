import csv
import io
from typing import Any, Dict, List, Optional, Tuple, Union
from pathlib import Path
from django.core.files.uploadedfile import InMemoryUploadedFile
from epic_app.models import Area, Group, Program

def tuple_to_dict(tup_lines: List[Tuple[str, List[Any]]]) -> Dict[str, List[Any]]:
    """
    Transforms a list of tuples into a dictionary without removing any element.

    Args:
        tup_lines (List[Tuple[str, List[Any]]]): List of tuples where the first element represents a key to group by.

    Returns:
        Dict[str, List[Any]]: Resulting dictionary.
    """
    new_dict = {}
    for key, list_obj in tup_lines:
        new_dict.setdefault(key, []).append(list_obj)
    return new_dict

def group_entity(group_key: str, data_read: List[Any]) -> Dict[str, List[Any]]:
    """
    Creates a dictionary grouping the data_read by the group_key representing an attribute of the objects.

    Args:
        group_key (str): Attribute of the list of objects.
        data_read (List[Any]): List of objects that needs to be grouped.

    Returns:
        Dict[str, List[Any]]: Resulting dictionary.
    """
    tuple_list = [(x.__dict__[group_key], x) for x in data_read]
    return tuple_to_dict(tuple_list)

class EpicDomainImporter:
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
            read_groups = group_entity("group", r_area_values)
            for r_group, r_group_values in read_groups.items():
                # Create new group
                c_group = Group(name=r_group, area=c_area)
                c_group.save()
                read_programs = group_entity("program", r_group_values)
                for r_program in read_programs.keys():
                    # Create new program
                    c_program = Program(name=r_program, group=c_group)
                    c_program.save()

    def import_csv(self, input_csv_file: Union[InMemoryUploadedFile, Path]):
        """
        Imports a csv file saved in memory into the EPIC domain data.

        Args:
            input_csv_file (Union[InMemoryUploadedFile, Path]): File containing EPIC data.
        """
        if not isinstance(input_csv_file, Path):
            read_text = io.StringIO(input_csv_file.read().decode('utf-8'))
        else:
            read_text = io.StringIO(input_csv_file.read_text())
        reader = csv.DictReader(read_text)        
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
        self._import_epic_domain(group_entity("area", line_objects))
        