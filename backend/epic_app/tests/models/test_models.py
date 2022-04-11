import pytest
from django.contrib.auth.models import User
from django.forms import ValidationError

import epic_app.models.models as epic_models
from epic_app.tests.epic_db_fixture import epic_test_db


@pytest.fixture(autouse=True)
def EpicModelsFixture(epic_test_db: pytest.fixture):
    """
    Dummy fixture just to load a default db from dummy_db.

    Args:
        epic_test_db (pytest.fixture): Fixture to load for the whole file tests.
    """
    pass


@pytest.mark.django_db
class TestEpicUser:
    def test_init_epicuser(self):
        created_user = epic_models.EpicUser.objects.create(
            username="Luke", organization="Rebel Alliance"
        )
        assert isinstance(created_user, epic_models.EpicUser)
        assert isinstance(created_user, User)
        assert created_user.is_superuser is False


@pytest.mark.django_db
class TestArea:
    def test_area_get_groups(self):
        alpha_area: epic_models.Area = epic_models.Area.objects.filter(
            name="alpha"
        ).first()
        assert isinstance(alpha_area, epic_models.Area)
        assert len(alpha_area.get_groups()) == 2
        group_names = [alpha_group.name for alpha_group in alpha_area.get_groups()]
        assert "first" in group_names
        assert "second" in group_names
        assert str(alpha_area) == "alpha"

    def test_delete_area_deletes_in_cascade(self):
        alpha_area: epic_models.Area = epic_models.Area.objects.filter(
            name="alpha"
        ).first()
        assert isinstance(alpha_area, epic_models.Area)

        # Delete model
        epic_models.Area.delete(alpha_area)

        # Verify cascade effect.
        assert not epic_models.Area.objects.filter(name="alpha").exists()
        # Groups deleted.
        assert not epic_models.Group.objects.filter(name="first").exists()
        assert not epic_models.Group.objects.filter(name="second").exists()
        # Programs deleted
        assert not epic_models.Program.objects.filter(name="a").exists()
        assert not epic_models.Program.objects.filter(name="b").exists()
        assert not epic_models.Program.objects.filter(name="c").exists()
        assert not epic_models.Program.objects.filter(name="d").exists()


@pytest.mark.django_db
class TestAgency:
    def test_agency_get_programs(self):
        tia_agency: epic_models.Agency = epic_models.Agency.objects.filter(
            name="T.I.A."
        ).first()
        assert isinstance(tia_agency, epic_models.Agency)
        assert len(tia_agency.get_programs()) == 2
        program_names = [tia_program.name for tia_program in tia_agency.get_programs()]
        assert "a" in program_names
        assert "b" in program_names
        assert str(tia_agency) == "T.I.A."

    def test_delete_agency_does_not_delete_in_cascade(self):
        tia_agency: epic_models.Agency = epic_models.Agency.objects.filter(
            name="T.I.A."
        ).first()
        assert isinstance(tia_agency, epic_models.Agency)
        epic_models.Agency.delete(tia_agency)

        # Verify elements still exist
        program_names = ["a", "b"]
        for p_name in program_names:
            p_program: epic_models.Program = epic_models.Program.objects.filter(
                name=p_name
            ).first()
            assert isinstance(p_program, epic_models.Program)
            assert not p_program.agencies.filter(name="T.I.A.").exists()


@pytest.mark.django_db
class TestGroup:
    def test_group_get_programs(self):
        second_group: epic_models.Group = epic_models.Group.objects.filter(
            name="second"
        ).first()
        assert isinstance(second_group, epic_models.Group)
        assert isinstance(second_group.area, epic_models.Area)
        assert second_group.area.name == "alpha"
        assert len(second_group.get_programs()) == 1
        assert "d" == second_group.get_programs()[0].name
        assert str(second_group) == "second"

    def test_delete_group_deletes_in_cascade(self):
        second_group: epic_models.Group = epic_models.Group.objects.filter(
            name="second"
        ).first()
        area = second_group.area
        assert isinstance(second_group, epic_models.Group)

        # Delete element
        epic_models.Group.delete(second_group)

        # Verify elements still exist
        assert not epic_models.Program.objects.filter(name="d").exists()
        assert epic_models.Area.objects.filter(name=area.name).exists()


@pytest.mark.django_db
class TestProgram:
    def test_program_data(self):
        program: epic_models.Program = epic_models.Program.objects.filter(
            name="e"
        ).first()
        assert isinstance(program, epic_models.Program)
        assert all(
            isinstance(p_agency, epic_models.Agency)
            for p_agency in program.agencies.all()
        )
        assert program.agencies.filter(name="R.W.S.").exists()
        assert isinstance(program.group, epic_models.Group)
        assert program.group.name == "third"
        assert program.description == "You will find only what you bring in."

    def test_program_delete_does_not_delete_in_cascade(self):
        program: epic_models.Program = epic_models.Program.objects.filter(
            name="e"
        ).first()
        g_name: str = program.group.name
        a_name: str = program.agencies.all().first().name
        assert isinstance(program, epic_models.Program)
        epic_models.Program.delete(program)
        assert not epic_models.Program.objects.filter(name="e").exists()
        assert epic_models.Agency.objects.filter(name=a_name).exists()
        assert epic_models.Group.objects.filter(name=g_name).exists()

    @pytest.mark.parametrize(
        "name_case",
        [
            pytest.param("a simple case", id="lowercase"),
            pytest.param("A Simple Case", id="camelCase"),
            pytest.param("A SIMPLE CASE", id="UPPERCASE"),
        ],
    )
    def test_program_unique_name_attribute(self, name_case: str):
        # Create one new program
        a_group: epic_models.Group = epic_models.Group.objects.all().first()
        a_description = "Lorem ipsum"
        a_name = "A simple case"
        a_simple_case_program = epic_models.Program(
            name=a_name, group=a_group, description=a_description
        )
        a_simple_case_program.save()
        assert epic_models.Program.objects.filter(
            name=a_simple_case_program.name
        ).exists()

        # Try adding a new instance with the same name but different case.
        with pytest.raises(ValidationError) as e_info:
            epic_models.Program(
                name=name_case, group=a_group, description=a_description
            ).save()
        assert (
            str(e_info.value.message)
            == f"There's already a Program with the name: {a_name}."
        )
        assert not epic_models.Program.objects.filter(name=name_case).exists()
