import pytest

import epic_app.models.models as epic_models
from epic_app.models.epic_questions import (
    EvolutionQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
    Question,
)


@pytest.fixture(autouse=False)
@pytest.mark.django_db
def epic_test_db():
    """
    Pytest automaticall sets and tears down this data for each test.
    (Or at least it should)
    """
    # Areas
    alpha_area = epic_models.Area(name="alpha")
    alpha_area.save()
    beta_area = epic_models.Area(name="beta")
    beta_area.save()

    # Agency
    tia_agency = epic_models.Agency(name="T.I.A.")
    tia_agency.save()
    cia_agency = epic_models.Agency(name="C.I.A.")
    cia_agency.save()
    mi6_agency = epic_models.Agency(name="M.I.6")
    mi6_agency.save()
    rws_agency = epic_models.Agency(name="R.W.S.")
    rws_agency.save()

    # Groups
    first_group = epic_models.Group(name="first", area=alpha_area)
    first_group.save()
    second_group = epic_models.Group(name="second", area=alpha_area)
    second_group.save()
    third_group = epic_models.Group(name="third", area=beta_area)
    third_group.save()

    # Programs
    a_program = epic_models.Program(
        name="a", group=first_group, description="May the Force be with you"
    )
    a_program.save()
    b_program = epic_models.Program(
        name="b",
        group=first_group,
        description="You're all clear, kid. Now blow this thing and go home!",
    )
    b_program.save()
    c_program = epic_models.Program(
        name="c", group=first_group, description="Do. Or do not. There is no try."
    )
    c_program.save()
    d_program = epic_models.Program(
        name="d",
        group=second_group,
        description="Train yourself to let go of everything you fear to lose.",
    )
    d_program.save()
    e_program = epic_models.Program(
        name="e", group=third_group, description="You will find only what you bring in."
    )
    e_program.save()
    a_program.agencies.add(cia_agency, tia_agency)
    b_program.agencies.add(cia_agency, tia_agency)
    c_program.agencies.add(cia_agency, rws_agency)
    d_program.agencies.add(mi6_agency, cia_agency)
    e_program.agencies.add(rws_agency, mi6_agency)

    # Add questions to program a (for instance).
    NationalFrameworkQuestion(
        title="Is this a National Framework question?",
        program=a_program,
        description="Commodo sint pariatur minim ea non nisi officia magna mollit officia.",
    ).save()
    NationalFrameworkQuestion(
        title="Is this another National Framework question?",
        program=a_program,
        description="In ut ea ex labore in proident cupidatat elit laboris veniam.",
    ).save()
    EvolutionQuestion(
        title="Is this an Evolution question?",
        program=a_program,
        nascent_description="Incididunt sunt sunt in commodo culpa cupidatat.",
        engaged_description="Cupidatat labore nulla irure consectetur aliquip cillum labore Lorem amet enim est laboris aliqua tempor.",
        capable_description="In do eu anim occaecat ad ut sit eiusmod magna cillum.",
        effective_description="Ipsum proident aliqua elit anim sit fugiat mollit amet.",
    ).save()
    EvolutionQuestion(
        title="Is this yet another Evolution question?",
        program=a_program,
        nascent_description="Esse occaecat cillum duis amet anim laboris labore magna ipsum.",
        engaged_description="Fugiat nulla culpa cillum esse consequat id irure laboris adipisicing esse veniam anim.",
        capable_description="Non officia eu ut enim veniam nulla nostrud in laborum sit eiusmod qui id.",
        effective_description="Velit aliqua laborum cillum ea fugiat mollit deserunt incididunt veniam cupidatat aute Lorem ea.",
    ).save()
    LinkagesQuestion(title="Finally a linkage question?", program=a_program).save()
