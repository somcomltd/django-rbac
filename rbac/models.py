from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ObjectDoesNotExist


def _get_permission(queryset_model, filters, roles):
    try:
        permission = queryset_model.objects.get(**filters)
    # If permission does not exist, authorization is not allowed
    except ObjectDoesNotExist:
        return False
    else:
        perm_roles = permission.roles.all()
        return True if filter(lambda x: x in perm_roles, roles) else False


class PermissionManager(models.Manager):

    def _get_filters(self, model_inst, operation):
        model_ct = ContentType.objects.get_for_model(model_inst)
        filters = {'object_ct': model_ct, 'object_id': model_inst.id,
                   'operation': operation}
        return filters

    def get_permission(self, model, operation, roles):
        filters = self._get_filters(model, operation)
        queryset_model = Permission
        return _get_permission(queryset_model, filters, roles)

    def create_permission(self, model_inst, operation, roles):
        filters = self._get_filters(model_inst, operation)
        permission = Permission.objects.create(**filters)
        for role in roles:
            permission.roles.add(role)
        return permission


class GenericPermissionManager(models.Manager):

    def _get_filters(self, model, operation):
        model_ct = ContentType.objects.get_for_model(model)
        filters = {'content_type': model_ct, 'operation': operation}
        return filters

    def get_permission(self, model, operation, roles):
        filters = self._get_filters(model, operation)
        queryset_model = GenericPermission
        return _get_permission(queryset_model, filters, roles)

    def create_permission(self, model, operation, roles):
        filters = self._get_filters(model, operation)
        permission = GenericPermission.objects.create(**filters)
        for role in roles:
            permission.roles.add(role)
        return permission


class Operation(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return '%s' % self.name


class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return '%s' % self.name


class RelationshipManager(models.Manager):
    def _get_filters(self, subject, target):
        subject_ct = ContentType.objects.get_for_model(subject)
        target_ct = ContentType.objects.get_for_model(target)
        filters = {'subject_ct': subject_ct, 'subject_id': subject.id,
                   'target_subject_ct': target_ct, 'target_subject_id': target.id}
        return filters

    def get_roles(self, subject, target):
        roles = []
        filters = self._get_filters(subject, target)
        queryset_model = Relationship
        relationships = queryset_model.objects.filter(**filters)
        for relationship in relationships:
            roles.append(relationship.role)
        return roles


class Relationship(models.Model):
    subject_ct = models.ForeignKey(ContentType, related_name='subject')
    subject_id = models.PositiveIntegerField()
    target_subject_ct = models.ForeignKey(ContentType, related_name='target_subject')
    target_subject_id = models.PositiveIntegerField()
    role = models.ForeignKey(Role)

    subject = generic.GenericForeignKey('subject_ct', 'subject_id')
    target_subject = generic.GenericForeignKey('target_subject_ct', 'target_subject_id')

    objects = RelationshipManager()

    class Meta:
        unique_together = ('subject_ct', 'subject_id', 'target_subject_ct',
                           'target_subject_id', 'role')

    def __unicode__(self):
        return '%s | %s | %s' % (self.subject, self.target_subject, self.role)


class Permission(models.Model):
    object_ct = models.ForeignKey(ContentType, related_name='permission_object')
    object_id = models.PositiveIntegerField()
    operation = models.ForeignKey(Operation)
    roles = models.ManyToManyField(Role, related_name='permissions')

    object = generic.GenericForeignKey('object_ct', 'object_id')

    objects = PermissionManager()

    class Meta:
        unique_together = ('object_ct', 'object_id', 'operation')
        ordering = ['object_ct', 'object_id']

    def __unicode__(self):
        return '%s | %s | %s' % (self.object, self.operation)


class GenericPermission(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='generic_permission_model')
    operation = models.ForeignKey(Operation)
    roles = models.ManyToManyField(Role, related_name='generic_permissions')

    objects = GenericPermissionManager()

    class Meta:
        unique_together = ('content_type', 'operation')

    def __unicode__(self):
        return '%s | %s | %s' % (self.content_type, self.operation)