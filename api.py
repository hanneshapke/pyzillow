import requests
import sys
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
        self.message = self.code[int(status)]
        self.url = url
        self.response = response

    def __str__(self):
        return repr(self.message) 

    def __unicode__(self):
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

    def get_deep_search_results(self, address, zipcode):
        """
        GetDeepSearchResults API
        """

        url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm'
        params = {
            'address': address,
            'citystatezip': zipcode,
            'zws-id': self.api_key 
            }
        return self.get_data(url, params)

    def get_updated_property_details(self, zpid):
        """
        GetUpdatedPropertyDetails API
        """
        url = 'http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm'

        params = {
            'zpid': zpid,
            'zws-id': self.api_key 
            }
        return self.get_data(url, params)

    # @omnimethod
    def get_data(self, url, params):
        """
        """

        try:
            request = requests.get(
                url = url,
                params = params,
                headers = {
                    'User-Agent': 'pyzillow/' + VERSION + ' (Python)'
                })
            print request.url
        except (ConnectionError, TooManyRedirects, Timeout):
            raise ZillowFail

        try:
            request.raise_for_status()
        except HTTPError:
            raise ZillowFail

        try:
            response = ElementTree.fromstring(request.text)
        except ParseError:
            print "Zillow response is not a valid XML" # (%s)" % (params['address'])
            raise ZillowFail

        if not response.findall('response'):
            print "Zillow returned no results" # (%s)" % (params['address'])
            raise ZillowNoResults

        if response.findall('message/code')[0].text is not '0':
            raise ZillowError(int(code)) 
        else:
            return response


class ZillowResults(object):
    """
    """

    attribute_mapping = {}

    def __init__(self, data):
        """
        Creates instance of GeocoderResult from the provided JSON data array
        """
        self.data = data.findall('response/results')
        self.len = len(self.data)
        self.current_index = 0
        self.current_data = self.data[0]
        self.tag = 'result'

    def __len__(self):
        return self.len

    def __iter__(self):
        return self

    def return_next(self):
        if self.current_index >= self.len:
            raise StopIteration
        self.current_data = self.data[self.current_index]
        self.current_index += 1
        return self

    def __unicode__(self):
        return self.zillow_id

    if sys.version_info[0] >= 3:  # Python 3
        def __str__(self):
            return self.__unicode__()

        def __next__(self):
            return self.return_next()
    else:  # Python 2
        def __str__(self):
            return self.__unicode__().encode('utf8')

        def next(self):
            return self.return_next()

    @property
    def count(self):
        return self.len

    @property
    def zillow_id(self):
        """
        Returns the zillow id
        """
        return self.current_data.find('result/zpid').text

    @property
    def home_type(self):
        """
        Returns the type of housing, based on useCode
        """
        return self.current_data.find('result/useCode').text

    @property
    def home_detail_link(self):
        """
        """
        return self.current_data.find('result/links/homedetails').text

    @property
    def graph_data_link(self):
        """
        graphsanddata
        """
        return self.current_data.find('result/links/graphsanddata').text

    @property
    def map_this_home_link(self):
        """
        mapthishome
        """
        return self.current_data.find('result/links/mapthishome').text

    @property
    def latitude(self):
        return self.current_data.find('result/address/latitude').text

    @property
    def longitude(self):
        return self.current_data.find('result/address/longitude').text

    @property
    def coordinates(self):
        """
        Return a (latitude, longitude) coordinate pair of the current result
        """
        return self.latitude, self.longitude

    @property
    def tax_year(self):
        """
        taxAssessmentYear
        """
        return self.current_data.find('result/taxAssessmentYear').text

    @property
    def tax_value(self):
        """
        taxAssessment
        """
        return self.current_data.find('result/taxAssessment').text
    
    @property
    def year_built(self):
        """
        yearBuilt
        """
        return self.current_data.find('result/yearBuilt').text

    @property
    def area_unit(self):
        """
        lotSizeSqFt
        """
        return u'SqFt'

    @property
    def property_size(self):
        """
        lotSizeSqFt
        """
        return self.current_data.find('result/lotSizeSqFt').text

    @property
    def home_size(self):
        """
        finishedSqFt
        """
        return self.current_data.find('result/finishedSqFt').text

    @property
    def bathrooms(self):
        """
        bathrooms
        """
        return self.current_data.find('result/bathrooms').text

    @property
    def bedrooms(self):
        """
        bedrooms
        """
        return self.current_data.find('result/bedrooms').text

    @property
    def last_sold_date(self):
        """
        lastSoldDate
        """
        return self.current_data.find('result/lastSoldDate').text

    @property
    def last_sold_price_currency(self):
        """
        lastSoldPrice currency
        """
        return self.current_data.find('result/lastSoldPrice').attrib["currency"]

    @property
    def last_sold_date(self):
        """
        lastSoldDate
        """
        return self.current_data.find('result/lastSoldPrice').text


class GetDeepSearchResults(ZillowResults):
    """
    """
    pass


class GetUpdatedPropertyDetails(ZillowResults):
    """
    """
    def __init__(self, data):
        """
        Creates instance of GeocoderResult from the provided JSON data array
        """
        super(GetUpdatedPropertyDetails, self).__init__(data)
        # self.tag = 'editedFacts'
        self.tag = 'result'
        
    # lastUpdatedDate

    @property
    def bedrooms(self):
        """
        bedrooms
        """
        return self.current_data.find(self.tag + '/bedrooms').text


    @property
    def last_sold_date2(self):
        """
        lastSoldDate
        """
        return '>>>>', self.current_data.find('result/lastSoldPrice').text

