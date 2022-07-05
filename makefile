
run:
	python test.py

setup: requirements.txt
	pip install -r requirements.txt

clean:
	rm -rf __pycache__

reload:
	python -m pip uninstall -y STIM_Module && python -m build && python -m pip install dist/STIM_Module-0.0.2-py3-none-any.whl