from django import template
register = template.Library()

# custom filter to format a number as idr
@register.filter
def rupiah(value):
    try:
        n = int(value)
    except Exception:
        return value
    return f"Rp{n:,.0f}".replace(",", ".")