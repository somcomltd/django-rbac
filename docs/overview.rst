Overview
========

First of all, I would like to show some drawbacks of
Django's current permission system:

* Permissions are tied directly to the ``User`` model from
  ``django.contrib.auth``, so you cannot use any other existing
  model in your application.
* The task of mantaining this list of permissions in the current Django system
  is responsibility of a superuser or some other kind of centralized entity.

* You can certainly assign permissions to ``Group`` model instances, but all
  users in this group will share the same permissions.

* Last, but not least, until Django v1.2 will come and ticket `#11010`_
  implemented, the permission system is model-level -- it doesn't allow granular
  permissions (row-level), which means you can give a user authorization to do
  something based on all instances of a model class, but not to a
  single model instance (an object).

Many applications, and specially today's web applications -- which involve
concepts as collaboration or content driven by the users -- need the flexibility
to support delegation of permission granting to objects by other trusted agents.
A clear example is a social networking site, where the users want to allow or
deny access to their profiles or pictures, open or close their different
communication channels like receiving friendship requests or private messages.
django-rbac tries to champion this by introducing some key features from the
Role-Based Access Control (RBAC_) proposal. In this implementation users
(subjects) are assigned different roles that, in turn, have (or not) privileges
over objects. With this permission system, the owner of an object can give
privileges to certain roles. For example, a user can grant access to other users
trying to read some personal info only if they belong to, at least, one of
the roles specified in the permission rule. 

I initially developed the first version of this app for a social network, to
give its users the ability to control who has privileges upon their profiles,
photo albums, personal information, and such. If you are in a similar situation,
you'll find that django-rbac suits perfect for your purposes. But, as long as a
general-purpose access control is being implemented, even if you are building
any other kind of application which needs this level of permission control,
django-rbac will help you out. I think I have made it enough generic to match a
wide range of use cases.

I you are interested, you can read the `introduced formal model`_ by
F. Ferraiolo and D. R. Kuhn.

.. _#11010: http://code.djangoproject.com/ticket/11010
.. _RBAC: http://csrc.nist.gov/groups/SNS/rbac/
.. _introduced formal model: http://csrc.nist.gov/groups/SNS/rbac/documents/Role_Based_Access_Control-1992.html

Download & Installation
=======================

Stable code
-----------

