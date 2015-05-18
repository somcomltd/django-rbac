from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, Group

from rbac.models import RBACRole, RBACOperation, RBACPermission, RBACGenericPermission


def users_are_friends(user, target_user):
    return False

def users_are_coworkers(user, target_user):
    return True

def get_user_roles(user, target_user):
    roles = []
    if users_are_friends(user, target_user):
        roles.append(RBACRole.objects.get(name='friends'))
    if users_are_coworkers(user, target_user):
        roles.append(RBACRole.objects.get(name='coworkers'))
    return roles

def my_view(request):
    """Displays info details from nabuco user"""

    owner, c = User.objects.get_or_create(username='nabuco')

    # Owner of the object has full permissions, otherwise check RBAC
    if request.user != owner:

        # Get roles
        roles = get_user_roles(request.user, owner)
        # Get operation
        op, c = RBACOperation.objects.get_or_create(name='display')

        # Per-model permission:
        # Has user permission to display groups that nabuco belongs to?
        if not RBACGenericPermission.objects.get_permission(owner, Group, op, roles):
            return HttpResponseForbidden("Sorry, you are not allowed to see nabuco groups")

        # Per-object permission:
        # Has user permission to see this group which nabuco belong to?
        group_inst = get_object_or_404(Group, name='punks')
        if not RBACPermission.objects.get_permission(owner, owner, op, roles):
            return HttpResponseForbidden("Sorry, you are not allowed to see this group details")

    return render_to_response("base.html",
                              {'owner': owner,
                               'model': Group,
                               'model_inst': owner,
                               'operation': op,
                               'roles': roles},
                              context_instance=RequestContext(request))
