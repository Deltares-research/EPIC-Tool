from rest_framework import permissions


class IsAdminOrSelfUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return (
            bool(request.user and request.user.is_staff)
            or str(request.user.pk) == view.kwargs["pk"]
        )
