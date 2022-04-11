import pytest
from django.contrib.auth.models import User

from epic_app.models.epic_questions import (
    EvolutionQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
)
from epic_app.models.epic_user import EpicUser
from epic_app.models.models import Agency, Area, Group, Program


@pytest.fixture(autouse=False)
@pytest.mark.django_db
def epic_test_db():
    """
    Pytest automaticall sets and tears down this data for each test.
    (Or at least it should)
    """
    admin_user = User(
        username="admin",
        email="admin@testdb.com",
        first_name="Star",
        last_name="Lord",
    )
    admin_user.set_password("admin")
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    # Epic users (no admins)
    def set_epic_user(username: str, organization: str) -> EpicUser:
        u_created = EpicUser(username=username, organization=organization)
        u_created.set_password(username.lower())
        u_created.save()
        return u_created

    u_palpatine: EpicUser = set_epic_user("Palpatine", "Gallactic Empire")
    u_anakin: EpicUser = set_epic_user("Anakin", "Gallactic Empire")

    # Areas
    alpha_area = Area.objects.create(name="alpha")
    beta_area = Area.objects.create(name="beta")

    # Agency
    tia_agency = Agency.objects.create(name="T.I.A.")
    cia_agency = Agency.objects.create(name="C.I.A.")
    mi6_agency = Agency.objects.create(name="M.I.6")
    rws_agency = Agency.objects.create(name="R.W.S.")

    # Groups
    first_group = Group.objects.create(name="first", area=alpha_area)
    second_group = Group.objects.create(name="second", area=alpha_area)
    third_group = Group.objects.create(name="third", area=beta_area)

    # Programs
    a_program = Program.objects.create(
        name="a", group=first_group, description="May the Force be with you"
    )
    b_program = Program.objects.create(
        name="b",
        group=first_group,
        description="You're all clear, kid. Now blow this thing and go home!",
    )
    c_program = Program.objects.create(
        name="c", group=first_group, description="Do. Or do not. There is no try."
    )
    d_program = Program.objects.create(
        name="d",
        group=second_group,
        description="Train yourself to let go of everything you fear to lose.",
    )
    e_program = Program.objects.create(
        name="e", group=third_group, description="You will find only what you bring in."
    )
    a_program.agencies.add(cia_agency, tia_agency)
    b_program.agencies.add(cia_agency, tia_agency)
    c_program.agencies.add(cia_agency, rws_agency)
    d_program.agencies.add(mi6_agency, cia_agency)
    e_program.agencies.add(rws_agency, mi6_agency)

    # Set programs:
    u_palpatine.selected_programs.add(a_program)
    u_palpatine.selected_programs.add(c_program)
    u_anakin.selected_programs.add(b_program)
    u_anakin.selected_programs.add(d_program)

    # Add questions to program a (for instance).
    NationalFrameworkQuestion.objects.create(
        title="Is this a National Framework question?",
        program=a_program,
        description="Commodo sint pariatur minim ea non nisi officia magna mollit officia.",
    )
    NationalFrameworkQuestion.objects.create(
        title="Is this another National Framework question?",
        program=a_program,
        description="In ut ea ex labore in proident cupidatat elit laboris veniam.",
    )
    EvolutionQuestion.objects.create(
        title="Is this an Evolution question?",
        program=a_program,
        nascent_description="Incididunt sunt sunt in commodo culpa cupidatat.",
        engaged_description="Cupidatat labore nulla irure consectetur aliquip cillum labore Lorem amet enim est laboris aliqua tempor.",
        capable_description="In do eu anim occaecat ad ut sit eiusmod magna cillum.",
        effective_description="Ipsum proident aliqua elit anim sit fugiat mollit amet.",
    )
    EvolutionQuestion.objects.create(
        title="Is this yet another Evolution question?",
        program=a_program,
        nascent_description="Esse occaecat cillum duis amet anim laboris labore magna ipsum.",
        engaged_description="Fugiat nulla culpa cillum esse consequat id irure laboris adipisicing esse veniam anim.",
        capable_description="Non officia eu ut enim veniam nulla nostrud in laborum sit eiusmod qui id.",
        effective_description="Velit aliqua laborum cillum ea fugiat mollit deserunt incididunt veniam cupidatat aute Lorem ea.",
    )
    LinkagesQuestion.objects.create(
        title="Finally a linkage question?", program=a_program
    )
