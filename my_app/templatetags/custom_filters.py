from django import template

register = template.Library()

@register.filter
def get_item(lst, index):
    try:
        if(int(index) < 50):
            return lst[int(index)-6]
        else:
            return lst[int(index)-50]
    except (IndexError, ValueError, TypeError):
        return index