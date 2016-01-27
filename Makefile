
clean:
	# Remove files not in source control
	find . -type f -name "*.pyc" -delete
	rm -rf nosetests.xml coverage.xml htmlcov *.egg-info *.pdf dist violations.txt

install:
	pip install -r reqs/dev.txt


watch_less:
	python watch_less.py