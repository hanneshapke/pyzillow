import os
import responses


DEEP_SEARCH_URL = "http://www.zillow.com/webservice/GetDeepSearchResults.htm"
PROPERTY_DETAIL_URL = "http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm"

XML_RESPONSE = {
    "get_deep_search_200_ok": "get_deep_search_200_ok.xml",
    "updated_property_details_200_ok": "updated_property_details_200_ok.xml",
    "error_2_zwsid_missing": "error_2_zwsid_missing.xml",
    "error_6_account_not_authorized": "error_6_account_not_authorized.xml",
    "error_500_no_address_provided": "error_500.xml",
    "error_501_no_city_state": "error_501.xml",
    "error_508_invalid_address": "error_508_invalid_address.xml",
    "error_508_invalid_zipcode": "error_508_invalid_zipcode.xml",
    "error_508_outside_of_area": "error_508_outside_of_area.xml",
}


def set_get_deep_search_response(body):
    responses.add(
        responses.GET,
        DEEP_SEARCH_URL,
        body=body,
        content_type="application/xml",
        status=200,
    )


def set_updated_property_details_response(body):
    responses.add(
        responses.GET,
        PROPERTY_DETAIL_URL,
        body=body,
        content_type="application/xml",
        status=200,
    )


class APIReponses(object):
    @staticmethod
    def load_response(key):
        BASE_PATH = "test/xml_payloads/"
        file_name = XML_RESPONSE[key]
        with open(os.path.join(BASE_PATH, file_name), "r") as content_file:
            return content_file.read()

    def get(self, key):
        rs = self.load_response(key)
        return rs
