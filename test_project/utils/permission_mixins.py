from test_project.users.models import User


def check_permission_role(request):
    if request.user.permission_role == User.PermissionChoices.Admin:
        return True
    elif request.user.permission_role == User.PermissionChoices.Restaurant:
        return True
    elif request.user.permission_role == User.PermissionChoices.Employee:
        return False
