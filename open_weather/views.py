from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.conf import settings
from .api import APIClient
import json
# Create your views here.

def dashboard(request):

	"""
	Handles the main page response for Weather app

	"""
	response = []

	client = APIClient(settings.OPEN_WEATHER_API_KEY)
	
	endpoint = '/weather'

	cities = request.session.get('city_choices',settings.DEFAULT_CITIES)

	for city in cities:
		params = {'q':city,'units':'metric'}
		try:
			out = client.call_API(endpoint,params)
			response.append(json.loads(out))
		except:
			pass

	print response

	return render_to_response(
			'index.html',
			{'response':response},
			RequestContext(request)
		)