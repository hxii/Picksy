.PHONY=publish
publish:
	poetry build
	poetry publish

.PHONY=clean
clean:
	rm -fr build dist pick.egg-info __pycache__
