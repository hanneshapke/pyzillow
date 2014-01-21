#!/usr/bin/env python
#
# Hannes Hapke - Santiago, Chile - 2014
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Unit tests for pyzillow.

"""

import unittest
import sys
import requests
from requests.exceptions import (ConnectionError, TooManyRedirects, 
                                Timeout, HTTPError)

from xml.etree import cElementTree as ElementTree

from api import (ZillowWrapper, 
                 GetDeepSearchResults, GetUpdatedPropertyDetails)

ZILLOW_API_KEY = '' 

MOCK_DATA_GET_DEEP_SEARCH_RESULTS = """<?xml version="1.0" encoding="utf-8"?><SearchResults:searchresults xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.zillow.com/static/xsd/SearchResults.xsd http://www.zillowstatic.com/vstatic/21ea7599abf94ca68a92faf7eec389f2/static/xsd/SearchResults.xsd" xmlns:SearchResults="http://www.zillow.com/static/xsd/SearchResults.xsd"><request><address>2114 Bigelow Ave Seattle, WA</address><citystatezip>98109</citystatezip></request><message><text>Request successfully processed</text><code>0</code></message><response><results><result><zpid>48749425</zpid><links><homedetails>http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/</homedetails><graphsanddata>http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/#charts-and-data</graphsanddata><mapthishome>http://www.zillow.com/homes/48749425_zpid/</mapthishome><comparables>http://www.zillow.com/homes/comps/48749425_zpid/</comparables></links><address><street>2114 Bigelow Ave N</street><zipcode>98109</zipcode><city>Seattle</city><state>WA</state><latitude>47.637933</latitude><longitude>-122.347938</longitude></address><FIPScounty>53033</FIPScounty><useCode>SingleFamily</useCode><taxAssessmentYear>2012</taxAssessmentYear><taxAssessment>902000.0</taxAssessment><yearBuilt>1924</yearBuilt><lotSizeSqFt>4680</lotSizeSqFt><finishedSqFt>3470</finishedSqFt><bathrooms>3.0</bathrooms><bedrooms>4</bedrooms><lastSoldDate>11/26/2008</lastSoldDate><lastSoldPrice currency="USD">1025000</lastSoldPrice><zestimate><amount currency="USD">1236601</amount><last-updated>01/16/2014</last-updated><oneWeekChange deprecated="true"></oneWeekChange><valueChange duration="30" currency="USD">-1187</valueChange><valuationRange><low currency="USD">1150039</low><high currency="USD">1347895</high></valuationRange><percentile>0</percentile></zestimate><localRealEstate><region id="271856" type="neighborhood" name="East Queen Anne"><links><overview>http://www.zillow.com/local-info/WA-Seattle/East-Queen-Anne/r_271856/</overview><forSaleByOwner>http://www.zillow.com/east-queen-anne-seattle-wa/fsbo/</forSaleByOwner><forSale>http://www.zillow.com/east-queen-anne-seattle-wa/</forSale></links></region></localRealEstate></result></results></response></SearchResults:searchresults><!-- H:001  T:28ms  S:1154  R:Mon Jan 20 19:08:34 PST 2014  B:3.0.217083.20140117121245003-comp_rel_b.217083.20140117121441139-comp_rel_b -->"""

MOCK_DATA_GET_UPDATED_PROPERTY_DETAILS = """<?xml version="1.0" encoding="utf-8"?><UpdatedPropertyDetails:updatedPropertyDetails xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.zillow.com/static/xsd/UpdatedPropertyDetails.xsd http://www.zillowstatic.com/vstatic/21ea7599abf94ca68a92faf7eec389f2/static/xsd/UpdatedPropertyDetails.xsd" xmlns:UpdatedPropertyDetails="http://www.zillow.com/static/xsd/UpdatedPropertyDetails.xsd"><request><zpid>48749425</zpid></request><message><text>Request successfully processed</text><code>0</code></message><response><zpid>48749425</zpid><pageViewCount><currentMonth>10672</currentMonth><total>10672</total></pageViewCount><address><street>2114 Bigelow Ave N</street><zipcode>98109</zipcode><city>Seattle</city><state>WA</state><latitude>47.637933</latitude><longitude>-122.347938</longitude></address><links><homeDetails>http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/</homeDetails><photoGallery>http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/#image=lightbox%3Dtrue</photoGallery><homeInfo>http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/</homeInfo></links><editedFacts><useCode>SingleFamily</useCode><bedrooms>4</bedrooms><bathrooms>3.0</bathrooms><finishedSqFt>3470</finishedSqFt><lotSizeSqFt>4680</lotSizeSqFt><yearBuilt>1924</yearBuilt><yearUpdated>2003</yearUpdated><numFloors>2</numFloors><basement>Finished</basement><roof>Composition</roof><view>Water, City, Mountain</view><parkingType>Off-street</parkingType><heatingSources>Gas</heatingSources><heatingSystem>Forced air</heatingSystem><rooms>Laundry room, Walk-in closet, Master bath, Office, Dining room, Family room, Breakfast nook</rooms></editedFacts><neighborhood>Queen Anne</neighborhood><schoolDistrict>Seattle</schoolDistrict><elementarySchool>John Hay</elementarySchool><middleSchool>McClure</middleSchool></response></UpdatedPropertyDetails:updatedPropertyDetails><!-- H:001  T:78ms  S:943  R:Mon Jan 20 19:09:44 PST 2014  B:3.0.217083.20140117121245003-comp_rel_b.217083.20140117121441139-comp_rel_b -->"""


