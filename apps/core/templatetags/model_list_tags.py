from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    value = ''
    if isinstance(dictionary, dict):
        if dictionary.get(key):
            value = dictionary.get(key)
    return value

@register.filter
def get_object_item(object_item, key, view=None):
    keys = key.split('__')
    for key in keys:
        object_item = getattr(object_item, key)
    if view and hasattr(view, f'get_{key}'):
        object_item = getattr(view, f'get_{key}')(object_item)
    return object_item

@register.filter
def get_verbose_name(model, key):
    if '__' not in key:
        return model._meta.get_field(key).verbose_name
    keys = key.split('__')
    for key in keys:
        model = model._meta.get_field(key).related_model or model
    return model._meta.get_field(key).verbose_name

    
@register.simple_tag()
def get_view_item(object_item, key, view=None):
    keys = key.split('__')
    value = object_item
    for key in keys:
        value = getattr(value, key)
    if view and hasattr(view, f'get_{key}'):
        value = getattr(view, f'get_{key}')(object_item)
    return value



