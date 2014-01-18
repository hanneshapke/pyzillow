import requests
from requests.exceptions import (ConnectionError, TooManyRedirects, 
                                Timeout, HTTPError)

from xml.etree import cElementTree as ElementTree  # for zillow API

from __version__ import VERSION


class ZillowError(Exception):
    """

    """
    code = dict([ 
        (0, 'Request successfully processed'), 
        (1, 'Service error-there was a server-side error while processing the request. \
            Check to see if your url is properly formed: delimiters, character cases, etc.'),
        (2, 'The specified ZWSID parameter was invalid or not specified in the request.\
            Check if you have provided a ZWSID in your API call. \
            If yes, check if the ZWSID is keyed in correctly. \
            If it still doesn\'t work, contact Zillow to get help on fixing \
            your ZWSID.'),
        (3, 'Web services are currently unavailable.\
            The Zillow Web Service is currently not available. \
            Please come back later and try again.'),
        (4, 'The API call is currently unavailable.\
            The Zillow Web Service is currently not available. \
            Please come back later and try again.'),
        (500, 'Invalid or missing address parameter.\
            Check if the input address parameter matches the format specified \
            in the input parameters table. When inputting a city name, the \
            state should also be given. A city name alone will not give \
            a valid address.'),
        (501, 'Invalid or missing citystatezip parameter. \
            Check if the input address parameter matches the format specified \
            in the input parameters table. When inputting a city name, the \
            state should also be given. A city name alone will not give \
            a valid address.'),
        (502, 'No results found. \
            Sorry, the address you provided is not found in the Zillow \
            property database.'),
        (503, 'Failed to resolve city, state or ZIP code.\
            Check if the city-state combination is valid. \
            Also check if you have provided a valid ZIP code.'),
        (504, 'No coverage for specified area  The specified area \
            is not covered by the Zillow property database. To see our \
            property coverage tables, click here.'),
        (505, 'Timeout Your request timed out. The server could be \
            busy or unavailable. Try again later.'),
        (506, 'Address string too long If address is valid, try using \
            abbreviations.'),
        (507, 'No exact match found. Verify that the given address is correct.'),
        ])

    def __init__(self, status, url=None, response=None):
        """

        """
        Exception.__init__(self, status)        # Exception is an old-school class
        self.status = status
        self.url = url
        self.response = response

    def __str__(self):
        """
        """
        return 'Error %s\nQuery: %s' % (code[status], self.url)

    def __unicode__(self):
        """Return a unicode representation of this :exc:`GeocoderError`."""
        return unicode(self.__str__())


class ZillowFail(Exception):

    def __init__(self):
        Exception.__init__(self)


class ZillowNoResults(Exception):

    def __init__(self):
        Exception.__init__(self)


class ZillowWrapper(object):

    ZILLOW_QUERY_URL = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm'
    ZILLOW_API_KEY = ''

    def __init__(self, api_key=None):
        """

        """
        self.api_key = api_key
        # pass

    # @omnimethod
    def get_data(self, address, zipcode):
        """
        """

        params = {
            'address': address,
            'zipcode': zipcode,
            'zws-id': self.api_key # ZillowWrapper.ZILLOW_API_KEY
            }

        try:
            request = requests.get(
                url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm',
                # ZillowWrapper.ZILLOW_QUERY_URL,
                params = params,
                headers = {
                    'User-Agent': 'pyzillow/' + VERSION + ' (Python)'
                })
        except (ConnectionError, TooManyRedirects, Timeout):
            raise ZillowFail

        try:
            request.raise_for_status()
        except HTTPError:
            raise ZillowFail

        try:
            response = ElementTree.fromstring(request.text)
        except ParseError:
            print "Zillow response is not a valid XML (%s)" % (params['address'])
            raise ZillowFail

        if not response.findall('response'):
            print "Zillow returned no results (%s)" % (params['address'])
            raise ZillowNoResults

        if not response.findall('code') == '0':
            raise ZillowError(response.findall('code'))
        else:
            return response


