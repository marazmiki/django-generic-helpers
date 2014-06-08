test:
	python setup.py test

flake8:
	flake8 --ignore=E501 generic_helpers
	flake8 --ignore=E501 tests.py
	flake8 --ignore=E501 setup.py


coverage:
	coverage run --include=generic_helpers/* ./tests.py
	coverage html
