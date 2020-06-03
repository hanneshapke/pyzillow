import requests

from xml.etree import cElementTree as ElementTree  # for zillow API

from .pyzillowerrors import ZillowError, ZillowFail, ZillowNoResults
from . import __version__


class ZillowWrapper(object):
    """This class provides an interface into the Zillow API. An API key is required to create an instance of this class:

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
           object. GetUpdatedPropertyDetails data is not available for all valid Zillow IDs.

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
        """This method provides results from the GetDeepSearchResults API endpoint as an XML object.

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
        """This method provides results from the GetUpdatedPropertyDetails API endpoint as an XML object.

        :param zpid: Zillow Web Service Identifier
        :type zpid: str
        :return: Result from API query
        :rtype: xml.etree.ElementTree.Element
        """
        url = "http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm"

        params = {"zpid": zpid, "zws-id": self.api_key}
        return self.get_data(url, params)

    def get_data(self, url: str, params: dict):
        """This method requests data from the API endpoint specified in the url argument. It uses parameters from the params argument.

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
    """Maps results from the XML data array into attributes of an instance of GetDeepSearchResults.

    An instance of ``GetDeepSearchResults`` has the following attributes:
    ``.bathrooms``
    ``.bedrooms``
    ``.city``
    ``.fips_county``
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
    ``.state``
    ``.street``
    ``.tax_value``
    ``.tax_year``
    ``.total_rooms``
    ``.use_code``
    ``.year_built``
    ``.zestimate_amount``
    ``.zestimate_last_updated``
    ``.zestimate_percentile``
    ``.zestimate_valuation_range_high``
    ``.zestimate_valuation_range_low``
    ``.zestimate_value_change``
    ``.zillow_id``
    ``.zipcode``
    """

    attribute_mapping = {
        "bathrooms": "result/bathrooms",
        "bedrooms": "result/bedrooms",
        "city": "result/address/city",
        "fips_county": "result/FIPScounty",
        "graph_data_link": "result/links/graphsanddata",
        "home_detail_link": "result/links/homedetails",
        "home_size": "result/finishedSqFt",
        "home_type": "result/useCode",
        "last_sold_date": "result/lastSoldDate",
        "last_sold_price": "result/lastSoldPrice",
        "latitude": "result/address/latitude",
        "longitude": "result/address/longitude",
        "map_this_home_link": "result/links/mapthishome",
        "property_size": "result/lotSizeSqFt",
        "rentzestimate_amount": "result/rentzestimate/amount",
        "rentzestimate_last_updated": "result/rentzestimate/last-updated",
        "rentzestimate_valuation_range_high": "result/rentzestimate/valuationRange/high",
        "rentzestimate_valuation_range_low": "result/rentzestimate/valuationRange/low",
        "rentzestimate_value_change": "result/rentzestimate/valueChange",
        "state": "result/address/state",
        "street": "result/address/street",
        "tax_value": "result/taxAssessment",
        "tax_year": "result/taxAssessmentYear",
        "total_rooms": "result/totalRooms",
        "use_code": "result/useCode",
        "year_built": "result/yearBuilt",
        "zestimate_amount": "result/zestimate/amount",
        "zestimate_last_updated": "result/zestimate/last-updated",
        "zestimate_percentile": "result/zestimate/percentile",
        "zestimate_valuation_range_high": "result/zestimate/valuationRange/high",
        "zestimate_valuation_range_low": "result/zestimate/valuationRange/low",
        "zestimate_value_change": "result/zestimate/valueChange",
        "zillow_id": "result/zpid",
        "zipcode": "result/address/zipcode",
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
    """Maps results from the XML data array into attributes of an instance of GetUpdatedPropertyDetails.

    An instance of ``GetUpdatedPropertyDetails`` has the following attributes:
    ``.agent_name``
    ``.agent_profile_url``
    ``.appliances``
    ``.basement``
    ``.bathrooms``
    ``.bedrooms``
    ``.brokerage``
    ``.city``
    ``.cooling_system``
    ``.elementary_school``
    ``.exterior_material``
    ``.floor_material``
    ``.heating_sources``
    ``.heating_system``
    ``.high_school``
    ``.home_description``
    ``.home_detail_link``
    ``.home_info``
    ``.home_size``
    ``.home_type``
    ``.latitude``
    ``.longitude``
    ``.middle_school``
    ``.neighborhood``
    ``.num_floors``
    ``.num_rooms``
    ``.page_view_count_this_month``
    ``.page_view_count_total``
    ``.parking_type``
    ``.photo_gallery``
    ``.posting_agent``
    ``.posting_last_update``
    ``.posting_mls``
    ``.posting_status``
    ``.posting_type``
    ``.price``
    ``.property_size``
    ``.roof``
    ``.rooms``
    ``.school_district``
    ``.state``
    ``.street``
    ``.view``
    ``.year_built``
    ``.year_updated``
    ``.zillow_id``
    ``.zipcode``
    """

    attribute_mapping = {
        # attributes in common with GetDeepSearchResults
        "bathrooms": "editedFacts/bathrooms",
        "bedrooms": "editedFacts/bedrooms",
        "city": "result/address/city",
        "home_detail_link": "links/homeDetails",
        "home_size": "editedFacts/finishedSqFt",
        "home_type": "editedFacts/useCode",
        "latitude": "address/latitude",
        "longitude": "address/longitude",
        "property_size": "editedFacts/lotSizeSqFt",
        "state": "result/address/state",
        "street": "result/address/street",
        "year_built": "editedFacts/yearBuilt",
        "zillow_id": "zpid",
        "zipcode": "result/address/zipcode",
        # new attributes in GetUpdatedPropertyDetails
        "agent_name": "posting/agentName",
        "agent_profile_url": "posting/agentProfileUrl",
        "appliances": "editedFacts/appliances",
        "basement": "editedFacts/basement",
        "brokerage": "posting/brokerage",
        "cooling_system": "editedFacts/coolingSystem",
        "elementary_school": "elementarySchool",
        "exterior_material": "editedFacts/exteriorMaterial",
        "floor_material": "editedFacts/floorCovering",
        "heating_sources": "editedFacts/heatingSources",
        "heating_system": "editedFacts/heatingSystem",
        "high_school": "highSchool",
        "home_description": "homeDescription",
        "home_info": "links/homeInfo",
        "middle_school": "middleSchool",
        "neighborhood": "neighborhood",
        "num_floors": "editedFacts/numFloors",
        "num_rooms": "editedFacts/numRooms",
        "page_view_count_this_month": "pageViewCount/currentMonth",
        "page_view_count_total": "pageViewCount/total",
        "parking_type": "editedFacts/parkingType",
        "photo_gallery": "links/photoGallery",
        "photo_gallery": "links/photoGallery",
        "posting_agent": "posting/agentName",
        "posting_last_update": "posting/lastUpdatedDate",
        "posting_mls": "posting/mls",
        "posting_status": "posting/status",
        "posting_type": "posting/type",
        "price": "price",
        "roof": "editedFacts/roof",
        "rooms": "editedFacts/rooms",
        "school_district": "schoolDistrict",
        "view": "editedFacts/view",
        "year_updated": "editedFacts/yearUpdated",
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
