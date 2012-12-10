import recaptcha.client.mailhide
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def mailhide(addr):
    return recaptcha.client.mailhide.asurl(addr, settings.MAILHIDE_PUBLIC_KEY, settings.MAILHIDE_PRIVATE_KEY)
