.PHONY: docs release clean build

clean:
	rm -rf venv htmlcov 
	
build:
	virtualenv --python=python3 venv && . venv/bin/activate && \
	pip install -r requirements.txt
	
test: clean build
	source venv/bin/activate && \
	coverage run --source=watch setup.py test && \
	coverage html && \
	coverage report

fast-test:
	source venv/bin/activate && \
	coverage run --source=watch setup.py test && \
	coverage html && \
	coverage report
	
lint:
	pylint --rcfile=.pylintrc watch -f html &> pylint.html
	

docs:
	sphinx-build -aE docs docs/generated > /dev/null

release: test docs
	open docs/generated/index.html
	open htmlcov/index.html
	vim riss_improved/__init__.py
