from xml.etree import ElementTree as ET

from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()


@register.filter(name='mail_to')
def mail_to(input_string):
    link_mailto = ET.Element('a', {'href': f'mailto:{input_string}'})
    link_mailto.text = input_string
    return mark_safe(ET.tostring(link_mailto, encoding='unicode'))


@register.filter(name='tel')
def tel(input_string):
    link_tel = ET.Element('a', {'href': f'tel:{input_string}'})
    link_tel.text = input_string
    return mark_safe(ET.tostring(link_tel, encoding='unicode'))


@register.filter(name='mfp')
def media_for_products(image_path):
    if not image_path:
        image_path = 'products_images/default.jpg'
    return f'{settings.MEDIA_URL}{image_path}'


@register.filter(name='mfu')
def media_for_users(image_path):
    if not image_path:
        image_path = 'users_avatars/Koala.jpg'
    return f'{settings.MEDIA_URL}{image_path}'

# Or you can register tag like this
# register.filter("mail_to", mail_to)
