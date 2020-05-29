import requests

from xml.etree import cElementTree as ElementTree  # for zillow API

from .pyzillowerrors import ZillowError, ZillowFail, ZillowNoResults
from . import __version__


class ZillowWrapper(object):
    """This class provides an interface into the Zillow API. An API key is required to
       create an instance of this class:

    >>> from pyzillow.pyzillow import ZillowWrapper
    >>> zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)

    To request data from Zillow, you can choose between:

        1. The GetDeepSearchResults API endpoint (:class:`pyzillow.pyzillow.GetDeepSearchResults`)
           which requires the following arguments:

            * A street address (e.g. ``'2114 Bigelow Ave'``)
            * A ZIP code or city and state combination (e.g. ``'98109'`` or ``'Seattle, WA'``)
            * Optional: Enabling or disabling Zillow Rentzestimate information in
              API results (``True``/``False``)

            Example:

            >>> from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
            >>> zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)
            >>> deep_search_response = zillow_data.get_deep_search_results(address,
                                                                           zipcode,
                                                                           rentzestimate)
            >>> result = GetDeepSearchResults(deep_search_response)

        2. The GetUpdatedPropertyDetails API endpoint
           (:class:`pyzillow.pyzillow.GetUpdatedPropertyDetails`) which requires a
           Zillow Property ID (ZPID) as an argument. You can acquire this identifier by
           accessing ``.zillow_id`` from a :class:`pyzillow.pyzillow.GetDeepSearchResults`
           object.

            Example:

            >>> from pyzillow.pyzillow import ZillowWrapper, GetUpdatedPropertyDetails
            >>> zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)
            >>> updated_property_details_response = \
                zillow_data.get_updated_property_details(zillow_id)
            >>> result = GetUpdatedPropertyDetails(updated_property_details_response)
    """

    def __init__(self, api_key: str = None):
        """Constructor method
        """
        self.api_key = api_key

    def get_deep_search_results(
        self, address: str, zipcode: str, rentzestimate: bool = False
    ):
        """This method provides results from the GetDeepSearchResults API endpoint
           as an XML object.

        :param address: Street address to look up
        :type address: str
        :param zipcode: ZIP code to look up
        :type zipcode: str
        :param rentzestimate: Add Rent Zestimate information to result (True/False),
         defaults to False
        :type rentzestimate: bool, optional
        :return: Result from API query
        :rtype: xml.etree.ElementTree.Element
        """
        url = "http://www.zillow.com/webservice/GetDeepSearchResults.htm"

        params = {
            "address": address,
            "citystatezip": zipcode,
            "rentzestimate": str(rentzestimate).lower(),
            "zws-id": self.api_key,
        }
        return self.get_data(url, params)

    def get_updated_property_details(self, zpid: str):
        """This method provides results from the GetUpdatedPropertyDetails API endpoint
           as an XML object.

        :param zpid: Zillow Web Service Identifier
        :type zpid: str
        :return: Result from API query
        :rtype: xml.etree.ElementTree.Element
        """
        url = "http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm"

        params = {"zpid": zpid, "zws-id": self.api_key}
        return self.get_data(url, params)

    def get_data(self, url: str, params: dict):
        """This method requests data from the API endpoint specified in the url argument.
           It uses parameters from the params argument.

        :param url: URL of API endpoint
        :type url: str
        :param params: Parameters for API query
        :type params: dict
        :raises ZillowFail: The API endpoint could not be reached or the request
            did not return valid XML
        :raises ZillowError: The API endpoint responded with an error code
        :raises ZillowNoResults: The request did not return any results
        :return: Result from API query
        :rtype: xml.etree.ElementTree.Element
        """
        try:
            request = requests.get(
                url=url,
                params=params,
                headers={
                    "User-Agent": "".join(["pyzillow/", __version__, " (Python)"])
                },
            )
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.Timeout,
        ):
            raise ZillowFail

        try:
            request.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ZillowFail

        try:
            response = ElementTree.fromstring(request.text)
        except ElementTree.ParseError:
            print("Zillow response is not a valid XML ({})".format(params["address"]))
            raise ZillowFail

        if response.findall("message/code")[0].text != "0":
            raise ZillowError(int(response.findall("message/code")[0].text))
        else:
            if not response.findall("response"):
                print("Zillow returned no results for ({})".format(params["address"]))
                raise ZillowNoResults
            return response


