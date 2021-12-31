###################################
Starting the Christmas 2022 Project
###################################

.. note:: Starting on December 27, 2021

I decided to start next year's Christmas website early this year. I want to change some things while the ideas are fresh
in my mind. Here are my initial plans:

********************
Starting the Project
********************

Here are the steps I followed in starting the project:

#. Used PyCharm to start the ``Christmas2022`` project using Python 3.9 and its own virtual environment ``venv``.
#. Installed sphinx with ``pip install sphinx``. This installed version 4.3.2.

   A. I got the usual upgrade pip suggestion
   #. I decided to upgrade through PyCharm but it didn't find the Christmas2022 version of python at first
   #. It did the second time around after I went to see how Christmas2021 was set up and returned to
      File->Settings->Project->Project Interpreter

#. Installed django with ``pip install django`` and got version 4.0.
#. Installed psycopg2 with ``pip install psycopg2`` and got version 2.9.2.
#. Copied Christmas2021/christmas21 to Christmas2022, let PyCharm do some of the edits to christmas22 and taking care
   of others by hand.
#. Updated the dates in ``header.html``, ``base.html`` and ``footer.html``.
#. Updated secret key in ``secrets.json`` using get_random_secret_key. (see start.rst in Christmas2021)
#. Updated database in ``secrets.json`` to ``c22data`` (note: DATABASE_PORT may need to be changed on my home computer)
#. Used ``pgAdmin 4`` to create the ``c22data`` database on the local machine.
#. Performed a ``python manage.py migrate`` command to prepare the database.
#. Used ``ssh -p 7822 jim@jatmorris.org`` to do a ``python manage.py dumpdata --indent=4 -e sessions -e admin``
   ``-e contenttypes -e auth.Permission > 2021-12-28-all.json`` on the server.
#. Copied the resulting file with FileZilla to perform a ``python manage.py loaddata 2021-12-29.json`` on the local
   machine.
#. Checked the functionality with ``python manage.py runserver``.
#. Created Christmas2022 repository on github.
#. Enabled VCS in PyCharm using Git.
#. Carefully added files to git (not secrets).
#. Did first commit and first push.

***************************************
Moving the Project to the Home Computer
***************************************

Here is the process I followed to clone the Christmas2022 project onto my home computer:

#. In a project that used Git, in this case Christmas2021, I selecte ``Git->Clone...`` from the menu and provided the
   URL to github.
#. After a little bit a yellow bar appeared at the top of the PyCharm edit screen telling me I had no Python Interpreter
   configured. It offered me the chance to do so and I selected Python3.9 (venv).
#. Unfortunately, it took (venv) from Christmas2021 as evidenced from doing ``which python`` in the Terminal.
#. In ``File->Settings...`` I selected ``Python Interpreter`` and clicked the gear next to the box indicating the
   Christmas2021 (venv). It allowed me to set up a virtual environment here on this computer.
#. I had to exit the project and re-enter it before the correct venv could be used.
#. ``pip install sphinx`` gave me version 4.3.2, as before.
#. ``pip install django`` gave me version 4.0, as before.
#. ``pip install psycopg2`` gave me version 2.9.3, which is different from before (2.9.2). This may give me a chance to
   learn about upgrading programs through pip.
#. Used ``dwseervice`` to download ``secrets.json`` from my Omen computer to ``config/settings`` in this project.
#. Used PgAdmin 4 to create a local ``c22data`` database.
#. Changed the ``DATABASE_PORT`` in ``secrets.json`` to 5434 as is needed on this machine.
#. Performed ``python manage.py migrate`` without much problem. (I first forgot to get into the ``christmas22``
   directory.
#. Performed ``python manage.py loaddata 2021-12-28-all.json`` which happily installed 3902 objects from one fixture.
#. Tested it with python manage.py runserver and it worked fine!

Notes on Moving Sphinx
======================

When I tried ``make html`` without first doing a ``sphinx-quickstart`` it didn't work of course. It didn't have the
``make.bat`` file. I used DWService to copy ``conf.py``, ``make.bat`` and ``Makefile`` to the home computer. It changed
the name of ``make.bat`` to ``make.bat.txt`` and I had to change it back, but then ``make html`` worked perfectly well
except it warned me to create a ``_static`` folder. I have added ``conf.py``, ``make.bat`` and ``Makefile`` to Git.

