==================
pygeocoder 0.2
==================
Hannes Hapke
Miguel Paolino
20/01/2014


README
------
This is a Python wrapper for Zillow's API.

Currrently it is supporting the GetDeepSearchResults and GetUpdatedPropertyDetails API. 

It allows you to directly convert an address/zipcode (GetDeepSearchResults API) or zillow id (GetUpdatedPropertyDetails API) into
real estate data based on the Zillow database.

License
------
BSD

Dependencies
------------
It has dependency on the xml.etree and requests module, included with Python versions 2.7 and later.
requests library is needed and installed by setuptools.

It is developed on Python 2.7 but should work on earlier versions. Not tested if It is also compatible with Python 3. Sorry.


Installation
------------
You can install this package using pip:

	sudo pip install pyzillow

or download the source from https://github.com/hanneshapke/pyzillow and install

	python setup.py install

Usage
-----
For the GetDeepSearchResults API:

from api import ZillowWrapper, GetDeepSearchResults
...
address = 'YOUR ADDRESS'
zipcode = 'YOUR ZIPCODE'
...
zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)
deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
result = GetDeepSearchResults(deep_search_response) 
...
result.zillow_id # zillow id, needed for the GetUpdatedPropertyDetails

For the GetUpdatedPropertyDetails API:

from api import ZillowWrapper, GetUpdatedPropertyDetails
...
zillow_id = 'YOUR ZILLOW ID'
...
zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)
updated_property_details_response = zillow_data.get_updated_property_details(zillow_id)
result = GetUpdatedPropertyDetails(updated_property_details_response) 
...
result.rooms # number of rooms of the home


Contact Information
-------------------
Author: Hannes Hapke
Twitter: @hanneshapke
Internet: https://github.com/hanneshapke/ 

For comments, issues, requests, please contact via Github at the above website


Changelog
---------
Version 0.2 > API Wrapper for the GetDeepSearchResults and GetUpdatedPropertyDetails API. test.py and setup.py created.

Version 0.1 > Project created