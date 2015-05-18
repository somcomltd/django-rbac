Usage in views
==============

The ``example`` folder is a Django project with a ``myapp`` app that
contains a ``views.py``. Inspect this file to see how you can
integrate django-rbac in your views.

If you want to try out the example project, you first have to run Django
``syncdb`` commad to create all the tables and everything else on
the SQLite database::

    python manage.py syncdb

After that, load the fixture that comes in the ``myapp/fixtures`` folder::

    ./manage.py loaddata myapp/fixtures/initial_data.json

Finally, run your development server and access the view at /myapp/ with
your browser to test. Play around changing the code to see how it works::

    http://localhost:8000/myapp/

Usage in templates
==================

First load the template tags with the ``load`` statement::

    {% load rbac_tags %}

There are two template tags, one for RBAC object-level permissions and
another one for RBAC model-level (generic) permissions. Syntax is::

    {% if_rbac_permission owner model_inst operation roles %}
        ...
    {% else %}
        ---
    {% endif_rbac_permission %}

    {% if_rbac_generic_permission owner model operation roles %}
        ...
    {% else %}
        ---
    {% endif_rbac_generic_permission %}

Take a look at the example project for an example on how to use them
from the ``templates/base.html`` template, having received the
arguments from the ``my_view`` view.

Usage in shell
==============

::

    # This use case is about defining a RBAC system for users  who want to
    # restrict display of their group memberships and profile info access.
    >>> from rbac.models import RBACRole, RBACOperation
    >>> from rbac.models import RBACPermission, RBACGenericPermission
    # Create an operation to define display of objects:
    >>> operation = RBACOperation.objects.create(name='display')
    # Create some roles:
    >>> RBACRole.objects.create(name='friend')
    <RBACRole: friend>
    >>> RBACRole.objects.create(name='coworker')
    <RBACRole: coworker>
    >>> RBACRole.objects.create(name='family')
    <RBACRole: family>
    # As an example of a generic permission (per-model permissions),
    # we will restrict access to all user groups only to certain roles
    >>> from django.contrib.auth.models import User, Group
    # Create a user that will act as the owner:
    >>> owner = User.objects.create(username='hector')
    # Add some groups to the owner:
    >>> group1 = Group.objects.create(name='punks')
    >>> group2 = Group.objects.create(name='rockers')
    >>> owner.groups.add(group1)
    >>> owner.groups.add(group2)
    # Create generic permission: hector (owner) allows his friends, coworkers
    # and family (roles) to display (operation) his groups (django Group model)
    >>> roles = RBACRole.objects.all()
    >>> RBACGenericPermission.objects.create_permission(owner, Group, operation, roles)
    <RBACGenericPermission: hector | group | display>
    # Check if a user with given roles is authorized to perform the
    # operation 'display':
    >>> RBACGenericPermission.objects.get_permission(owner, Group, operation, roles)
    True
    # Create a new role and verivy that we are not allowed if trying to access
    # with only this role in the role list:
    >>> RBACRole.objects.create(name='classmate')
    <RBACRole: classmate>
    # Note below that, although we get only one role object, still we need to pass
    # it inside a queryset list.
    >>> roles = RBACRole.objects.filter(name='classmate')
    >>> RBACGenericPermission.objects.get_permission(owner, Group, operation, roles)
    False
    # As an example of a per-object permission, we will restrict which roles
    # are allowed to display the owner's user details.
    # If no permission exists for any of the given roles, the manager method
    # returns False, according to the django-rbac golden rule:
    # if a permission doesn't exist, the operation is denied.
    # Also note that we are passing a model instance this time (owner, which is
    # a User model instance)
    >>> RBACPermission.objects.get_permission(owner, owner, operation, roles)
    False
    # Create permission: hector (owner) allows only his friends (roles) to
    # display (operation) his user info (django User model instance)
    >>> roles = RBACRole.objects.filter(name='friend')
    >>> RBACPermission.objects.create_permission(owner, owner, operation, roles)
    <RBACPermission: hector | hector | display>
    >>> RBACPermission.objects.get_permission(owner, owner, operation, roles)
    True
