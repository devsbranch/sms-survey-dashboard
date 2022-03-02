from email import contentmanager
from ensurepip import version
#from multiprocessing import context
from pathlib import Path
from re import template
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def tag(context):
    """Reads current project release from the VERSION file."""
    version_file = Path(Path(__file__).resolve(
        strict=True).parent.parent.parent, 'VERSION')
    try:
        with open(version_file, 'r') as file:
            version = file.read()
            context['version'] = version
    except IOError:
        context['version'] = 'unknown'
    return context['version']
