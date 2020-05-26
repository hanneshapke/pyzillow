Getting started
===============

Obtain an API key
*****************
An API key from Zillow is required to request data through the Zillow API. You can apply for an API key by following these instructions: `<https://www.zillow.com/howto/api/APIOverview.htm>`_.

Import pyzillow
***************
To use PyZillow in a project:

>>> import pyzillow

Initialize the API
******************
To be able to communicate with the API, you first need to initialize the ZillowWrapper with your API key:

>>> from pyzillow.pyzillow import ZillowWrapper
>>> zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)

Access the GetDeepSearchResults API
***********************************
The GetDeepSearchResults API queries the Zillow database for information on a specific address. The endpoint requires the following arguments:
    
* A street address (eg ``'2114 Bigelow Ave'``)
* A zip code or city+state combination (eg ``'98109'`` or ``'Seattle, WA'``)
* Optional: Enabeling or disabeling Zillow Rentzestimate information in API results (``True``/``False``)

To query the GetDeepSearchResults API:

>>> from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
>>> zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)
>>> deep_search_response = zillow_data.get_deep_search_results('2114 Bigelow Ave', '98109', True)
>>> result = GetDeepSearchResults(deep_search_response)

An instance of ``GetDeepSearchResults`` has the following attributes:
``.data``
``.zillow_id``
``.home_type``
``.home_detail_link``
``.graph_data_link``
``.map_this_home_link``
``.latitude``
``.longitude``
``.tax_year``
``.tax_value``
``.year_built``
``.property_size``
``.home_size``
``.bathrooms``
``.bedrooms``
``.last_sold_date``
``.last_sold_price``
``.zestimate_amount``
``.zestimate_last_updated``
``.zestimate_value_change``
``.zestimate_valuation_range_high``
``.zestimate_valuation_range_low``
``.zestimate_percentile``
``.rentzestimate_amount``
``.rentzestimate_last_updated``
``.rentzestimate_value_change``
``.rentzestimate_valuation_range_high``
``.rentzestimate_valuation_range_low``

Access the information by calling the ``GetDeepSearchResults`` object's attributes, for example:

>>> print(result.zillow_id)
48749425
>>> print(result.bathrooms)
3.0

Access the GetUpdatedPropertyDetails API
***********************************
The GetUpdatedPropertyDetails API endpoint requires a Zillow Web Service Identifier as an argument. You can acquire this identifier by accessing ``.zillow_id`` from a GetDeepSearchResults object.

To query the GetUpdatedPropertyDetails API:

>>> from pyzillow.pyzillow import ZillowWrapper, GetUpdatedPropertyDetails
>>> zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)
>>> updated_property_details_response = zillow_data.get_updated_property_details('48749425')
>>> result = GetUpdatedPropertyDetails(updated_property_details_response)

An instance of ``GetDeepSearchResults`` has the following attributes:
``.zillow_id``
``.home_type``
``.home_detail_link``
``.graph_data_link``
``.map_this_home_link``
``.latitude``
``.longitude``
``.tax_year``
``.tax_value``
``.year_built``
``.property_size``
``.home_size``
``.bathrooms``
``.bedrooms``
``.last_sold_date``
``.last_sold_price``
``.photo_gallery``
``.home_info``
``.year_updated``
``.floor_material``
``.num_floors``
``.basement``
``.roof``
``.view``
``.parking_type``
``.heating_sources``
``.heating_system``
``.rooms``
``.num_rooms``
``.appliances``
``.neighborhood``
``.school_district``
``.elementary_school``
``.middle_school``
``.home_description``
``.posting_status``
``.posting_type``
``.agent_name``
``.agent_profile_url``
``.brokerage``

Access the information by calling the ``GetUpdatedPropertyDetails`` object's attributes, for example:

>>> print(result.home_type)
SingleFamily
>>> print(result.parking_type)
Off-street
