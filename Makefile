test:
	python setup.py test

release:
	python setup.py sdist --format=zip,bztar,gztar register upload


flake8:
	flake8 --ignore=E501 generic_helpers
	flake8 --ignore=E501 tests.py
	flake8 --ignore=E501 setup.py


coverage:
	coverage run --include=generic_helpers/* setup.py test
	coverage html


coveralls:
	coveralls

clean:
	rm -rf *.egg *.egg-info
	rm -rf htmlcov
	rm -f .coverage
	find . -name "*.pyc" -exec rm -rf {} \;
