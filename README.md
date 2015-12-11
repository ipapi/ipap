# ipap
Image Processing and Analysis (IPA) Project, Gjøvik University College, 2015

## Setup

### Install Dependencies

This application depends on:
* Python 3
* PyQt5
* NumPy
* Pillow

See below for platform specific instructions

#### Ubuntu

`sudo apt-get install python3 python3-pyqt5`

The rest will be installed in __Prepare Application__.

#### Windows

The latest version of PyQt5 (5.5.1) is only available for Python 3.4 (if you don't build it yourself).
So you will need to use Python 3.4.

1. Install Python 3.4 from https://www.python.org/downloads/windows/
2. Install PyQt5 binaries for Python 3.4 from https://riverbankcomputing.com/software/pyqt/download5
3. Install NumPy binaries for Python 3.4 from http://sourceforge.net/projects/numpy/files/NumPy/
4. Install Pillow by running `easy_install Pillow` in a console

#### Other

You know what to do, or ask us.

### Prepare Application

You might need to replace `python` with `python3` if `python --version` is Python 2.x.

Run `python setup.py develop` in a console in the project directory.

### Run

You might need to replace `python` with `python3` if `python --version` is Python 2.x.

Run `python ipap` in a console in the project directory.
