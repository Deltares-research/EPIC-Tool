import csv
from pathlib import Path
from typing import List, Union

from django.core.files.uploadedfile import InMemoryUploadedFile

from epic_app.importers.csv_base_importer import BaseEpicImporter
from epic_app.models.epic_questions import (
    EvolutionQuestion,
    KeyAgencyActionsQuestion,
    NationalFrameworkQuestion,
    Question,
)
from epic_app.models.models import Program


class _YesNoJustifyQuestionImporter(BaseEpicImporter):
    class CsvLineObject:
        program: str
        question: str
        description: str

        @classmethod
        def from_dictreader_row(cls, dict_keys: dict, dict_row: dict):
            new_line = cls()
            new_line.program = dict_row.get(dict_keys["program"]).strip()
            new_line.question = dict_row.get(dict_keys["question"]).strip()
            new_line.description = dict_row.get(dict_keys["description"]).strip()
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

    def _get_type(self) -> Question:
        pass

    def _cleanup_questions(self):
        self._get_type().objects.all().delete()

    def _import_questions(self, imported_questions: List[CsvLineObject]):
        for q_question in imported_questions:
            # Create new question
            if not Program.objects.filter(name=q_question.program).exists():
                raise ValueError(
                    f"Program '{q_question.program}' not found, import can't go through."
                )
            p_found = Program.objects.filter(name=q_question.program).first()
            c_area = self._get_type()(
                title=q_question.program,
                description=q_question.description,
                program=p_found,
            )
            c_area.save()


class NationalFrameworkQuestionImporter(_YesNoJustifyQuestionImporter):
    def _get_type(self) -> Question:
        return NationalFrameworkQuestion


class KeyAgencyActionsQuestionImporter(_YesNoJustifyQuestionImporter):
    def _get_type(self) -> Question:
        return KeyAgencyActionsQuestion


class EvolutionQuestionImporter(BaseEpicImporter):
    class CsvLineObject:
        program: str
        question: str
        nascent_description: str
        engaged_description: str
        capable_description: str
        effective_description: str

        @classmethod
        def from_dictreader_row(cls, dict_keys: dict, dict_row: dict):
            new_line = cls()
            new_line.program = dict_row.get(dict_keys["program"]).strip()
            new_line.question = dict_row.get(dict_keys["question"]).strip()
            new_line.nascent_description = dict_row.get(
                dict_keys["nascent_description"]
            ).strip()
            new_line.engaged_description = dict_row.get(
                dict_keys["engaged_description"]
            ).strip()
            new_line.capable_description = dict_row.get(
                dict_keys["capable_description"]
            ).strip()
            new_line.effective_description = dict_row.get(
                dict_keys["effective_description"]
            ).strip()
            return new_line

    def import_csv(self, input_csv_file: Union[InMemoryUploadedFile, Path]):
        reader = csv.DictReader(self.get_valid_csv_text(input_csv_file))
        keys = dict(
            program=reader.fieldnames[0],
            question=reader.fieldnames[1],
            nascent_description=reader.fieldnames[2],
            engaged_description=reader.fieldnames[3],
            capable_description=reader.fieldnames[4],
            effective_description=reader.fieldnames[5],
        )
        line_objects = []
        for row in reader:
            line_objects.append(self.CsvLineObject.from_dictreader_row(keys, row))
        self._cleanup_questions()
        self._import_questions(line_objects)

    def _cleanup_questions(self):
        EvolutionQuestion.objects.all().delete()

    def _import_questions(self, imported_questions: List[CsvLineObject]):
        for q_question in imported_questions:
            # Create new question
            if not Program.objects.filter(name=q_question.program).exists():
                raise ValueError(
                    f"Program '{q_question.program}' not found, import can't go through."
                )
            p_found = Program.objects.filter(name=q_question.program).first()
            c_area = EvolutionQuestion(
                title=q_question.question,
                nascent_description=q_question.nascent_description,
                engaged_description=q_question.engaged_description,
                capable_description=q_question.capable_description,
                effective_description=q_question.effective_description,
                program=p_found,
            )
            c_area.save()
