project_name=generic_helpers

.PHONY: check
check:
	./setup.py sdist bdist_wheel
	twine check dist/*
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: release
release:
	make check
	twine upload dist/*


.PHONY: clean
clean:
	rm -rf *.egg *.egg-info
	rm -rf htmlcov
	rm -f .coverage
	find . -name "*.pyc" -exec rm -rf {} \;

.PHONY: patch
patch:
	echo "Making a patch release"
	pipenv run bump2version patch

.PHONY: minor
minor:
	echo "Making a minor release"
	pipenv run bump2version minor


.PHONY: push
push:
	git push origin master --tags


