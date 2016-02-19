#!/usr/bin/env python
#

"""
Tests for `pyzillow` module.
"""

import responses
from pytest import raises
from pyzillow.pyzillow import (
    ZillowWrapper,
    GetDeepSearchResults,
    GetUpdatedPropertyDetails
)
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
        address = 'not a valid address'
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

    @responses.activate
    def test_deep_search_results(self):
        """
        """

        address = '2114 Bigelow Ave Seattle, WA'
        zipcode = '98109'

        responses.add(
            responses.GET,
            'http://www.zillow.com/webservice/GetDeepSearchResults.htm',
            body='<?xml version="1.0" encoding="utf-8"?><SearchResults:searchresults xsi:schemaLocation="http://www.zillow.com/static/xsd/SearchResults.xsd http://www.zillowstatic.com/vstatic/34794f0/static/xsd/SearchResults.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SearchResults="http://www.zillow.com/static/xsd/SearchResults.xsd"><request><address>2114 Bigelow Ave Seattle, WA</address><citystatezip>98109</citystatezip></request><message><text>Request successfully processed</text><code>0</code></message><response><results><result><zpid>48749425</zpid><links><homedetails>http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/</homedetails><graphsanddata>http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/#charts-and-data</graphsanddata><mapthishome>http://www.zillow.com/homes/48749425_zpid/</mapthishome><comparables>http://www.zillow.com/homes/comps/48749425_zpid/</comparables></links><address><street>2114 Bigelow Ave N</street><zipcode>98109</zipcode><city>Seattle</city><state>WA</state><latitude>47.637933</latitude><longitude>-122.347938</longitude></address><FIPScounty>53033</FIPScounty><useCode>SingleFamily</useCode><taxAssessmentYear>2014</taxAssessmentYear><taxAssessment>1060000.0</taxAssessment><yearBuilt>1924</yearBuilt><lotSizeSqFt>4680</lotSizeSqFt><finishedSqFt>3470</finishedSqFt><bathrooms>3.0</bathrooms><bedrooms>4</bedrooms><lastSoldDate>11/26/2008</lastSoldDate><lastSoldPrice currency="USD">1025000</lastSoldPrice><zestimate><amount currency="USD">1419804</amount><last-updated>09/10/2015</last-updated><oneWeekChange deprecated="true"></oneWeekChange><valueChange duration="30" currency="USD">20690</valueChange><valuationRange><low currency="USD">1292022</low><high currency="USD">1547586</high></valuationRange><percentile>0</percentile></zestimate><localRealEstate><region name="East Queen Anne" id="271856" type="neighborhood"><zindexValue>629,900</zindexValue><links><overview>http://www.zillow.com/local-info/WA-Seattle/East-Queen-Anne/r_271856/</overview><forSaleByOwner>http://www.zillow.com/east-queen-anne-seattle-wa/fsbo/</forSaleByOwner><forSale>http://www.zillow.com/east-queen-anne-seattle-wa/</forSale></links></region></localRealEstate></result></results></response></SearchResults:searchresults><!-- H:003  T:27ms  S:1181  R:Sat Sep 12 23:30:47 PDT 2015  B:4.0.19615-release_20150908-endor.2fa5797~candidate.358c83d -->',
            content_type='application/xml',
            status=200
        )

        zillow_data = ZillowWrapper(api_key=None)
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
        assert result.tax_year == '2014'
        assert result.tax_value == '1060000.0'
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
        assert result.zestimate_amount == '1419804'
        # assert result.zestimate_currency == 'USD'
        assert result.zestimate_last_updated == '09/10/2015'
        assert result.zestimate_value_change == '20690'
        assert result.zestimate_valuation_range_high == '1547586'
        assert result.zestimate_valuation_range_low == '1292022'
        assert result.zestimate_percentile == '0'
        
    @responses.activate
    def test_get_updated_property_details_results(self):
        """
        """

        zillow_id = '48749425'
        responses.add(
            responses.GET,
            'http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm',
            body='<?xml version="1.0" encoding="utf-8"?><UpdatedPropertyDetails:updatedPropertyDetails xmlns:UpdatedPropertyDetails="http://www.zillow.com/static/xsd/UpdatedPropertyDetails.xsd" xsi:schemaLocation="http://www.zillow.com/static/xsd/UpdatedPropertyDetails.xsd http://www.zillowstatic.com/vstatic/34794f0/static/xsd/UpdatedPropertyDetails.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><request><zpid>48749425</zpid></request><message><text>Request successfully processed</text><code>0</code></message><response><zpid>48749425</zpid><pageViewCount><currentMonth>16125</currentMonth><total>16125</total></pageViewCount><address><street>2114 Bigelow Ave N</street><zipcode>98109</zipcode><city>Seattle</city><state>WA</state><latitude>47.637933</latitude><longitude>-122.347938</longitude></address><links><homeDetails>http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/</homeDetails><photoGallery>http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/#image=lightbox%3Dtrue</photoGallery><homeInfo>http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/</homeInfo></links><images><count>1</count><image><url>http://photos3.zillowstatic.com/p_d/ISxb3qa8s1cwx01000000000.jpg</url></image></images><editedFacts><useCode>SingleFamily</useCode><bedrooms>4</bedrooms><bathrooms>3.0</bathrooms><finishedSqFt>3470</finishedSqFt><lotSizeSqFt>4680</lotSizeSqFt><yearBuilt>1924</yearBuilt><yearUpdated>2003</yearUpdated><numFloors>2</numFloors><basement>Finished</basement><roof>Composition</roof><view>Water, City, Mountain</view><parkingType>Off-street</parkingType><heatingSources>Gas</heatingSources><heatingSystem>Forced air</heatingSystem><rooms>Laundry room, Walk-in closet, Master bath, Office, Dining room, Family room, Breakfast nook</rooms></editedFacts><neighborhood>Queen Anne</neighborhood><schoolDistrict>Seattle</schoolDistrict><elementarySchool>John Hay</elementarySchool><middleSchool>McClure</middleSchool></response></UpdatedPropertyDetails:updatedPropertyDetails><!-- H:001  T:127ms  S:990  R:Sat Sep 12 23:47:31 PDT 2015  B:4.0.19615-release_20150908-endor.2fa5797~candidate.358c83d -->',
            content_type='application/xml',
            status=200
        )

        zillow_data = ZillowWrapper(api_key=None)
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
