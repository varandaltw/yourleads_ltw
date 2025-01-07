from django import template

register = template.Library()

@register.filter
def get_value(dictionary, key):
    """
    Safely retrieves a value from a dictionary using the given key.
    """
    return dictionary.get(key, "")

@register.filter
def getattr_safe(obj, attr):
    """Safely retrieves an attribute from an object."""
    return getattr(obj, attr, "")

@register.filter
def verbose_name(model, field_name):
    """Fetch the verbose name of a model field."""
    try:
        return model._meta.get_field(field_name).verbose_name.title()
    except Exception as e:
        return field_name  # Fallback if field_name doesn't exist
