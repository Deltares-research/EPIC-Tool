import itertools
from typing import Type

from django.db import models


def get_submodel_type_list(model: Type[models.Model]) -> Type[models.Model]:
    subtypes = []
    for m in model.__subclasses__():
        if m.__subclasses__():
            subtypes.append(m.__subclasses__())
        else:
            subtypes.append([m])
    return list(itertools.chain(*subtypes))


def get_submodel_type(model_type: Type[models.Model], pk: str) -> Type[models.Model]:
    l_subtypes = get_submodel_type_list(model_type)
    sm_type = next(
        (q_t for q_t in l_subtypes if q_t.objects.filter(pk=pk).exists()),
        None,
    )
    return sm_type


def get_instance_as_submodel_type(model_instance: models.Model) -> models.Model:
    submodel_type = get_submodel_type(type(model_instance), model_instance.pk)
    return submodel_type.objects.get(pk=model_instance.pk)
