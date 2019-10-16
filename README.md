# FSRPv2

[![Mozilla Public Licence v2](https://img.shields.io/badge/Licence-MPL--2.0-yellow.svg?style=flat-square)](https://www.mozilla.org/en-US/MPL/)
[![Written for Python 3.7](https://img.shields.io/badge/Written%20in-Python--3.7-green.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org)

![Demo](https://raw.githubusercontent.com/codemicro/FSRPv2/master/doc/2019-10-16_19-39-28.gif "In action")

Rich presence but for flight simulators. It displays the route you're flying, the plane, what network and your current altitude and speed. It connects to your sim using FSUIPC, and feeds that data into Discord. Give it a try!

Supports FSX and P3D, as well as X-Plane (probably - it theoretically should work, but it's not been tested).

Built with Python 3.7 using PyPresence, PyUIPC and PyQt5.

## Installation

To run yourself, you will need to download the FSUIPC SDK [from here](https://www.schiratti.com/dowson.html) and install it into the 32-bit version of Python 3.7 (PyUIPC only works with 32-bit versions of Python). In addition to this, you should install [PyPresence](https://pypi.org/project/pypresence/) and [PyQt5](https://pypi.org/project/PyQt5/) from PyPI.

Once the requirements are installed, make sure your sim has FSUIPC installed into it and you should be able  run "app.py".

## Usage

![GUI](https://raw.githubusercontent.com/codemicro/FSRPv2/master/doc/python_2019-10-16_17-40-10.png "The GUI")

To use, enter details in the boxes provided, connect to your simulator through FSUIPC and then press the "Start presence" button to start the rich presence within Discord. This will make the GUI window disappear, and a console window should remain, in which it will display rubbish that's sorta useful but not really. It prints a line of text every time the status changes in Discord. To stop it, close your sim and it will close, or just close the console window, which will also just stop it.

## Problems?

Open an issue. If it's for general tech support, still open an issue. [Here's how](https://help.github.com/en/articles/creating-an-issue).
