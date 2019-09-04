.PHONY: clean

ACTIVATE = source venv/bin/activate

dist : venv
	# TODO: Note that this distribution is incomplete.  We're not properly
	# building the cspice or starcat modules, which require some
	# cross-platform magic and for which I'll need some help.  But this is
	# enough to be able to start work on pds-webtools, so I'm
	# intentionally publishing incomplete work, with this warning.
	$(ACTIVATE) && python setup.py sdist

venv : requirements.txt
	virtualenv --no-site-packages -p python2.7 $@
	$(ACTIVATE) && pip install -r requirements.txt

clean :
	-find . -name '*~' -delete
	-find . -name '#*' -delete
	-find . -name '*.pyc' -delete
	-rm -rf dist venv MANIFEST

