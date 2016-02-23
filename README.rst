Drama-free Django
=============

This project aims to make Django projects easy to deploy. It provides a command-line tool for bundling your project and it's dependencies into a zip file (called a "build") and later modifying the build to insert environment-specific configuration (called a "release"). These definitions of "build" and "release" are inspired by chapter 5 of The Twelve Factor App: 

http://12factor.net/build-release-run

Dependencies
------------

This has only been tested on 64-bit Linux, with Python 2.7. The system that generates builds needs to have 'pip' and 'wheel' installed, and whatever else is needed to build your Python dependencies. Servers you deploy too must only have a Python 2.7 interpreter, and a server that can run WSGI apps, like Apache with mod_wsgi.

Installation
------------

This package isn't in PyPI yet-- in the meantime, you should be able to install it with:::

   pip install git+https://github.com/cfpb/drama-free-django.git


Make a build
-----

Like this::

   bash@:~$ no-drama build --help
   usage: no-drama build [-h] project_path requirements_file name label

   positional arguments:
     project_path
     requirements_file  just like you would 'pip install -r'
     name               name of this project
     label              a label for this build-- maybe a build ID or version number

   optional arguments:
     -h, --help         show this help message and exit
  
Show users how to use the software. Be specific. Use appropriate
formatting when showing code snippets.

How to test the software
------------------------

If the software includes automated tests, detail how to run those tests.

Known issues
------------

Document any known significant shortcomings with the software.

Getting help
------------

Instruct users how to get help with this software; this might include
links to an issue tracker, wiki, mailing list, etc.

**Example**

If you have questions, concerns, bug reports, etc, please file an issue
in this repository's Issue Tracker.

Getting involved
----------------

This section should detail why people should get involved and describe
key areas you are currently focusing on; e.g., trying to get feedback on
features, fixing certain bugs, building important pieces, etc.

General instructions on *how* to contribute should be stated with a link
to `CONTRIBUTING <CONTRIBUTING.md>`__.

--------------

Open source licensing info
--------------------------

1. `TERMS <TERMS.md>`__
2. LICENSE
3. `CFPB Source Code
   Policy <https://github.com/cfpb/source-code-policy/>`__

--------------

Credits and references
----------------------

1. Projects that inspired you
2. Related projects
3. Books, papers, talks, or other sources that have meaningful impact or
   influence on this project

