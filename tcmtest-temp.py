import responses
#from pytest import raises
from pyzillow.pyzillow import (
    ZillowWrapper,
    GetDeepSearchResults,
    GetUpdatedPropertyDetails
)
from pyzillow.pyzillowerrors import ZillowError

ZILLOW_API_KEY = 'X1-ZWz1b88d9eaq6j_1wtus'
# address = '2114 Bigelow Ave Seattle, WA'
# zipcode = '98109'
address = '2114 Bigelow Ave'
zipcode = 'Seattle, WA'

def test_zillow_api_connect(ZILLOW_API_KEY, address, zipcode, zestimate = False):
    zillow_data = ZillowWrapper(ZILLOW_API_KEY)
    zillow_search_response = zillow_data.get_deep_search_results(address, zipcode, zestimate)
    # print(type(zillow_search_response))
    result = GetDeepSearchResults(zillow_search_response)
    #print(type(result))
    return result


def test_updated(ZILLOW_API_KEY, zillow_id):
    zillow_data = ZillowWrapper(ZILLOW_API_KEY)
    updated_property_details_response = zillow_data.get_updated_property_details(zillow_id)
    result = GetUpdatedPropertyDetails(updated_property_details_response)
    return result

# api_result = test_zillow_api_connect(ZILLOW_API_KEY, address, zipcode, True)
# print(api_result.region_name)
# print(api_result.bathrooms)
# print(api_result.zillow_id)
# all_results = api_result.__dict__

# for item in api_result.__dict__.keys():
#     print(f'.{item}')

api_result = test_updated(ZILLOW_API_KEY, '48749425')
# all_results = api_result.__dict__

# for item in api_result.__dict__.keys():
#     print(f'.{item} : {api_result.__dict__[item]}')

element_list = []
for item in api_result.__dict__.keys():
    print(f'``.{item}``')