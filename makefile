# Signifies our desired python version
# Makefile macros (or variables) are defined a little bit differently than traditional bash, keep in mind that in the Makefile there's top-level Makefile-only syntax, and everything else is bash script syntax.
PYTHON = python3
PACKAGE = STIM_Module
VERSION = 0.3.0

# Defining an array variable
FILES = input output

# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

.PHONY : help hello run test setup clean clean_dist rebuild uninstall upload upload_test install_test install build build_install rebuild_ver


# REGULAR COMMANDS

hello:
	@echo "Hello, world!"

help:
	@echo "---------------HELP-----------------"
	@grep -F ":" Makefile | awk '!/awk/' | awk '!/Description/' | sed -e 's/://'
	@echo "------------------------------------"

run:
	LOLstats

setup: requirements.txt
	${PYTHON} -m pip install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf data/*

clean_dist:
	rm -rf dist

uninstall:
	${PYTHON} -m pip uninstall -y ${PACKAGE}

install:
	${PYTHON} -m pip install ${PACKAGE}

install_test:
	${PYTHON} -m pip install --index-url https://test.pypi.org/simple/ --no-deps ${PACKAGE}


# DEV COMMANDS

upload:
	${PYTHON} -m twine upload dist/*

upload_test:
	${PYTHON} -m twine upload --repository testpypi dist/*

build:
	${PYTHON} -m build

rebuild:
	${PYTHON} -m pip uninstall -y ${PACKAGE} && ${PYTHON} -m build && ${PYTHON} -m pip install dist/${PACKAGE}-${VERSION}-py3-none-any.whl

test:
	${PYTHON} -m pytest


# VERSION SPECIFIC COMMANDS
# make {command}_ver ver={version}

install_ver:
ifdef ver
	${PYTHON} -m pip install ${PACKAGE}==${ver}
else
	@echo "No version specified"
endif

rebuild_ver:
ifdef ver
	${PYTHON} -m pip uninstall -y ${PACKAGE} && ${PYTHON} -m build && ${PYTHON} -m pip install dist/${PACKAGE}-${ver}-py3-none-any.whl
else
	@echo "No version specified"
endif