import requests

from xml.etree import cElementTree as ElementTree  # for zillow API

from .pyzillowerrors import ZillowError, ZillowFail, ZillowNoResults
from . import __version__


class ZillowWrapper(object):
    """
    """

    def __init__(self, api_key=None):
        """

        """
        self.api_key = api_key

    def get_deep_search_results(self, address, zipcode, rentzestimate=False):
        """
        GetDeepSearchResults API
        """

        url = "http://www.zillow.com/webservice/GetDeepSearchResults.htm"
        params = {
            "address": address,
            "citystatezip": zipcode,
            "rentzestimate": str(rentzestimate).lower(),
            "zws-id": self.api_key,
        }
        return self.get_data(url, params)

    def get_updated_property_details(self, zpid):
        """
        GetUpdatedPropertyDetails API
        """
        url = "http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm"

        params = {"zpid": zpid, "zws-id": self.api_key}
        return self.get_data(url, params)

    def get_data(self, url, params):
        """
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
    """
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
    """
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
        """
        Creates instance of GeocoderResult from the provided XML data array
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
    """
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
        """
        Creates instance of GeocoderResult from the provided XML data array
        """
        self.data = data.findall("response")[0]
        for attr in self.attribute_mapping.__iter__():
            try:
                self.__setattr__(attr, self.get_attr(attr))
            except AttributeError:
                print("AttributeError with {}".format(attr))
