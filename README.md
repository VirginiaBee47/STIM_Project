# LOL STIM

## League of Legends Statistics Tracker and Improvement Manager
STIM is an app to use to help monitor and improve your LOL gameplay. Get it today!
Source Code: "https://github.com/ben-covert2020/STIM_Module"

<br/>

------------

<br/>

## USER GUIDE:

<br/>

### Enter "bEANS47" as the username for real data

<br/>

### **For WINDOWS users**

#### Installing with pip:
```py -m pip install STIM_Module```

<br/>

#### Once the program is installed, run the program with:
```lolstats```

<br/>

#### Uninstall the package:
```py -m pip uninstall -y STIM_Module```

<br/>
<br/>

### **Windows Dev Commands from source code**

#### Build the project:
```py -m build```

<br/>

#### Upload to TestPyPi with Twine:
```twine upload --repository testpypi dist/*```

<br/>

#### Install from TestPyPI with pip:
```py -m pip install --index-url https://test.pypi.org/simple/ --no-deps STIM_Module```

<br/>

#### Upload to PyPi with Twine:
```twine upload dist/*```

<br/>

#### Quickly rebuild application to test code and CLI changes:
```py -m pip uninstall -y STIM_Module && py -m build && py -m pip install dist/STIM_Module-0.3.0-py3-none-any.whl```

<br/>

----------------

<br/>
<br/>

### **For UNIX/macOS users**

#### Installing with pip:
```python3 -m pip install STIM_Module```

<br/>

#### Once the program is installed, RUN the program with:
```lolstats```

<br/>

#### Uninstall the package:
```python3 -m pip uninstall -y STIM_Module```

<br/>

### **UNIX/macOS Dev Commands from source code**

#### Build the project
```python3 -m build```

<br/>

#### Upload to TestPyPi with Twine:
```twine upload --repository testpypi dist/*```

<br/>

#### Install from TestPyPI with pip:
```python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps STIM_Module```

<br/>

#### Upload to PyPi with Twine:
```twine upload dist/*```

<br/>

#### Quickly rebuild application to test code and CLI changes
```python3 -m pip uninstall -y STIM_Module && python3 -m build && python3 -m pip install dist/STIM_Module-0.3.0-py3-none-any.whl```

<br/>
<br/>
<br/>

## Also check the makefile for these common scripts



### DEV NOTES

For local script install, make sure to add this path in wsl

export PATH="$HOME/.local/bin:$PATH"


Using BumpVer to control automatic version numbers

Usage:

version_pattern = "MAJOR.MINOR.PATCH"


Automatic increment:
bumpver update {--major/--minor/--patch}

Do I need -n? Otherwise I have to log into GitHub

Add --dry to see what changes to make sure everything works, check pyproject.toml to ensure each file changes properly