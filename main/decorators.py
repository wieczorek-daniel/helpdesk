from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied


def group_required(*group_names, login_url=None, raise_exception=False):
    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)):
                return True
            if raise_exception:
                raise PermissionDenied
        return False

    return user_passes_test(in_groups, login_url='/login')
