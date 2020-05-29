.PHONY: help clean clean-pyc clean-build list test test-all coverage docs release sdist

help:
	@echo "clean - remove build artifacts"
	@echo "develop - set up dev environment"
	@echo "install-deps"
	@echo "install-pre-commit"
	@echo "setup-git"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

develop: setup-git install-deps

install-deps:
	pip install -e "file://`pwd`#egg=responses[tests]"

install-pre-commit:
	pip install "pre-commit>=1.10.1,<1.11.0"

setup-git: install-pre-commit
	pre-commit install
	git config branch.autosetuprebase always

lint: install-pre-commit
	@echo "Linting Python files"
	pre-commit run -a
	@echo ""

test: develop lint
	@echo "Running Python tests"
	py.test .
	@echo ""

test-all:
	tox

coverage:
	coverage run --source pyzillow setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/pyzillow.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ pyzillow
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

sdist: clean
	python setup.py sdist
	python setup.py bdist_wheel upload
	ls -l dist
