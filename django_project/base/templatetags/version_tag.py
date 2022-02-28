from pathlib import Path
from django.template import Library

register = Library()

@register.simple_tag(takes_context=True)
def version_tag(context):
    """Reads current project release from the VERSION file."""
    version_file = Path(Path(__file__).resolve(strict=True).parent.parent.parent, "VERSION")

    try:
        with open(version_file, 'r') as file:
            version = file.read()
            context['version'] = version
    except IOError:
        context['version'] = 'Unknown'
    return context['version']

