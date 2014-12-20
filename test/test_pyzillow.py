#!/usr/bin/env python
#
# Hannes Hapke - Santiago, Chile and Portland, Oregon - 2014

"""
Tests for `pyzillow` module.
"""
from pyzillow.pyzillow import (
    ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails)


class TestPyzillow(object):

    @classmethod
    def setup_class(cls):
        cls.ZILLOW_API_KEY = 'X1-ZWz1b88d9eaq6j_1wtus'

    def test_zillow_api_results(self):
        address = '2114 Bigelow Ave Seattle, WA'
        zipcode = '98109'

        # create response from zillow and check for error code '0'
        zillow_data = ZillowWrapper(self.ZILLOW_API_KEY)
        zillow_search_response = zillow_data.get_deep_search_results(
            address, zipcode)

        assert zillow_search_response.find('message').find('code').text == \
            '0'

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
