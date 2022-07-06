.PHONY : run setup clean rebuild uninstall upload upload_test install_test install build build_install

# Makefile for the project
run:
	LOLstats

setup: requirements.txt
	python3 -m pip install -r requirements.txt

clean:
	rm -rf __pycache__

rebuild:
	python3 -m pip uninstall -y STIM_Module && python3 -m build && python3 -m pip install dist/STIM_Module-0.0.2-py3-none-any.whl

uninstall:
	python3 -m pip uninstall -y STIM_Module

install_test:
	python3 -m pip install -r requirements.txt

install:
	python3 -m pip install STIM_Module

upload:
	twine upload dist/*

upload_test:
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps STIM_Module

build:
	python3 -m build

build_install:
	python3 -m build && python3 -m pip install dist/STIM_Module-0.0.2-py3-none-any.whl