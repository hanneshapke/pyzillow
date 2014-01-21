class ZillowError(Exception):
    """
    Error messages copied from Zillow\'s API documentation
    http://www.zillow.com/howto/api/GetDeepSearchResults.htm
    """
    code = dict([ 
        (0, 'Request successfully processed'), 
        (1, 'Service error-there was a server-side error while processing the request. \
            Check to see if your url is properly formed: delimiters, character cases, etc.'),
        (2, 'The specified ZWSID parameter was invalid or not specified in the request.\
            Check if you have provided a ZWSID in your API call. \
            If yes, check if the ZWSID is keyed in correctly. \
            If it still doesn\'t work, contact Zillow to get help on fixing \
            your ZWSID.'),
        (3, 'Web services are currently unavailable.\
            The Zillow Web Service is currently not available. \
            Please come back later and try again.'),
        (4, 'The API call is currently unavailable.\
            The Zillow Web Service is currently not available. \
            Please come back later and try again.'),
        (500, 'Invalid or missing address parameter.\
            Check if the input address parameter matches the format specified \
            in the input parameters table. When inputting a city name, the \
            state should also be given. A city name alone will not give \
            a valid address.'),
        (501, 'Invalid or missing citystatezip parameter. \
            Check if the input address parameter matches the format specified \
            in the input parameters table. When inputting a city name, the \
            state should also be given. A city name alone will not give \
            a valid address.'),
        (502, 'No results found. \
            Sorry, the address you provided is not found in the Zillow \
            property database.'),
        (503, 'Failed to resolve city, state or ZIP code.\
            Check if the city-state combination is valid. \
            Also check if you have provided a valid ZIP code.'),
        (504, 'No coverage for specified area  The specified area \
            is not covered by the Zillow property database. To see our \
            property coverage tables, click here.'),
        (505, 'Timeout Your request timed out. The server could be \
            busy or unavailable. Try again later.'),
        (506, 'Address string too long If address is valid, try using \
            abbreviations.'),
        (507, 'No exact match found. Verify that the given address is correct.'),
        ])

    def __init__(self, status, url=None, response=None):
        """

        """
        Exception.__init__(self, status)        # Exception is an old-school class
        self.status = status
        self.message = self.code[int(status)]
        self.url = url
        self.response = response

    def __str__(self):
        return repr(self.message) 

    def __unicode__(self):
        return unicode(self.__str__())


class ZillowFail(Exception):

    def __init__(self):
        Exception.__init__(self)


class ZillowNoResults(Exception):

    def __init__(self):
        Exception.__init__(self)