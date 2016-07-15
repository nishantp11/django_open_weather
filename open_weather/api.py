"""
API interactions
"""

# Python 2.x/3.x compatibility imports
try:
    from urllib.error import HTTPError, URLError
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import HTTPError, URLError
    from urllib import urlencode

import socket
from .exceptions import APICallError

ROOT_API_URL = 'http://api.openweathermap.org/data/2.5'
ICONS_BASE_URL = 'http://openweathermap.org/img/w'

class APIClient(object):

    """
    An HTTP client class, that cosumes OW API.

    :param API_key: a Unicode object representing the OWM web API key
    :type API_key: Unicode

    """

    def __init__(self, API_key):
        self._API_key = API_key
        self._API_root_URL = ROOT_API_URL
        

    def call_API(self, API_endpoint_URL, params_dict,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):

        """
        Invokes a specific OWM web API endpoint URL, returning raw JSON data.

        :param API_endpoint_URL: the API endpoint to be invoked
        :type API_endpoint_URL: str
        :param params_dict: a dictionary containing the query parameters to be
            used in the HTTP request (given as key-value couples in the dict)
        :type params_dict: dict
        :param timeout: how many seconds to wait for connection establishment
            (defaults to ``socket._GLOBAL_DEFAULT_TIMEOUT``)
        :type timeout: int
        :returns: a string containing raw JSON data
        :raises: *APICallError*

        """
        url = self._build_full_URL(API_endpoint_URL, params_dict)

        try:
            try:
                from urllib.request import urlopen
            except ImportError:
                from urllib2 import urlopen
            response = urlopen(url, None, timeout)
        except HTTPError as e:
            raise APICallError(str(e), e)
        except URLError as e:
            raise APICallError(str(e), e)
        else:
            data = response.read().decode('utf-8')
            return data

    def _build_full_URL(self, API_endpoint_URL, params_dict):
        """
        Adds the API key and the query parameters dictionary to the specified
        API endpoint URL, returning a complete HTTP request URL.

        :param API_endpoint_URL: the API endpoint base URL
        :type API_endpoint_URL: str
        :param params_dict: a dictionary containing the query parameters to be
            used in the HTTP request (given as key-value couples in the dict)
        :type params_dict: dict
        :param API_key: the OWM web API key
        :type API_key: str
        :returns: a full string HTTP request URL

        """
        url =self._API_root_URL + API_endpoint_URL
        params = params_dict.copy()
        if self._API_key is not None:
            params['APPID'] = self._API_key
        return self._build_query_parameters(url, params)

    def _build_query_parameters(self, base_URL, params_dict):
        """
        Turns dictionary items into query parameters and adds them to the base
        URL

        :param base_URL: the base URL whom the query parameters must be added
            to
        :type base_URL: str
        :param params_dict: a dictionary containing the query parameters to be
            used in the HTTP request (given as key-value couples in the dict)
        :type params_dict: dict
        :returns: a full string HTTP request URL

        """
        return base_URL + '?' + urlencode(params_dict)

