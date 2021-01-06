ve:
	test ! -d .ve && python3 -m venv .ve; \
	. .ve/bin/activate; \
	pip install -r requirements.txt; \

clean:
	test -d .ve && rm -rf .ve

runserver:
	.ve/bin/python wsgi.py

victoria:
	export PYTHONPATH="." && .ve/bin/python ./wheels/grosvenorcasinos.py

mrgreen:
	export PYTHONPATH="." && .ve/bin/python ./wheels/mr_green.py