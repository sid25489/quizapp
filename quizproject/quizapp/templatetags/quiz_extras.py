from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get value from dict by key (for template use)."""
    if dictionary is None:
        return None
    return dictionary.get(key)
