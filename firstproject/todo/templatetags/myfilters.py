from django import template

register = template.Library()

def addclass(value, token):
    value.field.widget.attrs["class"] = token
    return value

def addplaceholder(value, token):
    value.field.widget.attrs["placeholder"] = token
    return value

def lower_case(value):
    return value.lower()

register.filter(addclass)
register.filter(addplaceholder)
register.filter(lower_case)