class ZillowResults(object):
    """Base class for :class:`pyzillow.pyzillow.GetDeepSearchResults`
       and :class:`pyzillow.pyzillow.GetUpdatedPropertyDetails`.
    """

    attribute_mapping = {}

    def get_attr(self, attr):
        """
        """
        try:
            return self.data.find(self.attribute_mapping[attr]).text
        except AttributeError:
            return None

    def __str__(self):
        return self.zillow_id

    @property
    def area_unit(self):
        """
        lotSizeSqFt
        """
        return u"SqFt"

    @property
    def last_sold_price_currency(self):
        """
        lastSoldPrice currency
        """
        return self.data.find(self.attribute_mapping["last_sold_price"]).attrib[
            "currency"
        ]


class GetDeepSearchResults(ZillowResults):
    """Maps results from the XML data array into attributes of an instance of
       GetDeepSearchResults.

    An instance of ``GetDeepSearchResults`` has the following attributes:
    ``.bathrooms``
    ``.bedrooms``
    ``.graph_data_link``
    ``.home_detail_link``
    ``.home_size``
    ``.home_type``
    ``.last_sold_date``
    ``.last_sold_price``
    ``.latitude``
    ``.longitude``
    ``.map_this_home_link``
    ``.property_size``
    ``.rentzestimate_amount``
    ``.rentzestimate_last_updated``
    ``.rentzestimate_valuation_range_high``
    ``.rentzestimate_valuation_range_low``
    ``.rentzestimate_value_change``
    ``.tax_value``
    ``.tax_year``
    ``.year_built``
    ``.zestimate_amount``
    ``.zestimate_last_updated``
    ``.zestimate_percentile``
    ``.zestimate_valuation_range_high``
    ``.zestimate_valuation_range_low``
    ``.zestimate_value_change``
    ``.zillow_id``
    """

    attribute_mapping = {
        "zillow_id": "result/zpid",
        "home_type": "result/useCode",
        "home_detail_link": "result/links/homedetails",
        "graph_data_link": "result/links/graphsanddata",
        "map_this_home_link": "result/links/mapthishome",
        "latitude": "result/address/latitude",
        "longitude": "result/address/longitude",
        "tax_year": "result/taxAssessmentYear",
        "tax_value": "result/taxAssessment",
        "year_built": "result/yearBuilt",
        "property_size": "result/lotSizeSqFt",
        "home_size": "result/finishedSqFt",
        "bathrooms": "result/bathrooms",
        "bedrooms": "result/bedrooms",
        "last_sold_date": "result/lastSoldDate",
        "last_sold_price": "result/lastSoldPrice",
        "zestimate_amount": "result/zestimate/amount",
        "zestimate_last_updated": "result/zestimate/last-updated",
        "zestimate_value_change": "result/zestimate/valueChange",
        "zestimate_valuation_range_high": "result/zestimate/valuationRange/high",
        "zestimate_valuation_range_low": "result/zestimate/valuationRange/low",
        "zestimate_percentile": "result/zestimate/percentile",
        "rentzestimate_amount": "result/rentzestimate/amount",
        "rentzestimate_last_updated": "result/rentzestimate/last-updated",
        "rentzestimate_value_change": "result/rentzestimate/valueChange",
        "rentzestimate_valuation_range_high": "result/rentzestimate/valuationRange/high",
        "rentzestimate_valuation_range_low": "result/rentzestimate/valuationRange/low",
    }

    def __init__(self, data, *args, **kwargs):
        """Constructor method
        """
        self.data = data.findall("response/results")[0]
        for attr in self.attribute_mapping.__iter__():
            try:
                self.__setattr__(attr, self.get_attr(attr))
            except AttributeError:
                print("AttributeError with {}".format(attr))

    @property
    def region_name(self):
        """
        region name
        """
        try:
            return self.data.find("result/localRealEstate/region").attrib["name"]
        except AttributeError:
            return None

    @property
    def region_id(self):
        """
        region id
        """
        try:
            return self.data.find("result/localRealEstate/region").attrib["id"]
        except AttributeError:
            return None

    @property
    def region_type(self):
        """
        region type
        """
        try:
            return self.data.find("result/localRealEstate/region").attrib["type"]
        except AttributeError:
            return None


