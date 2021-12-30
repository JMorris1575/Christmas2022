###################################
Starting the Christmas 2022 Project
###################################

.. note:: Starting on December 27, 2021

*************
Initial Ideas
*************

I decided to start next year's Christmas website early this year. I want to change some things while the ideas are fresh
in my mind. Here are my initial plans:

#. Modify ``wordgame`` to keep a rejected word list and simplify the verification of submitted words. (See
   :ref:`wordgame_update`)
#. Modify ``trivia`` to use Base_Dir to save the question and answer files instead of hard-coding the directory. (See
   :ref:`trivia_update`)
#. Improve the interface with the Concentration game, such as the game being able to send a ``post`` request. (See
   :ref:`concentration_update`)
#. Create a new game involving St. Nicholas. (See :ref:`new_game`)

.. _wordgame_update:

Plans for Updating the Christmas Word Game
==========================================

I noticed that I had to reject the same words over and over when finalizing them this year. I thought it would be easier
if the system saved the rejected words and didn't display them on the verify page once they had been rejected. They
could also be kept in the players' word lists but not scored and they could see that their words had been rejected.
Currently they just disappear. Here are some thoughts:

#. Display the rejected words in red as soon as they are entered (and known to be rejected).
#. Option: If a player convinces me to count a word, remove it from rejected words and add it to the dictionary.
#. Option: You could take points off for guessing.

You may also want to revise the rules of the game.

Thoughts on Scoring: Perhaps using all the letters of a word to form a new word should be worth more points. Perhaps the
scoring should take the length of the words into account. I doubt it though. The one and two point thing seems to be
working well enough.

.. _trivia_update:

Updating the Way the Trivia Game Saves Question and Answer Files
================================================================

This was the easiest update and so the one I started with. All I had to do was add a couple of imports at the beginning
of ``trivia/views.py`` and alter the ``open`` statements that set up writing to the files. Note the use of
``os.path.join`` rather than just ``os.join`` (I had tried the latter first.)::

    from django.conf import settings
    import os

    question_file = open(os.path.join(settings.BASE_DIR, 'Christmas_Trivia_Questions.txt', 'w'))
    ...
    answer_file = open(os.path.join(settings.BASE_DIR, 'Christmas_Trivia_Answers.txt', 'w'))


.. _concentration_update:

Plans for Improving the Interface with the Concentration Game
=============================================================

.. _new_game:

Plans for a New Game Involving St. Nicholas
===========================================

I got this idea when I started working with Godot but haven't been ready to implement it until now. I'm hoping that this
sort of game will attract the kids to the website while still being fun for the adults too. The game will be based on
topdown-shooter tutorials, such as the one at https://www.youtube.com/channel/UCLzFt-NdfCm8WFKTyqD0yJw but that doesn't
involve shooting people, but instead, St. Nicholas throwing bags of gold into the homes of poor people.

I am working on the tutorial cited above and hope to learn enough to develop a fully-working game with several levels
that are fun to play.

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

