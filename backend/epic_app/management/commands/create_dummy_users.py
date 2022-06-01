import random
from typing import Any, List, Optional

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand

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
from epic_app.utils import get_instance_as_submodel_type


class Command(BaseCommand):
    help = "Generates dummy EpicUsers and a dummy admin with their usernames matching the password."

    def _create_superuser(self):
        """
        Creates an admin 'superuser' with classic 'admin'/'admin' user/pass.
        """
        # Create an admin user.
        admin_user = User(
            username="admin",
            email="admin@testdb.com",
            first_name="Ad",
            last_name="Min",
        )
        admin_user.set_password("admin")
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        self.stdout.write(
            self.style.SUCCESS("Created superuser: 'admin', password: 'admin'.")
        )

    def _create_dummy_users(self):
        try:
            self._create_superuser()
        except:
            call_command("createsuperuser")

        def set_password_and_log(e_user: EpicUser):
            e_user.set_password(e_user.username.lower())
            self.stdout.write(
                self.style.SUCCESS(
                    "Created user: '{}' with password: {}".format(
                        e_user.username, e_user.username.lower()
                    )
                )
            )

        test_org: EpicOrganization = EpicOrganization.objects.create(
            name="Deltares Test Organization"
        )
        self.stdout.write(
            self.style.SUCCESS("Created organization: '{}'".format(test_org.name))
        )
        epic_users: List[EpicUser] = test_org.generate_users(10)
        for e_n, e_user in enumerate(epic_users[:2]):
            e_user.username = "advisor_{}".format(e_n)
            e_user.is_advisor = True
        [set_password_and_log(e_user) for e_user in epic_users]
        self._fill_up_test_data(epic_users)

    def _fill_up_test_data(self, org_users: List[EpicUser]):
        program_list = set(Program.objects.all())
        select_programs_a = set(random.choices(list(program_list), k=6))
        select_programs_b = set(
            random.choices(list(program_list - select_programs_a), k=6)
        )
        select_programs_c = set(list(select_programs_a) + list(select_programs_b))

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

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            self._create_dummy_users()
        except Exception as e_info:
            self.stdout.write(
                self.style.ERROR(f"Error setting up EPIC. Detailed info: {str(e_info)}")
            )
