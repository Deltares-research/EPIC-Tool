from django.contrib import admin

from epic_app.admin_models.generate_entity_admin import EpicOrganizationAdmin, LnkAdmin
from epic_app.admin_models.import_entity_admin import (
    AgencyAdmin,
    AreaAdmin,
    EvoAdmin,
    KaaAdmin,
    NfqAdmin,
)
from epic_app.models.epic_answers import (
    MultipleChoiceAnswer,
    SingleChoiceAnswer,
    YesNoAnswer,
)
from epic_app.models.epic_questions import (
    EvolutionQuestion,
    KeyAgencyActionsQuestion,
    LinkagesQuestion,
    NationalFrameworkQuestion,
)
from epic_app.models.epic_user import EpicOrganization, EpicUser
from epic_app.models.models import Agency, Area, Group, Program

# Models exposed to the admin page .
admin.site.register(EpicUser)
admin.site.register(EpicOrganization, EpicOrganizationAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(Group)
admin.site.register(Program)
admin.site.register(NationalFrameworkQuestion, NfqAdmin)
admin.site.register(KeyAgencyActionsQuestion, KaaAdmin)
admin.site.register(EvolutionQuestion, EvoAdmin)
admin.site.register(LinkagesQuestion, LnkAdmin)
admin.site.register(YesNoAnswer)
admin.site.register(SingleChoiceAnswer)
admin.site.register(MultipleChoiceAnswer)
