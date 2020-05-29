.. complexity documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyZillow
========

A Python library to access the Zillow API
-----------------------------------------

PyZillow is a Python wrapper for `Zillow's API <http://www.zillow.com/howto/api/APIOverview.htm>`_. With PyZillow, you can use a physical address or a Zillow ID to access real estate data from the Zillow database.

Currently, PyZillow supports the **GetDeepSearchResults** and **GetUpdatedPropertyDetails** API endpoints.

Scope of this document
----------------------

This documentation describes how to use PyZillow to access data through the Zillow API in Python.
You will learn how to install PyZillow, initialize the API wrapper with the ZillowConnect class,
and how to use the classes GetDeepSearchResults and GetUpdatedPropertyDetails to request and parse
data from the Zillow API.

Table of contents
-----------------

.. toctree::
   :maxdepth: 1

   installation
   getting_started
   pyzillow
   contributing
   authors
   history