class GetUpdatedPropertyDetails(ZillowResults):
    """Maps results from the XML data array into attributes of an instance of
       GetUpdatedPropertyDetails.

    An instance of ``GetDeepSearchResults`` has the following attributes:
    ``.agent_name``
    ``.agent_profile_url``
    ``.appliances``
    ``.basement``
    ``.bathrooms``
    ``.bedrooms``
    ``.brokerage``
    ``.elementary_school``
    ``.floor_material``
    ``.graph_data_link``
    ``.heating_sources``
    ``.heating_system``
    ``.home_description``
    ``.home_detail_link``
    ``.home_info``
    ``.home_size``
    ``.home_type``
    ``.last_sold_date``
    ``.last_sold_price``
    ``.latitude``
    ``.longitude``
    ``.map_this_home_link``
    ``.middle_school``
    ``.neighborhood``
    ``.num_floors``
    ``.num_rooms``
    ``.parking_type``
    ``.photo_gallery``
    ``.posting_status``
    ``.posting_type``
    ``.property_size``
    ``.roof``
    ``.rooms``
    ``.school_district``
    ``.tax_value``
    ``.tax_year``
    ``.view``
    ``.year_built``
    ``.year_updated``
    ``.zillow_id``
    """

    attribute_mapping = {
        # attributes in common with GetDeepSearchResults
        "zillow_id": "zpid",
        "home_type": "editedFacts/useCode",
        "home_detail_link": "links/homeDetails",
        "graph_data_link": "",
        "map_this_home_link": "",
        "latitude": "address/latitude",
        "longitude": "address/longitude",
        "tax_year": "",
        "tax_value": "",
        "year_built": "editedFacts/yearBuilt",
        "property_size": "editedFacts/lotSizeSqFt",
        "home_size": "editedFacts/finishedSqFt",
        "bathrooms": "editedFacts/bathrooms",
        "bedrooms": "editedFacts/bedrooms",
        "last_sold_date": "",
        "last_sold_price": "",
        # new attributes in GetUpdatedPropertyDetails
        "photo_gallery": "links/photoGallery",
        "home_info": "links/homeInfo",
        "year_updated": "editedFacts/yearUpdated",
        "floor_material": "editedFacts/floorCovering",
        "num_floors": "editedFacts/numFloors",
        "basement": "editedFacts/basement",
        "roof": "editedFacts/roof",
        "view": "editedFacts/view",
        "parking_type": "editedFacts/parkingType",
        "heating_sources": "editedFacts/heatingSources",
        "heating_system": "editedFacts/heatingSystem",
        "rooms": "editedFacts/rooms",
        "num_rooms": "editedFacts/numRooms",
        "appliances": "editedFacts/appliances",
        "neighborhood": "neighborhood",
        "school_district": "schoolDistrict",
        "elementary_school": "elementarySchool",
        "middle_school": "middleSchool",
        "school_district": "schoolDistrict",
        "home_description": "homeDescription",
        "posting_status": "posting/status",
        "posting_type": "posting/type",
        "agent_name": "posting/agentName",
        "agent_profile_url": "posting/agentProfileUrl",
        "brokerage": "posting/brokerage",
    }

    def __init__(self, data, *args, **kwargs):
        """Constructor method
        """
        self.data = data.findall("response")[0]
        for attr in self.attribute_mapping.__iter__():
            try:
                self.__setattr__(attr, self.get_attr(attr))
            except AttributeError:
                print("AttributeError with {}".format(attr))
