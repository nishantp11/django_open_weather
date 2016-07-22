"""
Templatetags for weather app
"""

from datetime import datetime
from django import template    
register = template.Library()    

@register.filter('timestamp_to_time')
def timestamp_to_time(in_string):
	"""
	Converts unix timestamp to python datetime object
	"""
	return datetime.fromtimestamp(int(in_string))
