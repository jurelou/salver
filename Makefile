.PHONY: all install venv lint test run doc autodoc clean

PROJECT 		?= opulence
CELERY_APP		?= opulence.app
HOST 			?= $(shell hostname)
VENV_NAME		?= venv
VENV_BIN		?= $(shell pwd)/${VENV_NAME}/bin
VENV_ACTIVATE	?= . ${VENV_BIN}/activate

CELERY_LOGLEVEL	?= info

PYTHON 			?= ${VENV_BIN}/python3



export FLASK_APP=frontend/run.py

all:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "make \033[36m%-15s\033[0m %s\n", $$1, $$2}'

reinstall: clean install ## make clean + make install.

install: ## Create python virtual environment and install dependencies
	make clean; make venv

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip setuptools
	${PYTHON} -m pip install -r requirements.txt
	${PYTHON} -m pip install -e .
	touch $(VENV_NAME)/bin/activate

flower: venv ## Launch celery monitoring tool.
	. venv/bin/activate ; \
	flower --app $(CELERY_APP) --broker=redis://:thisisaverrygoodpassword@localhost/0

engine: venv ## Launch engine worker.
	. venv/bin/activate ; \
	celery worker --app=$(CELERY_APP) --loglevel=$(CELERY_LOGLEVEL) --hostname=worker.engine@%h --queues=engine -c 3

collector: venv ## Launch scan worker.
	. venv/bin/activate ; \
	celery worker --app=$(CELERY_APP) --loglevel=$(CELERY_LOGLEVEL) --hostname=worker.collectors@%h --queues=collectors -c 10

lint: venv ## Run linter on project.
	. venv/bin/activate ; \
	${PYTHON} -m pylint --rcfile=.pylintrc $(PROJECT)

test: venv ## Run tests on project.
	. venv/bin/activate ; \
	@cd $(PROJECT); $(PYTHON) -m unittest discover

doc: venv ## Build documenation.
	. venv/bin/activate ; \
	sphinx-build docs docs/_html

autodoc: venv ## Automatically re-build documenation.
	. venv/bin/activate ; \
	sphinx-autobuild docs docs/_html

autopep8:
	. venv/bin/activate ; \
	autopep8 --in-place --aggressive --aggressive --recursive $(PROJECT)

clean: ## Remove python artifacts and virtualenv.
	find . -name '*.pyc' -exec rm --force {} +
	@rm -rf $(VENV_NAME) *.eggs *.egg-info dist build docs/_html .cache