You can use your favorite management tool to install (the old and well-known
easy_install or the better pip::

    easy_install django-rbac
    pip install django-rbac

Or you can download and install the source code yourself
(``python setup.py install``) from here::

    http://bitbucket.org/nabucosound/django-rbac/downloads/

Latest Development code
-----------------------

Source code is hosted in Bitbucket here_.

Install Mercurial_ if you don't have it yet, and clone the repository::

    hg clone http://bitbucket.org/nabucosound/django-rbac/
    
Symlink to the folder called ``rbac`` inside ``django-rbac`` from somewhere
in your PYTHONPATH -- could be the system-wide ``site-packages`` python folder,
or the path your virtualenv project is using, if you are using Virtualenv_
(which I strongly encourage). And if you do and are also using
Virtualenvwrapper_ then you can easily ``add2virtualenv``.

.. _here: http://bitbucket.org/nabucosound/django-rbac/
.. _Mercurial: http://www.selenic.com/mercurial/
.. _Virtualenv: http://pypi.python.org/pypi/virtualenv/
.. _Virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/

Dependencies
============

Be sure you have ``django.contrib.contenttypes`` installed in you project.

Overview
========

The following elements conform a RBAC permission in django-rbac:

1. The **owner**: The proprietary of either the object being accessed or the
   permission rule itself, e.g. a site user or a community administrator.

2. The **object**: The element being accessed on which the permission is being
   checked upon, e.g. a profile or photo album.

3. The **operation**: The action requested, e.g. display, create, delete, show
   birth date, send message or request friendship.

4. The **roles**: Define who are the requesting users in relation to the owner
   or the object, e.g anonymous, friend, family, coworker, or roommate.

This is best explained with a simple example:

* User *Fritz* wants to see *Mr. Natural's* profile. Thus, *Fritz* (subject)
  requests permission to access (**operation**) the profile (**object**) of
  *Mr. Natural* (**owner**).
* *Fritz* is an 'anonymous' user (**role**), a role that everybody holds
  initially in the system. As *Fritz* and *Mr. Natural* are friends, the role
  'friend' is appended to the **roles**. So we have a role list containing
  'anonymous' and 'friend'.
* The privacy framework performs its magic to pull an answer: has *Fritz*
  permission to access this profile?

    - For the 'anonymous' role, the system denies the access.
    - For the 'friend' role the access is granted, as *Mr. Natural* had set
      access only to friends to his profile.
* Access is granted, so *Fritz* can go ahead and view all the stuff.

Permissions can be assigned to either a single object ("per-object permission"
category, also known as "granular permissions" or "row level permissions")
like in the example above, or to all objects of the same model class. For this
reason, django-rbac implements two classes respectively:
``RBACPermission`` and ``RBACGenericPermission``.

How it works
============

Asking for permission in django-rbac is a 2-step process:

1. Get the roles: The user that tries to perform the operation over an object
or model does so within a context given between him and the owner or the
object/model itself. You have to provide a python list of ``RBACRole``
objects to the function that will later check authorization.
2. Call the ``get_permission`` method from one of the two RBAC permission
objects (``RBACPermission.objects.get_permission`` or
``RBACGenericPermission.objects.get_permission``). The method will return
``True`` or ``False`` if the operation is authorized or not.

You are totally responsible of executing step 1. The ways that roles can be
assigned to users are endless, particular to each application or project, so
django-rbac cannot provide any generic method to accomplish this task. Jump to
the subsection "Writing functions to get roles" in the "Roles" section for
more information.

Operations
==========

The ``RBACOperation`` model defines operations that can be done in the system,
e.g. 'display_profile', 'send_message', 'request_friendship', or 'show_email'.
You can define what you want, just try to stick to a common syntax convention
and short names for your own sake.

Roles
=====

Originally a role is a job function within the context of an organization, but
it can also be seen like a relationship between the requesting user (subject)
and the owner. Users trying to perform operations over objects can do so in
multiple fashions. For example, someone asks for permission to see, let's say,
a photo album from another user. Such requesting user can be friend or family
of the album owner, a member of a photography community, or maybe an anonymous
folk with a deep interest in other's pics. Thus, 'anonymous', 'friend',
'community_member' or 'family' would be names of ``RBACRole`` roles that users
can belong to.

Writing functions to get roles
------------------------------

You need to provide your app some programming logic to know which roles is the
requesting user going to play. A common case is the ``request.user`` in a
Django view. See this example extracted from the project that comes with the
django-rbac package in the ``example`` folder::

    from rbac.models import RBACRole
    
    def get_user_roles(user, target_user):
        roles = []
        # These two functions below would validate the relationship
        # between the two users.
        # If any exist, append the corresponding role to the roles
        # list to be returned.
        if users_are_friends(user, target_user):
            #Assuming 'friend' role object exists
            roles.append(RBACRole.objects.get(name='friend'))
        if users_are_coworkers(user, target_user):
            #Assuming 'coworker' role object exists
            roles.append(RBACRole.objects.get(name='coworker'))
        return roles

Permissions
===========

Once you have your operations and roles ready, you can start creating
permissions. RBAC enables the conditions for the implementaiton of what is
called the *Separation of Duties* (SoD), so tipically applications or projects
using django-rbac will set mechanisms to delegate creating new permissions
to owners. That is, the owner of an object will be who is setting the
permission level to all the operations that can be done with the object.
You are again responsible of providing the user an interface to accomplish
this task. Classical social networks, for example, give their users a
'privacy' page with forms to change different permission settings.

As mentioned in the beginning of this document, the scope of a permission can
be row level (``RBACPermission``) or model class level
(``RBACGenericPermission``). Both models receive:

* The model instance of the permission owner, e.g. a ``User`` object.
* An ``RBACOperation`` object for an operation, e.g. 'display_profile'.
* A list of ``RBACRole`` objects, e.g. 'anonymous', 'friend' and 'coworker'.
* The object: ``RBACPermission`` receives a model instance (for example, a
  ``Group`` object), while ``RBACGenericPermission`` receives a class model
  (for example, a ``Group`` model).

Two things to keep in mind when planning your permissions:

* django-rbac follows this golden rule: *if a permission doesn't exist, the
  operation is denied*. This is for convenience, because fewer permission
  objects need to be created.
* Try to avoid defining permissions that contain mutually exclusive roles.
  For example, a permission could have 'friend' and 'anonymous user' into his
  list of roles. The first allows the permission operation to everybody, while
  the second restricts an access only to friends, so both are mutually exclusive.

