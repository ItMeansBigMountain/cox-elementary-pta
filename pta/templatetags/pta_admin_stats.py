from django import template
from pta.models import VolunteerInterest

register = template.Library()

@register.simple_tag
def unreviewed_volunteer_interest_count():
    return VolunteerInterest.objects.filter(reviewed=False).count()
