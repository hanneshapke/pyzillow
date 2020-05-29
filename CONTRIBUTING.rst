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

Look through the `GitHub issues <https://github.com/hanneshapke/pyzillow/issues>`_ for bugs. Anything tagged with "bug"
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

Submitzing feedback
~~~~~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/hanneshapke/pyzillow/issues.

If you are proposing a feature:

* Explain in detail how the feature would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Geting started
--------------

Ready to contribute? Here's how to set up PyZillow for
local development.

1. Fork_ the `pyzillow` repo on GitHub.
2. Clone your fork locally::

        $ git clone git@github.com:hanneshapke/pyzillow.git

3. Create a branch for local development::

        $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

4. When you're done making changes, use ``tox`` to check that your changes pass style and unit
   tests, including testing other Python versions::

    $ tox

To get tox, just pip install it.

5. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

.. _Fork: https://github.com/hanneshapke/pyzillow/fork

Submitting a pull request
-------------------------

Check that your pull request meets these guidelines before you submit it:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs have to be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work with Python 3.6, 3.7 and 3.8.
   Check https://travis-ci.org/hanneshapke/pyzillow
   under pull requests for active pull requests or run the ``tox`` command and
   make sure that the tests pass for all supported Python versions.

Running a subset of tests
-------------------------
Use pytest in case you want to run a subset of tests::

    $ pytest test/test_pyzillow.py
