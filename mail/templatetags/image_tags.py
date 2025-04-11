from django import template

register = template.Library()


@register.filter()
def image_path(path):
    """Фильтр для создания пути к изображению."""
    if path:
        return f"/media/{path}"
    return "#"
