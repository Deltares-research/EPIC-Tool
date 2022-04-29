import io
from pathlib import Path
from typing import Any, Dict, List, Protocol, Tuple, Union, runtime_checkable

import openpyxl
from django.core.files.uploadedfile import InMemoryUploadedFile
from openpyxl.cell import Cell


@runtime_checkable
class ProtocolEpicImporter(Protocol):
    class XlsxLineObject:
        pass

    def import_file(self, input_file: Union[InMemoryUploadedFile, Path]):
        pass


class BaseEpicImporter:
    class XlsxLineObject:
        @staticmethod
        def get_valid_cell(xlsx_row: List[Cell], cell_pos: int) -> str:
            try:
                return xlsx_row[cell_pos].value.strip()
            except:
                return ""

        @classmethod
        def from_xlsx_row(cls, xlsx_row: Any):
            raise NotImplementedError("Implement in concrete class.")

    def _get_xlsx_line_objects(
        self, input_file: Union[InMemoryUploadedFile, Path]
    ) -> List[XlsxLineObject]:
        """
        Gets all the Xlsx lines into our custom `XlsxLineObject`.

        Args:
            input_file (Union[InMemoryUploadedFile, Path]): File to parse.

        Returns:
            List[XlsxLineObject]: Resulting list of parsed objects.
        """
        loaded_workbook: openpyxl.Workbook = openpyxl.load_workbook(input_file)
        loaded_sheet = loaded_workbook.active
        return list(map(self.XlsxLineObject.from_xlsx_row, loaded_sheet.rows))

    def import_file(self, input_file: Union[InMemoryUploadedFile, Path]):
        """
        Imports an xlsx file saved in memory or as a path into the EPIC domain data.

        Args:
            input_file (Union[InMemoryUploadedFile, Path]): File containing EPIC data.
        """
        raise NotImplementedError("Implement in concrete class.")

    def tuple_to_dict(
        self, tup_lines: List[Tuple[str, List[Any]]]
    ) -> Dict[str, List[Any]]:
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

    def group_entity(
        self, group_key: str, data_read: List[Any]
    ) -> Dict[str, List[Any]]:
        """
        Creates a dictionary grouping the data_read by the group_key representing an attribute of the objects.

        Args:
            group_key (str): Attribute of the list of objects.
            data_read (List[Any]): List of objects that needs to be grouped.

        Returns:
            Dict[str, List[Any]]: Resulting dictionary.
        """
        tuple_list = [(x.__dict__[group_key], x) for x in data_read]
        return self.tuple_to_dict(tuple_list)
