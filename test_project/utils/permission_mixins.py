def check_permission_role(request):
    if request.user.permission_role == "admin":
        return True
    elif request.user.permission_role == "restaurnat":
        return True
    elif request.user.permission_role == "employee":
        return False
