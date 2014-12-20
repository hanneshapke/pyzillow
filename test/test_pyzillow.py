#!/usr/bin/env python
#
# Hannes Hapke - Santiago, Chile and Portland, Oregon - 2014

"""
Tests for `pyzillow` module.
"""
from pytest import raises
from pyzillow.pyzillow import (
    ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails)
from pyzillow.pyzillowerrors import ZillowError


class TestPyzillow(object):

    @classmethod
    def setup_class(cls):
        cls.ZILLOW_API_KEY = 'X1-ZWz1b88d9eaq6j_1wtus'
        cls.address = '2114 Bigelow Ave Seattle, WA'
        cls.zipcode = '98109'

    def test_zillow_api_connect(self):
        # create response from zillow and check for error code '0'
        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)
        zillow_search_response = zillow_data.get_deep_search_results(
            self.address, self.zipcode)
        assert \
            zillow_search_response.find('message').find('code').text == '0'

    def test_zillow_error_invalid_ZWSID(self):
        # This test checks the correct error message if no ZWSID is provided.
        # Expected error code: 2
        zillow_data = ZillowWrapper(None)
        raises(
            ZillowError,
            zillow_data.get_deep_search_results,
            address=self.address,
            zipcode=self.zipcode)

    def test_zillow_error_missing_address(self):
        # This test checks the correct error message if no address is provided.
        # Expected error code: 500
        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)
        raises(
            ZillowError,
            zillow_data.get_deep_search_results,
            address=None,
            zipcode=self.zipcode)

    def test_zillow_error_missing_zipcode(self):
        # This test checks the correct error message if no zipcode is provided.
        # Expected error code: 501
        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)
        raises(
            ZillowError,
            zillow_data.get_deep_search_results,
            address=self.address,
            zipcode=None)

    def test_zillow_error_no_property_match(self):
        # This test checks the correct error message if no property is found.
        # Expected error code: 508
        # Address and zip code of an exisiting property, but not listed
        address = '599 Pennsylvania Avenue Northwest, Washington, DC'
        zipcode = '20001'
        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)
        raises(
            ZillowError,
            zillow_data.get_deep_search_results,
            address=address,
            zipcode=zipcode)

    def test_zillow_error_match_zipcode_city(self):
        # This test checks the correct error message if no zipcode is provided.
        # Expected error code: 503
        mismatch_zipcode = '97204'  # Portland, OR
        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)
        raises(
            ZillowError,
            zillow_data.get_deep_search_results,
            address=self.address,
            zipcode=mismatch_zipcode)

    def test_zillow_error_invalid_zipcode(self):
        # This test checks the correct error message if an
        # invalid zipcode is provided.
        # Expected error code: 503
        invalid_zipcode = 'ABCDE'  # invalid zipcode
        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)
        raises(
            ZillowError,
            zillow_data.get_deep_search_results,
            address=self.address,
            zipcode=invalid_zipcode)

    def test_zillow_error_no_coverage(self):
        # This test checks the correct error message
        # if no coverage is provided.
        # Expected error code: 504
        address = 'Calle 21 y O, Vedado, Plaza, Ciudad de la Habana, Cuba'
        zipcode = '10400'  # Cuban address, I assume Zillow doesn't cover Cuba
        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)
        raises(
            ZillowError,
            zillow_data.get_deep_search_results,
            address=address,
            zipcode=zipcode)

    def test_deep_search_results(self):
        """
        """

        address = '2114 Bigelow Ave Seattle, WA'
        zipcode = '98109'

        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)
        deep_search_response = zillow_data.get_deep_search_results(
            address, zipcode)
        result = GetDeepSearchResults(deep_search_response)

        assert result.zillow_id == '48749425'
        assert result.home_type == 'SingleFamily'
        assert result.home_detail_link == \
            'http://www.zillow.com/homedetails/' + \
            '2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/'
        assert result.graph_data_link == \
            'http://www.zillow.com/homedetails/' + \
            '2114-Bigelow-Ave-N-Seattle-WA-98109/' + \
            '48749425_zpid/#charts-and-data'
        assert result.map_this_home_link == \
            'http://www.zillow.com/homes/48749425_zpid/'
        assert result.tax_year == '2013'
        assert result.tax_value == '995000.0'
        assert result.year_built == '1924'
        assert result.property_size == '4680'
        assert result.home_size == '3470'
        assert result.bathrooms == '3.0'
        assert result.bedrooms == '4'
        assert result.last_sold_date == '11/26/2008'
        assert result.last_sold_price_currency == 'USD'
        assert result.last_sold_price == '1025000'
        lat = float(result.latitude)
        assert lat - 0.01 <= 47.637933 <= lat + 0.01
        lng = float(result.longitude)
        assert lng - 0.01 <= -122.347938 <= lng + 0.01
        assert result.zestimate_amount == '1434364'
        # assert result.zestimate_currency == 'USD'
        assert result.zestimate_last_updated == '12/18/2014'
        assert result.zestimate_value_change == '18880'
        assert result.zestimate_valuation_range_high == '1577800'
        assert result.zestimate_valuationRange_low == '1247897'
        assert result.zestimate_percentile == '0'

    def test_get_updated_property_details_results(self):
        """
        """

        zillow_id = '48749425'

        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)
        updated_property_details_response = \
            zillow_data.get_updated_property_details(zillow_id)
        result = GetUpdatedPropertyDetails(updated_property_details_response)

        assert result.zillow_id == '48749425'
        assert result.home_type == 'SingleFamily'
        assert result.home_detail_link == \
            'http://www.zillow.com/homedetails/' + \
            '2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/'
        assert result.photo_gallery == \
            'http://www.zillow.com/homedetails/' + \
            '2114-Bigelow-Ave-N-Seattle-WA-98109/' + \
            '48749425_zpid/#image=lightbox%3Dtrue'
        assert result.home_info == \
            'http://www.zillow.com/homedetails/' + \
            '2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/'
        assert result.year_built == '1924'
        assert result.property_size == '4680'
        assert result.home_size == '3470'
        assert result.bathrooms == '3.0'
        assert result.bedrooms == '4'
        assert result.year_updated == '2003'
        assert result.basement == 'Finished'
        assert result.roof == 'Composition'
        assert result.view == 'Water, City, Mountain'
        assert result.heating_sources == 'Gas'
        assert result.heating_system == 'Forced air'
        assert result.rooms == \
            'Laundry room, Walk-in closet, Master bath, Office,' + \
            ' Dining room, Family room, Breakfast nook'
        assert result.neighborhood == 'Queen Anne'
        assert result.school_district == 'Seattle'
        lat = float(result.latitude)
        assert lat - 0.01 <= 47.637933 <= lat + 0.01
        lng = float(result.longitude)
        assert lng - 0.01 <= -122.347938 <= lng + 0.01
        assert result.floor_material is None
        assert result.num_floors == '2'
        assert result.parking_type == 'Off-street'
        # assert result.home_description == """Bright, spacious, """

    @classmethod
    def teardown_class(cls):
        pass
