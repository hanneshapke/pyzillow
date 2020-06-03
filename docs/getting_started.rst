Getting started
===============

Obtaining an API key (Zillow Web Service Identifier)
****************************************************
You need an API key from Zillow to request data from the Zillow API. You can apply for an API key by following these instructions: `<https://www.zillow.com/howto/api/APIOverview.htm>`_. Zillow calls API keys 'Zillow Web Service Identifier'.

Initializing the API
********************
To be able to communicate with the API, you first need to initialize a ZillowWrapper object with your API key. For example:

>>> from pyzillow.pyzillow import ZillowWrapper
>>> zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)

Accessing the GetDeepSearchResults API
**************************************
The GetDeepSearchResults API queries the Zillow database for information on a specific address. The endpoint requires the following arguments:

* A street address (e.g. ``'2114 Bigelow Ave'``)
* A ZIP code or city and state combination (e.g. ``'98109'`` or ``'Seattle, WA'``)
* Optional: Enabling or disabling Zillow Rentzestimate information in API results (``True``/``False``)

To query the GetDeepSearchResults API:

>>> from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
>>> zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)
>>> deep_search_response = zillow_data.get_deep_search_results('2114 Bigelow Ave', '98109', True)
>>> result = GetDeepSearchResults(deep_search_response)

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

Access the information by reading the ``GetDeepSearchResults`` object's attributes. For example:

>>> print(result.zillow_id)
48749425
>>> print(result.bathrooms)
3.0

Accessing the GetUpdatedPropertyDetails API
*******************************************
The GetUpdatedPropertyDetails API endpoint requires a Zillow Property ID (ZPID) as an argument. To find this identifier, you can read the attribute ``.zillow_id`` of a GetDeepSearchResults object.

Compared to the GetDeepSearchResults API endpoint described above, the GetUpdatedPropertyDetails API endpoint delivers more details about the object, such as ``.heating_system`` or ``.school_district``.
However, GetUpdatedPropertyDetails data is not available for all valid Zillow Property IDs.

To query the GetUpdatedPropertyDetails API:

>>> from pyzillow.pyzillow import ZillowWrapper, GetUpdatedPropertyDetails
>>> zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)
>>> updated_property_details_response = zillow_data.get_updated_property_details('48749425')
>>> result = GetUpdatedPropertyDetails(updated_property_details_response)

An instance of ``GetDeepSearchResults`` has the following attributes:
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

Access the information by reading the ``GetUpdatedPropertyDetails`` object's attributes. For example:

>>> print(result.home_type)
SingleFamily
>>> print(result.parking_type)
Off-street
