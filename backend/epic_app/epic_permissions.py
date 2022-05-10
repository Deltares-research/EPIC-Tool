from django.http import HttpRequest
from rest_framework import permissions


def _is_admin(request: HttpRequest) -> bool:
    return bool(request.user and request.user.is_staff) or bool(
        request.user and request.user.is_superuser
    )


class IsAdminOrSelfUser(permissions.BasePermission):
    """
    Allows access only to admin users and the user itself.
    """

    def has_permission(self, request: HttpRequest, view):
        return _is_admin(request) or str(request.user.pk) == view.kwargs["pk"]


class IsInstanceOwner(permissions.BasePermission):
    """
    Allows access to admin users and users in the field `user` of an entity.
    """

    def has_permission(self, request: HttpRequest, view):
        return request.user.pk == view.get_object().user.pk
