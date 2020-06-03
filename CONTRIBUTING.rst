Contributing
============

Contributions are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

Types of contributions
----------------------

Reporting bugs
~~~~~~~~~~~~~~

Report bugs at https://github.com/hanneshapke/pyzillow/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fixing bugs
~~~~~~~~~~~

Fixes are always welcome! Look through the `GitHub issues <https://github.com/hanneshapke/pyzillow/issues>`_ for bugs. Anything tagged with "bug"
is open to whoever wants to fix it.

Implementing features
~~~~~~~~~~~~~~~~~~~~~

Look through the `GitHub issues <https://github.com/hanneshapke/pyzillow/issues>`_ for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Writing documentation
~~~~~~~~~~~~~~~~~~~~~

PyZillow could always use more documentation, whether as part of the
official PyZillow docs, in docstrings, or even on the web in blog posts,
articles, or tweets.

Submitting feedback
~~~~~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/hanneshapke/pyzillow/issues.

If you are proposing a feature:

* Explain in detail how the feature would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Getting started
---------------

Ready to contribute? Here's how to set up PyZillow for
local development.

Fork_ the `pyzillow` repo on GitHub.

Clone your fork locally::

   $ git clone git@github.com:hanneshapke/pyzillow.git

Create a branch for local development::

   $ git checkout -b name-of-your-bugfix-or-feature

Create a virtualenv to separate your Python dependencies:

   $ virtualenv .pyzillow-env && source .pyzillow-env/bin/activate

Configure development requirements::

   $ make develop

Now you can make your changes locally.

When you're done making changes, use `Pytest <https://docs.pytest.org/en/latest/>`_ to check that your changes pass style and unit tests, including testing other Python versions. You can run all tests by running pytest::

    $ pytest

Please lint your code before committing your changes::

   $ make lint

Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

Submitting a pull request
-------------------------

Check that your pull request meets these guidelines before you submit it:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs need to be updated. Include
   docstrings with your new functionality (`Sphinx <https://www.sphinx-doc.org/en/stable/usage/extensions/autodoc.html>`_ reStructuredText) and check if you
   need to update the information in the /docs/ folder.
3. The pull request should work with Python 3.6, 3.7 and 3.8. Make sure that
   all tests run by pytest pass.

Running a subset of tests
-------------------------
Use pytest in combination with a substring in case you want to run only specific tests instead of all available tests.
pytest will only run tests with names matching the substring::

    $ pytest -k <substring> -v
