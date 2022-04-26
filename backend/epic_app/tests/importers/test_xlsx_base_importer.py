from io import BytesIO

import pytest

from epic_app.importers import BaseEpicImporter
from epic_app.importers.xlsx_base_importer import ProtocolEpicImporter


class TestBaseEpicImporter:
    @pytest.mark.django_db
    def test_epic_agency_importer(self):
        base_importer = BaseEpicImporter()
        assert isinstance(base_importer, ProtocolEpicImporter)