class Test(unittest.TestCase):
    """
    Unit tests for googlemaps.

    """
    def test_zillow_api_results(self):
        """
        """

        address = '2114 Bigelow Ave Seattle, WA'
        zipcode = '98109'
        zpid    = '48749425'

        # create expected result from mock data
        deep_search_mock = ElementTree.XML(MOCK_DATA_GET_DEEP_SEARCH_RESULTS)

        # create response from zillow
        zillow_data = ZillowWrapper(ZILLOW_API_KEY)
        deep_search_response = zillow_data.get_deep_search_results(address, zipcode)

        # compare expected with real result
        self.assertEqual(ElementTree.tostringlist(deep_search_response, encoding="us-ascii", method="xml"), 
                          ElementTree.tostringlist(deep_search_mock, encoding="us-ascii", method="xml"))

    def test_deep_search_results(self):
        """
        """

        address = '2114 Bigelow Ave Seattle, WA'
        zipcode = '98109'

        zillow_data = ZillowWrapper(ZILLOW_API_KEY)
        deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
        result = GetDeepSearchResults(deep_search_response) 

        self.assertEqual(result.zillow_id, '48749425')
        self.assertEqual(result.home_type, 'SingleFamily')
        self.assertEqual(result.home_detail_link, 
          'http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/')
        self.assertEqual(result.graph_data_link, 
          'http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/#charts-and-data')
        self.assertEqual(result.map_this_home_link, 
          'http://www.zillow.com/homes/48749425_zpid/')
        self.assertEqual(result.tax_year, '2012')
        self.assertEqual(result.tax_value, '902000.0')
        self.assertEqual(result.year_built, '1924')
        self.assertEqual(result.property_size, '4680')
        self.assertEqual(result.home_size, '3470')
        self.assertEqual(result.bathrooms, '3.0')
        self.assertEqual(result.bedrooms, '4')
        self.assertEqual(result.last_sold_date, '11/26/2008')
        self.assertEqual(result.last_sold_price_currency, 'USD')
        self.assertEqual(result.last_sold_price, '1025000')
        self.assertAlmostEqual(float(result.latitude), 47.637933, 2)
        self.assertAlmostEqual(float(result.longitude), -122.347938, 2)

    def test_get_updated_property_details_results(self):
        """
        """

        zillow_id = '48749425'

        zillow_data = ZillowWrapper(ZILLOW_API_KEY)
        updated_property_details_response = zillow_data.get_updated_property_details(zillow_id)
        result = GetUpdatedPropertyDetails(updated_property_details_response) 

        self.assertEqual(result.zillow_id, '48749425')
        self.assertEqual(result.home_type, 'SingleFamily')
        self.assertEqual(result.home_detail_link, 
          'http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/')
        self.assertEqual(result.photo_gallery, 
          'http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/#image=lightbox%3Dtrue')
        self.assertEqual(result.home_info, 
          'http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/')
        self.assertEqual(result.year_built, '1924')
        self.assertEqual(result.property_size, '4680')
        self.assertEqual(result.home_size, '3470')
        self.assertEqual(result.bathrooms, '3.0')
        self.assertEqual(result.bedrooms, '4')
        self.assertEqual(result.year_updated, '2003')
        self.assertEqual(result.floors, '2')
        self.assertEqual(result.basement, 'Finished')
        self.assertEqual(result.roof, 'Composition')
        self.assertEqual(result.view, 'Water, City, Mountain')
        self.assertEqual(result.heating_sources, 'Gas')
        self.assertEqual(result.heating_system, 'Forced air')
        self.assertEqual(result.rooms, 
          'Laundry room, Walk-in closet, Master bath, Office, Dining room, Family room, Breakfast nook')
        self.assertEqual(result.neighborhood, 'Queen Anne')
        self.assertEqual(result.school_district, 'Seattle')
        self.assertAlmostEqual(float(result.latitude), 47.637933, 2)
        self.assertAlmostEqual(float(result.longitude), -122.347938, 2)

if __name__ == "__main__":
    unittest.main()