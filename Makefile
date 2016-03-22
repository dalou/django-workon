
clean:
	# Remove files not in source control
	find . -type f -name "*.pyc" -delete
	rm -rf nosetests.xml coverage.xml htmlcov *.egg-info *.pdf dist violations.txt

install:
	python setup.py install

rs:
	python manage.py runserver

stylus:
	stylus -w workon/contrib/admin/styl/admin.styl -o workon/static/workon/admin/css/



watch_less:
	python watch_less.py