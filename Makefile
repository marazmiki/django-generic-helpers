project_name=generic_helpers

test:
	pytest

release:
	python setup.py sdist bdist_wheel
	twine upload dist/* --verbose

flake8:
	flake8 .

clean:
	rm -rf *.egg *.egg-info
	rm -rf htmlcov
	rm -f .coverage
	find . -name "*.pyc" -exec rm -rf {} \;
