import random
from typing import List

import pytest
from django.contrib.auth.models import User
from django.http import FileResponse
from rest_framework.test import APIClient

from epic_app.models.epic_answers import (
    MultipleChoiceAnswer,
    SingleChoiceAnswer,
    YesNoAnswer,
    YesNoAnswerType,
)
from epic_app.models.epic_questions import (
    EvolutionChoiceType,
    EvolutionQuestion,
    LinkagesQuestion,
    YesNoQuestion,
)
from epic_app.models.epic_user import EpicOrganization, EpicUser
from epic_app.models.models import Program
from epic_app.tests import test_data_dir
from epic_app.tests.importers.epic_domain_importer_fixture import full_epic_domain_data
from epic_app.utils import get_instance_as_submodel_type


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
def set_user_auth_token(api_client: APIClient, username: str) -> str:
    epic_user = User.objects.get(username=username)
    assert epic_user
    token_str = "Token " + epic_user.auth_token.key

    # Run request.
    api_client.credentials(HTTP_AUTHORIZATION=token_str)


justify_answer_list = [
    "Duis esse excepteur elit ad fugiat id quis enim dolore non aliquip et nulla dolor.",
    "Consequat officia veniam veniam deserunt reprehenderit occaecat incididunt et aute irure reprehenderit.",
    "Exercitation aute duis enim exercitation cillum.",
    "Commodo culpa incididunt non aliqua laboris dolor nostrud incididunt sunt dolor incididunt esse consectetur laborum.",
    "Sint est id qui proident et minim pariatur dolore.",
    "Veniam fugiat in non fugiat nulla consequat incididunt tempor pariatur do pariatur.",
    "Adipisicing nostrud quis qui eiusmod eiusmod enim aliqua ullamco irure in.",
    "Sit mollit qui nulla mollit elit pariatur officia nisi nulla do qui velit eiusmod.",
    "Velit in anim sit deserunt.",
    "Ea veniam incididunt sunt et do anim culpa anim commodo dolore minim fugiat elit enim.",
]


@pytest.fixture(autouse=False)
@pytest.mark.django_db
def _report_fixture(full_epic_domain_data: pytest.fixture):
    test_org: EpicOrganization = EpicOrganization.objects.create(
        name="Deltares Test Organization"
    )
    org_users = test_org.generate_users(12)
    select_programs_a = set(random.choices(Program.objects.all(), k=4))
    select_programs_b = set(random.choices(Program.objects.all(), k=4))
    select_programs_c = []
    select_programs_c.extend(select_programs_a)
    select_programs_c.extend(select_programs_b)
    select_programs_c = set(select_programs_c)

    def answer_yes_no(sel_user: EpicUser, yn_question: YesNoQuestion):
        YesNoAnswer.objects.create(
            user=sel_user,
            question=yn_question,
            short_answer=random.choice(list(YesNoAnswerType)),
            justify_answer=random.choice(justify_answer_list),
        )

    def answer_singlechoice(sel_user: EpicUser, sc_question: EvolutionQuestion):
        SingleChoiceAnswer.objects.create(
            user=sel_user,
            question=sc_question,
            selected_choice=random.choice(list(EvolutionChoiceType)),
            justify_answer=random.choice(justify_answer_list),
        )

    def answer_multiple_choice(sel_user: EpicUser, mc_question: LinkagesQuestion):
        mca = MultipleChoiceAnswer(
            user=sel_user,
            question=mc_question,
        )
        mca.save()
        sel_linkages = random.choices(
            Program.objects.all().values_list("id", flat=True), k=3
        )
        mca.selected_programs.add(*sel_linkages)

    def complete_programs(user_list: List[EpicUser], program_list: List[Program]):
        for p in program_list:
            for p_question in p.questions.all():
                q_instance = get_instance_as_submodel_type(p_question)
                if isinstance(q_instance, YesNoAnswer):
                    [answer_yes_no(sel_user, q_instance) for sel_user in user_list]
                if isinstance(q_instance, EvolutionQuestion):
                    [
                        answer_singlechoice(sel_user, q_instance)
                        for sel_user in user_list
                    ]
                if isinstance(q_instance, LinkagesQuestion):
                    [
                        answer_multiple_choice(sel_user, q_instance)
                        for sel_user in user_list
                    ]

    # Group A
    complete_programs(org_users[0:4], select_programs_a)
    # Group B
    complete_programs(org_users[4:8], select_programs_b)
    # Group A + B
    complete_programs(org_users[8:], select_programs_c)

    advisor_user = EpicUser(
        username="advisor_test", organization=test_org, is_advisor=True
    )
    advisor_user.set_password("advisor_test")
    advisor_user.save()


@pytest.mark.django_db
class TestGeneratePdfReport:
    url_root = "/api/epicorganization/report-pdf/"

    def test_RETRIEVE_pdf_report_As_Advisor_epic_user(
        self, _report_fixture: dict, api_client: APIClient
    ):
        # Run request
        set_user_auth_token(api_client, "advisor_test")
        response: FileResponse = api_client.get(self.url_root)

        # Verify final expectations
        assert response.status_code == 200
        output_file = test_data_dir / response.filename
        if output_file.exists():
            output_file.unlink()
        fs = b"".join(response.streaming_content)
        with open(output_file, "wb") as f:
            f.write(fs)
        assert output_file.exists()
