import itertools
from typing import Type

from django.db import models


def get_model_subtypes(model: Type[models.Model]) -> Type[models.Model]:
    subtypes = []
    for m in model.__subclasses__():
        if m.__subclasses__():
            subtypes.append(m.__subclasses__())
        else:
            subtypes.append([m])
    return list(itertools.chain(*subtypes))
