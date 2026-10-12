
from django.core.exceptions import PermissionDenied

from .models import FacilityMembership


def get_user_facility(request):
    """Return the active facility assigned to the logged-in user."""
    if not request.user.is_authenticated:
        raise PermissionDenied("Login is required.")

    memberships = FacilityMembership.objects.filter(
        user=request.user,
        is_active=True,
        facility__is_active=True,
    ).select_related("facility")

    # Do not silently choose a facility if the user has multiple memberships.
    if memberships.count() != 1:
        raise PermissionDenied(
            "Your account must have exactly one active facility "
            "assignment to use this page."
        )

    return memberships.first().facility
