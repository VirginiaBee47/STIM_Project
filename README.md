#### League of Legends

# Example Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

STIM is an app to use to help monitor and improve your LOL gameplay.



### USER GUIDE:

## For building and uploading, you need to be in the STIM_Module directory


## For WINDOWS users:

# Installing with pip
```py -m pip install STIM_Module```py

# Once the program is installed, run the program with:
```LOLstats```py


# Install requirment packages
```py -m pip install -r requirements.txt```py

# Uninstall the package:
```py -m pip uninstall -y STIM_Module```py


## Windows Dev Commands from source code

# Build the project
```py -m build```py



# Upload to TestPyPi with Twine:
```twine upload --repository testpypi dist/*```py

# Install from TestPyPI with pip:
```py -m pip install --index-url https://test.pypi.org/simple/ --no-deps STIM_Module```py

# Upload to PyPi with Twine:
```twine upload dist/*```py

# Quickly rebuild application to test code and CLI changes
Make sure to change the version number to the correct version you're on but it doesn't matter too much I think
```py -m pip uninstall -y STIM_Module && py -m build && py -m pip install dist/STIM_Module-0.0.2-py3-none-any.whl```py




## For UNIX/macOS users:

# Installing with pip
```python3 -m pip install STIM_Module```py

# Once the program is installed, RUN the program with:
```applic```py


# Uninstall the package:
```python3 -m pip uninstall -y STIM_Module```py

# Install requirment packages
```python3 -m pip install -r requirements.txt```py



## UNIX/macOS Dev Commands from source code

# Build the project
```python3 -m build```py

# Upload to TestPyPi with Twine:
```twine upload --repository testpypi dist/*```py

# Install from TestPyPI with pip:
```python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps STIM_Module```py

# Upload to PyPi with Twine:
```twine upload dist/*```py

# Quickly rebuild application to test code and CLI changes
Make sure to change the version number to the correct version you're on but it doesn't matter too much I think
```python3 -m pip uninstall -y STIM_Module && python3 -m build && python3 -m pip install dist/STIM_Module-0.0.2-py3-none-any.whl```py





## Also check the makefile for these common scripts