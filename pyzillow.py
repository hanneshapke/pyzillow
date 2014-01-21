import requests
import sys
from requests.exceptions import (ConnectionError, TooManyRedirects, 
                                Timeout, HTTPError)

from xml.etree import cElementTree as ElementTree  # for zillow API

from pyzillowerrors import ZillowError, ZillowFail, ZillowNoResults
from __version__ import VERSION


class ZillowWrapper(object):
    """
    """

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
        # self.data = data.findall('response/results')
        self.len = len(self.data)
        self.current_index = 0
        self.current_data = self.data[0]

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
        return self.current_data.find(self.attribute_mapping['zillow_id']).text

    @property
    def home_type(self):
        """
        Returns the type of housing, based on useCode
        """
        return self.current_data.find(self.attribute_mapping['home_type']).text

    @property
    def home_detail_link(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['home_detail_link']).text

    @property
    def graph_data_link(self):
        """
        graphsanddata
        """
        return self.current_data.find(self.attribute_mapping['graph_data_link']).text

    @property
    def map_this_home_link(self):
        """
        mapthishome
        """
        return self.current_data.find(self.attribute_mapping['map_this_home_link']).text

    @property
    def latitude(self):
        return self.current_data.find(self.attribute_mapping['latitude']).text

    @property
    def longitude(self):
        return self.current_data.find(self.attribute_mapping['longitude']).text

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
        return self.current_data.find(self.attribute_mapping['tax_year']).text

    @property
    def tax_value(self):
        """
        taxAssessment
        """
        return self.current_data.find(self.attribute_mapping['tax_value']).text
    
    @property
    def year_built(self):
        """
        yearBuilt
        """
        return self.current_data.find(self.attribute_mapping['year_built']).text

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
        return self.current_data.find(self.attribute_mapping['property_size']).text

    @property
    def home_size(self):
        """
        finishedSqFt
        """
        return self.current_data.find(self.attribute_mapping['home_size']).text

    @property
    def bathrooms(self):
        """
        bathrooms
        """
        return self.current_data.find(self.attribute_mapping['bathrooms']).text

    @property
    def bedrooms(self):
        """
        bedrooms
        """
        return self.current_data.find(self.attribute_mapping['bedrooms']).text

    @property
    def last_sold_date(self):
        """
        lastSoldDate
        """
        return self.current_data.find(self.attribute_mapping['last_sold_date']).text

    @property
    def last_sold_price_currency(self):
        """
        lastSoldPrice currency
        """
        return self.current_data.find(self.attribute_mapping['last_sold_price']).attrib["currency"]

    @property
    def last_sold_price(self):
        """
        lastSoldDate
        """
        return self.current_data.find(self.attribute_mapping['last_sold_price']).text


class GetDeepSearchResults(ZillowResults):
    """
    """
    attribute_mapping = {
        'zillow_id':             'result/zpid',
        'home_type':        'result/useCode',
        'home_detail_link': 'result/links/homedetails',
        'graph_data_link':  'result/links/graphsanddata',
        'map_this_home_link': 'result/links/mapthishome',
        'latitude':         'result/address/latitude',
        'longitude':        'result/address/longitude',
        'tax_year':         'result/taxAssessmentYear',
        'tax_value':        'result/taxAssessment',
        'year_built':       'result/yearBuilt',
        'property_size':    'result/lotSizeSqFt',
        'home_size':        'result/finishedSqFt',
        'bathrooms':        'result/bathrooms',
        'bedrooms':         'result/bedrooms',
        'last_sold_date':   'result/lastSoldDate',
        'last_sold_price_currency': 'result/lastSoldPrice',
        'last_sold_price':  'result/lastSoldPrice',
    }

    def __init__(self, data):
        """
        
        """
        self.data = data.findall('response/results')
        super(GetDeepSearchResults, self).__init__(data)


class GetUpdatedPropertyDetails(ZillowResults):
    """
    """
    attribute_mapping = {
        # attributes in common with GetDeepSearchResults
        'zillow_id':        'zpid', 
        'home_type':        'editedFacts/useCode',
        'home_detail_link': 'links/homeDetails',
        'graph_data_link':  '',
        'map_this_home_link': '',
        'latitude':         'address/latitude',
        'longitude':        'address/longitude',
        'tax_year':         '',
        'tax_value':        '',
        'year_built':       'editedFacts/yearBuilt',
        'property_size':    'editedFacts/lotSizeSqFt',
        'home_size':        'editedFacts/finishedSqFt',
        'bathrooms':        'editedFacts/bathrooms',
        'bedrooms':         'editedFacts/bedrooms',
        'last_sold_date':   '',
        'last_sold_price_currency': '',
        'last_sold_price':  '',
        # new attributes in GetUpdatedPropertyDetails
        'photo_gallery':    'links/photoGallery',
        'home_info':        'links/homeInfo',
        'year_updated':     'editedFacts/yearUpdated', 
        'floors':           'editedFacts/numFloors', 
        'basement':         'editedFacts/basement', 
        'roof':             'editedFacts/roof',
        'view':             'editedFacts/view', 
        'heating_sources':   'editedFacts/heatingSources', 
        'heating_system':   'editedFacts/heatingSystem', 
        'rooms':            'editedFacts/rooms', 
        'neighborhood':     'neighborhood', 
        'school_district':  'schoolDistrict', 
        #'': '', 
    }

    def __init__(self, data):
        """
        #### Creates instance of GeocoderResult from the provided JSON data array
        """
        self.data = data.findall('response')
        super(GetUpdatedPropertyDetails, self).__init__(data)
        

    # lastUpdatedDate

    @property
    def photo_gallery(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['photo_gallery']).text

    @property
    def home_info(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['home_info']).text

    @property
    def year_updated(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['year_updated']).text  

    @property
    def floors(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['floors']).text  

    @property
    def basement(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['basement']).text

    @property
    def roof(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['roof']).text

    @property
    def view(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['view']).text

    @property
    def heating_sources(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['heating_sources']).text

    @property
    def heating_system(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['heating_system']).text

    @property
    def rooms(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['rooms']).text

    @property
    def neighborhood(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['neighborhood']).text

    @property
    def school_district(self):
        """
        """
        return self.current_data.find(self.attribute_mapping['school_district']).text