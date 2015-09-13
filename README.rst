==================
pyzillow 0.3
==================

By Hannes Hapke & Miguel Paolino

10/09/2015
.. image:: https://travis-ci.org/hanneshapke/pyzillow.png?branch=master
    :target: https://travis-ci.org/hanneshapke/pyzillow

.. image:: https://pypip.in/d/pyzillow/badge.png
    :target: https://pypi.python.org/pypi/pyzillow

.. image:: https://coveralls.io/repos/hanneshapke/pyzillow/badge.png
  :target: https://coveralls.io/r/hanneshapke/pyzillow
=======
README
------
This is a Python wrapper for [Zillow's API](http://www.zillow.com/howto/api/APIOverview.htm).

Currrently it supports the GetDeepSearchResults and GetUpdatedPropertyDetails APIs.

It allows you to directly convert an address/zipcode (GetDeepSearchResults API) or zillow id (GetUpdatedPropertyDetails API) into real estate data from the Zillow database.

Documentation available here: http://pyzillow.readthedocs.org/en/latest/
.. image:: https://readthedocs.org/projects/pyzillow/badge/?version=latest
  :target: https://readthedocs.org/projects/pyzillow

=======
Dependencies
------------
It requires the xml.etree module, included with Python versions 2.7 and later.
The [requests](http://docs.python-requests.org/en/latest/index.html) library is also needed and will be installed by setuptools.

It is developed on Python 2.7 but should work on earlier versions. We have not tested it with Python 3. Sorry.

Currently it is supporting the GetDeepSearchResults and GetUpdatedPropertyDetails API.

It allows you to directly convert an address/zipcode (GetDeepSearchResults API) or zillow id (GetUpdatedPropertyDetails API) into
real estate data based on the Zillow database.

Installation
------------
You can install this package using pip:

    pip install pyzillow

or download the source from https://github.com/hanneshapke/pyzillow and install

    python setup.py install


Usage of the GetDeepSearchResults API
-------------------------------------

    from pyzillow import ZillowWrapper, GetDeepSearchResults
    ...
    address = 'YOUR ADDRESS'
    zipcode = 'YOUR ZIPCODE'
    ...
    zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)
    deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
    result = GetDeepSearchResults(deep_search_response)
    ...
    result.zillow_id # zillow id, needed for the GetUpdatedPropertyDetails

The following attributes are currently supported:

    - zillow_id
    - home_type
    - home_detail_link
    - graph_data_link
    - map_this_home_link
    - latitude
    - latitude
    - coordinates (as GEOS point)
    - tax_year
    - tax_value
    - year_built
    - property_size
    - home_size
    - bathrooms
    - bedrooms
    - last_sold_date
    - last_sold_price_currency
    - last_sold_price
    - zestimate_amount
    - zestimate_last_updated
    - zestimate_value_change
    - zestimate_valuation_range_high
    - zestimate_valuationRange_low
    - zestimate_percentile


Usage of the GetUpdatedPropertyDetails API
------------------------------------------

    from pyzillow import ZillowWrapper, GetUpdatedPropertyDetails
    ...
    zillow_id = 'YOUR ZILLOW ID'
    ...
    zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)
    updated_property_details_response = zillow_data.get_updated_property_details(zillow_id)
    result = GetUpdatedPropertyDetails(updated_property_details_response)
    ...
    result.rooms # number of rooms of the home

The following attributes are currently supported:

    - zillow_id
    - home_type
    - home_detail_link
    - photo_gallery
    - latitude
    - latitude
    - coordinates (as GEOS point)
    - year_built
    - property_size
    - home_size
    - bathrooms
    - bedrooms
    - home_info
    - year_updated
    - floor_material
    - num_floors
    - basement
    - roof
    - view
    - parking_type
    - heating_sources
    - heating_system
    - rooms
    - home_description
    - neighborhood
    - school_district

The following attributes are not provided by the API:

    - graph_data_link
    - map_this_home_link
    - tax_year
    - tax_value
    - last_sold_date
    - last_sold_price_currency
    - last_sold_price


Contact Information
-------------------
Author: Hannes Hapke (renooble)
Twitter: @hanneshapke

Internet: https://github.com/hanneshapke/

For comments, issues, requests, please contact via Github at the above website


Changelog
---------
- Version 0.5 > Removed django.contrib.gis.geos dependency, remove Django from the pip requirements, moved requirements to separate folder
- Version 0.4 > DepreciationWarning: def coordinates(self) will not be supported in version 0.5
- Version 0.3.1 > Merged PR
- Version 0.3 > pip created and code refactored
- Version 0.2 > API Wrapper for the GetDeepSearchResults and GetUpdatedPropertyDetails API. test.py and setup.py created.
- Version 0.1 > Project created
