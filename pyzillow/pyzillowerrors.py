class ZillowError(Exception):
    """A ZillowError exception is raised if the API endpoint responded
    with an error code (http://www.zillow.com/howto/api/GetDeepSearchResults.htm).
    """

    code = dict(
        [
            (0, "Request successfully processed"),
            (
                1,
                "Service error-there was a server-side error "
                + "while processing the request. \n "
                + "Check to see if your url is properly formed: delimiters, "
                + "character cases, etc.",
            ),
            (
                2,
                "The specified ZWSID parameter was invalid or "
                + "not specified in the request. \n"
                + "Check if you have provided a ZWSID in your API call. "
                + "If yes, check if the ZWSID is keyed in correctly. "
                + "If it still doesn't work, contact Zillow to "
                + "get help on fixing your ZWSID.",
            ),
            (
                3,
                "Web services are currently unavailable.\n"
                + "The Zillow Web Service is currently not available. "
                + "Please come back later and try again.",
            ),
            (
                4,
                "The API call is currently unavailable.\n"
                + "The Zillow Web Service is currently not available. "
                + "Please come back later and try again.",
            ),
            (6, "This account is not authorized to execute this API call."),
            (7, "Too many requests. \n" + "Daily requests exceeded.",),
            (
                500,
                "Invalid or missing address parameter.\n"
                "Check if the input address parameter "
                + "matches the format specified "
                + "in the input parameters table. When inputting a city name, the "
                + "state should also be given. A city name alone will not give "
                + "a valid address.",
            ),
            (
                501,
                "Invalid or missing citystatezip parameter. "
                + "Check if the input address parameter matches "
                + "the format specified "
                + "in the input parameters table. When inputting a city name, the "
                + "state should also be given. A city name alone will not give"
                + "a valid address.",
            ),
            (
                502,
                "No results found. \n "
                + "Sorry, the address you provided is not found in the Zillow "
                + "property database.",
            ),
            (
                503,
                "Failed to resolve city, state or ZIP code.\n "
                + "Check if the city-state combination is valid. "
                + "Also check if you have provided a valid ZIP code.",
            ),
            (
                504,
                "No coverage for specified area. \nThe specified area "
                + "is not covered by the Zillow property database.",
            ),
            (
                505,
                "Timeout Your request timed out. \nThe server could be "
                + "busy or unavailable. Try again later.",
            ),
            (
                506,
                "Address string too long. \nIf address is valid, try using "
                + "abbreviations.",
            ),
            (
                507,
                "No exact match found. \n"
                + "Verify that the given address is correct.",
            ),
            # this error isn't specified in the zillow doc's,
            # but returned instead of 502
            (508, "No exact match found for input address."),
        ]
    )

    def __init__(self, status, url=None, response=None):
        """Constructor method
        """
        Exception.__init__(self, status)  # Exception is an old-school class
        self.status = status
        self.message = "Status {code}: {text}".format(
            code=status, text=self.code.get(int(status), "Unknown status.")
        )
        self.url = url
        self.response = response

    def __str__(self):
        return self.message


class ZillowFail(Exception):
    """A ZillowFail exception is raised if the API endpoint could not be reached or
       the request did not return valid XML.
    """

    def __init__(self):
        Exception.__init__(self)


class ZillowNoResults(Exception):
    """A ZillowNoResults exception is raised if the request did not return any results.
    """

    def __init__(self):
        Exception.__init__(self)
