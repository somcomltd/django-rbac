from django.contrib import admin
from rbac.models import Operation, Role, Relationship, Permission, GenericPermission


admin.site.register(Operation)
admin.site.register(Role)
admin.site.register(Relationship)
admin.site.register(Permission)
admin.site.register(GenericPermission)
