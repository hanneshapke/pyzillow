"""
Tests for `pyzillow` module.
"""

import pytest
import responses

from api_responses import (
    APIReponses,
    set_get_deep_search_response,
    set_updated_property_details_response,
)
from pyzillow.pyzillow import (
    GetDeepSearchResults,
    GetUpdatedPropertyDetails,
    ZillowWrapper,
)
from pyzillow.pyzillowerrors import ZillowError


class TestPyzillow(object):
    @classmethod
    def setup_class(cls):
        cls.ZILLOW_API_KEY = "NO_KEY_NEEDED_DUE_TO_MOCKING_API"
        cls.address = "2114 Bigelow Ave Seattle, WA"
        cls.zipcode = "98109"
        cls.api_response_obj = APIReponses()

    @responses.activate
    def test_zillow_api_connect(self):

        set_get_deep_search_response(
            self.api_response_obj.get("get_deep_search_200_ok")
        )
        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)
        zillow_search_response = zillow_data.get_deep_search_results(
            self.address, self.zipcode
        )

        assert zillow_search_response.find("message").find("code").text == "0"

    @responses.activate
    def test_zillow_error_invalid_ZWSID(self):
        """
        This test checks the correct error message if no ZWSID is provided.
        Expected error code: 2
        """
        set_get_deep_search_response(self.api_response_obj.get("error_2_zwsid_missing"))
        zillow_data = ZillowWrapper(None)

        with pytest.raises(ZillowError) as excinfo:
            zillow_data.get_deep_search_results(address=self.address, zipcode=None)
        error_msg = "Status 2: The specified ZWSID parameter was invalid"
        assert error_msg in str(excinfo.value)

    @responses.activate
    def test_zillow_error_missing_address(self):
        """
        This test checks the correct error message if no address is provided.
        Expected error code: 500
        """

        set_get_deep_search_response(
            self.api_response_obj.get("error_500_no_address_provided")
        )
        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)

        with pytest.raises(ZillowError) as excinfo:
            zillow_data.get_deep_search_results(address=self.address, zipcode=None)
        error_msg = "Status 500: Invalid or missing address parameter."
        assert error_msg in str(excinfo.value)

    @responses.activate
    def test_zillow_error_missing_zipcode(self):
        """
        This test checks the correct error message if no zipcode is provided.
        Expected error code: 501
        """

        set_get_deep_search_response(
            self.api_response_obj.get("error_501_no_city_state")
        )
        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)

        with pytest.raises(ZillowError) as excinfo:
            zillow_data.get_deep_search_results(address=self.address, zipcode=None)
        error_msg = "Status 501: Invalid or missing citystatezip parameter"
        assert error_msg in str(excinfo.value)

    @responses.activate
    def test_zillow_error_no_property_match(self):
        """
        This test checks the correct error message if no property is found.
        Expected error code: 508
        Address and zip code of an exisiting property, but not listed
        """

        address = "not a valid address"
        zipcode = "20001"
        set_get_deep_search_response(
            self.api_response_obj.get("error_508_invalid_address")
        )
        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)

        with pytest.raises(ZillowError) as excinfo:
            zillow_data.get_deep_search_results(address=address, zipcode=zipcode)
        error_msg = "Status 508: No exact match found for input address."
        assert error_msg in str(excinfo.value)

    # CASE BELOW SEEMS TO HAVE BEEN DEPRECATED
    # # @responses.activate
    # def test_zillow_error_match_zipcode_city(self):
    #     # This test checks the correct error message if no zipcode is provided.
    #     # Expected error code: 503
    #     mismatch_zipcode = '97204'  # Portland, OR
    #     zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)

    #     with pytest.raises(ZillowError) as excinfo:
    #         zillow_data.get_deep_search_results(
    #             address=self.address,
    #             zipcode=mismatch_zipcode
    #         )
    #     error_msg = "Status 508: No exact match found for input address."
    #     assert error_msg in str(excinfo.value)

    @responses.activate
    def test_zillow_error_invalid_zipcode(self):
        """
        This test checks the correct error message if an
        invalid zipcode is provided.
        Expected error code: 508
        """

        invalid_zipcode = "ABCDE"  # invalid zipcode
        set_get_deep_search_response(
            self.api_response_obj.get("error_508_invalid_zipcode")
        )

        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)

        with pytest.raises(ZillowError) as excinfo:
            zillow_data.get_deep_search_results(
                address=self.address, zipcode=invalid_zipcode
            )
        error_msg = "Status 508: No exact match found for input address."
        assert error_msg in str(excinfo.value)

    @responses.activate
    def test_zillow_error_no_coverage(self):
        """
        This test checks the correct error message
        if no coverage is provided.
        Expected error code: 508
        """

        address = "Calle 21 y O, Vedado, Plaza, Ciudad de la Habana, Cuba"
        zipcode = "10400"  # Cuban address, I assume Zillow doesn't cover Cuba
        set_get_deep_search_response(
            self.api_response_obj.get("error_508_outside_of_area")
        )

        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)

        with pytest.raises(ZillowError) as excinfo:
            zillow_data.get_deep_search_results(address=address, zipcode=zipcode)
        error_msg = "Status 508: No exact match found for input address."
        assert error_msg in str(excinfo.value)

    @responses.activate
    def test_zillow_error_account_not_authorized(self):
        """
        This test checks for account not authorized error
        Expected error code: 6
        """

        set_get_deep_search_response(
            self.api_response_obj.get("error_6_account_not_authorized")
        )

        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)

        with pytest.raises(ZillowError) as excinfo:
            zillow_data.get_deep_search_results(
                address=self.address, zipcode=self.zipcode
            )
        error_msg = "Status 6: This account is not authorized to execute this API call"
        assert error_msg in str(excinfo.value)

    @responses.activate
    def test_deep_search_results(self):
        """
        Tests parsing of deep_search results
        """

        address = "2114 Bigelow Ave Seattle, WA"
        zipcode = "98109"

        set_get_deep_search_response(
            self.api_response_obj.get("get_deep_search_200_ok")
        )

        zillow_data = ZillowWrapper(api_key=None)
        deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
        result = GetDeepSearchResults(deep_search_response)

        assert result.zillow_id == "48749425"
        assert result.home_type == "SingleFamily"
        assert (
            result.home_detail_link
            == "http://www.zillow.com/homedetails/"
            + "2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/"
        )
        assert (
            result.graph_data_link
            == "http://www.zillow.com/homedetails/"
            + "2114-Bigelow-Ave-N-Seattle-WA-98109/"
            + "48749425_zpid/#charts-and-data"
        )
        assert result.map_this_home_link == "http://www.zillow.com/homes/48749425_zpid/"
        assert result.tax_year == "2018"
        assert result.tax_value == "1534000.0"
        assert result.year_built == "1924"
        assert result.property_size == "4680"
        assert result.home_size == "3470"
        assert result.bathrooms == "3.0"
        assert result.bedrooms == "4"
        assert result.last_sold_date == "11/26/2008"
        assert result.last_sold_price_currency == "USD"
        assert result.last_sold_price == "995000"
        lat = float(result.latitude)
        assert lat - 0.01 <= 47.637933 <= lat + 0.01
        lng = float(result.longitude)
        assert lng - 0.01 <= -122.347938 <= lng + 0.01
        assert result.zestimate_amount == "2001121"
        # assert result.zestimate_currency == 'USD'
        assert result.zestimate_last_updated == "05/28/2020"
        assert result.zestimate_value_change == "-16739"
        assert result.zestimate_valuation_range_high == "2121188"
        assert result.zestimate_valuation_range_low == "1881054"
        assert result.zestimate_percentile == "0"

    @responses.activate
    def test_get_updated_property_details_results(self):
        """
        Tests parsing of updated_property_details results
        """

        zillow_id = "48749425"
        set_updated_property_details_response(
            self.api_response_obj.get("updated_property_details_200_ok")
        )

        zillow_data = ZillowWrapper(api_key=None)
        updated_property_details_response = zillow_data.get_updated_property_details(
            zillow_id
        )
        result = GetUpdatedPropertyDetails(updated_property_details_response)

        assert result.zillow_id == "48749425"
        assert result.home_type == "SingleFamily"
        assert (
            result.home_detail_link
            == "http://www.zillow.com/homedetails/"
            + "2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/"
        )
        assert (
            result.photo_gallery
            == "http://www.zillow.com/homedetails/"
            + "2114-Bigelow-Ave-N-Seattle-WA-98109/"
            + "48749425_zpid/#image=lightbox%3Dtrue"
        )
        assert (
            result.home_info
            == "http://www.zillow.com/homedetails/"
            + "2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/"
        )
        assert result.year_built == "1924"
        assert result.property_size == "4680"
        assert result.home_size == "3470"
        assert result.bathrooms == "3.0"
        assert result.bedrooms == "4"
        assert result.year_updated == "2003"
        assert result.basement == "Finished"
        assert result.roof == "Composition"
        assert result.view == "Water, City, Mountain"
        assert result.heating_sources == "Gas"
        assert result.heating_system == "Forced air"
        assert (
            result.rooms
            == "Laundry room, Walk-in closet, Master bath, Office,"
            + " Dining room, Family room, Breakfast nook"
        )
        assert result.neighborhood == "Queen Anne"
        assert result.school_district == "Seattle"
        lat = float(result.latitude)
        assert lat - 0.01 <= 47.637933 <= lat + 0.01
        lng = float(result.longitude)
        assert lng - 0.01 <= -122.347938 <= lng + 0.01
        assert result.floor_material is None
        assert result.num_floors == "2"
        assert result.parking_type == "Off-street"
        # assert result.home_description == """Bright, spacious, """

    @classmethod
    def teardown_class(cls):
        pass
