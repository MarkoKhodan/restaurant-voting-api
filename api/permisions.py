from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsRestaurantStaffOrIfAuthenticatedReadOnly(BasePermission):
    """
    Allows access only to restraurants staff.
    """

    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_restaurant_staff)
        )


class IsEmployee(BasePermission):
    """
    Allows access only for employees.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_employee)
