import csv
from pathlib import Path
from typing import List, Union

from django.core.files.uploadedfile import InMemoryUploadedFile

from epic_app.importers.csv_base_importer import BaseEpicImporter
from epic_app.models.epic_questions import NationalFrameworkQuestion
from epic_app.models.models import Program


class NationalFrameworkQuestionImporter(BaseEpicImporter):
    class CsvLineObject:
        program: str
        question: str
        description: str

        @classmethod
        def from_dictreader_row(cls, dict_keys: dict, dict_row: dict):
            new_line = cls()
            new_line.program = dict_row.get(dict_keys["program"])
            new_line.question = dict_row.get(dict_keys["question"])
            new_line.description = dict_row.get(dict_keys["description"])
            return new_line

    def import_csv(self, input_csv_file: Union[InMemoryUploadedFile, Path]):
        reader = csv.DictReader(self.get_valid_csv_text(input_csv_file))
        keys = dict(
            program=reader.fieldnames[0],
            question=reader.fieldnames[1],
            description=reader.fieldnames[2],
        )
        line_objects = []
        for row in reader:
            line_objects.append(self.CsvLineObject.from_dictreader_row(keys, row))
        self._cleanup_questions()
        self._import_questions(line_objects)

    def _cleanup_questions(self):
        NationalFrameworkQuestion.objects.all().delete()

    def _import_questions(self, imported_questions: List[CsvLineObject]):
        for q_question in imported_questions:
            # Create new question
            if not Program.objects.filter(name=q_question.program).exists():
                raise ValueError(
                    f"Program '{q_question.program}' not found, import can't go through."
                )
            p_found = Program.objects.filter(name=q_question.program).first()
            c_area = NationalFrameworkQuestion(
                title=q_question.program,
                description=q_question.description,
                program=p_found,
            )
            c_area.save()


class EvolutionQuestionImporter(BaseEpicImporter):
    class CsvLineObject:
        program: str
        question: str
        description: str


class LinkagesQuestionImporter(BaseEpicImporter):
    class CsvLineObject:
        program: str
        question: str
        description: str
