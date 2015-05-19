from django import template

from rbac.models import RBACPermission, RBACGenericPermission

register = template.Library()


class RBACPermissionNode(template.Node):
    def __init__(self, params, nodelist_true, nodelist_false):
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.owner = params[0]
        self.model_inst = params[1]
        self.operation = params[2]
        self.roles = params[3]

    def render(self, context):
        owner = template.resolve_variable(self.owner, context)
        model_inst = template.resolve_variable(self.model_inst, context)
        op = template.resolve_variable(self.operation, context)
        roles = template.resolve_variable(self.roles, context)
        if RBACPermission.objects.get_permission(owner, model_inst, op, roles):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

@register.tag('if_rbac_permission')
def if_rbac_permission(parser, token):
    """
    {% if_rbac_permission owner model_inst operation roles %}
        ...
    {% else %}
        ---
    {% endif_rbac_permission %}
    """
    bits = list(token.split_contents())
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return RBACPermissionNode(bits[1:], nodelist_true, nodelist_false)


class RBACGenericPermissionNode(template.Node):
    def __init__(self, params, nodelist_true, nodelist_false):
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.owner = params[0]
        self.model = params[1]
        self.operation = params[2]
        self.roles = params[3]

    def render(self, context):
        owner = template.resolve_variable(self.owner, context)
        model = template.resolve_variable(self.model, context)
        op = template.resolve_variable(self.operation, context)
        roles = template.resolve_variable(self.roles, context)
        if RBACGenericPermission.objects.get_permission(owner, model, op, roles):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

@register.tag('if_rbac_generic_permission')
def if_rbac_generic_permission(parser, token):
    """
    {% if_rbac_generic_permission owner model operation roles %}
        ...
    {% else %}
        ---
    {% endif_rbac_generic_permission %}
    """
    bits = list(token.split_contents())
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return RBACGenericPermissionNode(bits[1:], nodelist_true, nodelist_false)
