import io
from pathlib import Path
from typing import Any, Dict, List, Protocol, Tuple, Union, runtime_checkable

from django.core.files.uploadedfile import InMemoryUploadedFile


@runtime_checkable
class ProtocoEpicImporter(Protocol):
    class CsvLineObject:
        pass

    def import_csv(self, input_csv_file: Union[InMemoryUploadedFile, Path]):
        pass


class BaseEpicImporter:
    class CsvLineObject:
        pass

    def import_csv(self, input_csv_file: Union[InMemoryUploadedFile, Path]):
        pass

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

    def get_valid_csv_text(
        self, input_csv_file: Union[InMemoryUploadedFile, Path]
    ) -> io.StringIO:
        """
        Gets a valid csv StringIo text from either source.

        Args:
            input_csv_file (Union[InMemoryUploadedFile, Path]): Different IO source.

        Returns:
            io.StringIO: Stream of decoded CSV text.
        """
        if not isinstance(input_csv_file, Path):
            return io.StringIO(input_csv_file.read().decode("utf-8"))
        return io.StringIO(input_csv_file.read_text(encoding="utf-8"))
