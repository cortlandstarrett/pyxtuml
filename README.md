pyxtuml [![Build Status](https://travis-ci.org/john-tornblom/pyxtuml.svg?branch=master)](https://travis-ci.org/john-tornblom/pyxtuml)	[![Coverage Status](https://coveralls.io/repos/john-tornblom/pyxtuml/badge.svg?branch=master)](https://coveralls.io/r/john-tornblom/pyxtuml?branch=master)
========
pyxtuml is a python library for parsing, manipulating, and generating [BridgePoint](https://www.xtuml.org) xtUML models.

### Getting Started
pyxtuml depend on the following software packages:
* [python](http://python.org) (tested with v2.7)
* [ply](http://www.dabeaz.com/ply) (tested with v3.4)

For people running Ubuntu, all packages are available via apt-get.
```
$ sudo apt-get install python2.7 python-ply
```

Once the dependencies have been met, the source code needs to be prepared by issuing the following set of commands.
```
$ git clone https://github.com/john-tornblom/pyxtuml.git
$ cd pyxtuml
$ python setup.py prepare
```

Optionally, you can also execute a test suite:
```
$ python setup.py test
```

Next, install pyxtuml on your system:
```
$ python setup.py install
```

Or if you prefer, install only for the current user:
```
$ python setup.py install --user
```

### Usage example
The [examples folder](https://github.com/john-tornblom/pyxtuml/tree/master/examples) contains a few scripts which demonstrate how pyxtuml may be used.

The following command will create an empty metamodel and populate it with some sample data:
```
$ python examples/create_external_entity.py > test.sql
```
Copy the SQL statements saved in test.sql to your clipboard, and paste them into the BridgePoint editor with a project selected in the project explorer.

If you are on a more recent GNU/Linux system, you can also pipe the output directly to your clipboard without bouncing via disk:
```
$ python examples/create_external_entity.py | xclip -selection clipboard
```

### Reporting bugs
If you encounter problems with pyxtuml, please [file a github issue](https://github.com/john-tornblom/pyxtuml/issues/new). 
If you plan on sending pull request which affect more than a few lines of code, please file an issue before you start to work on you changes.
This will allow us to discuss the solution properly before you commit time and effort.

### License
pyxtuml is licensed under the GPLv3, see LICENSE for more information.
