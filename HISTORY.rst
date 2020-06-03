.. :changelog:

Version history
---------------


0.7.0 (2020-05-30)
++++++++++++++++++

* Updated error handling, too many request error, Github issue 18
* Updated error handling, error 6 (Github issue 6)
* Pinned python-coveralls to latest version 2.9.3 (#27)
* Added posting details to GetUpdatedPropertyDetails result (#10)
* Updated pytest version (#32)
* Updated coverage version (#28)
* Added support for additional API fields (#16)

Thanks to Alexandra M. Chace (#16), Marilyn Chace, Evan Pete Walsh (#11), Stephen Holsapple (#10), ZAD-Man (Issue #6)


0.6.0 (2020-05-28)
++++++++++++++++++

* Updated tests, incl. complete API mocking
* Updated test dependencies
* Removed Python 2 support

0.5.0 (2015-09-12)
++++++++++++++++++

* Removed Django dependency, mocked tests, Python 3.4 support

0.4.0 (2014-12-20)
++++++++++++++++++

* Zestimate extracted from Zillow's GetDeepSearchResults API.

0.3.1 (2014-12-20)
++++++++++++++++++

* Added test cases and increased test coverage setup.

0.3.0 (2014-12-19)
++++++++++++++++++

* Refactored structure, travis CI compliance, coverage setup.

0.2.7
++++++++++++++++++

* Bug fix: Missing ParseError, numRooms now read from UpdatedProperty

0.2.6
++++++++++++++++++

* Bug fix

0.2.5
++++++++++++++++++

* Using markdown as README file for setup.py

0.2.4
++++++++++++++++++

* Coordinates provides as GEOS point

0.2.3
++++++++++++++++++

* New attributes added: home_description, num_floors, floor_material, parking_type

0.2.2
++++++++++++++++++

* Licence changed to MIT

0.2.1
++++++++++++++++++

* pip created and code refactured

0.2
++++++++++++++++++

* API Wrapper for the GetDeepSearchResults and GetUpdatedPropertyDetails API. test.py and setup.py created.

0.1
++++++++++++++++++

* Project created
