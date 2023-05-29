from test_project.users.models import User


def check_permission_role(request, restaurant=None):
    if request.user.permission_role == User.PermissionChoices.Admin:
        return True
    if request.user.permission_role == User.PermissionChoices.RestaurantManager:
        if request.user.restaurant == restaurant:
            return True
    return False
