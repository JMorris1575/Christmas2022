===================================
Starting the Christmas 2022 Project
===================================

Starting on December 27, 2021 -- want to change some things while the ideas are fresh in my mind -- rejected word list,
using Base_Dir in mail, post request from Concentration

Want to look up preferred style of rst document headings

Installed sphinx, got version 4.3.2
got the usual upgrade pip, decided to upgrade through PyCharm, didn't find the Christmas2022 version of python at first
but did the second time around after I went to see how Christmas2021 was set up

Installed django, got version 4.0

Installed psycopg2, got version 2.9.2

Copied Christmas2021/christmas21 to Christmas2022, let PyCharm do some of the edits to christmas22

Updated database in secrets.json to c22data (note: the DATABASE_PORT may need to be changed on my home computer)

updated secret key in secrets.json using get_random_secret_key (see start.rst in Christmas2021)

Did python manage.py dumpdata > 2021-12-27-all.json on the jatmorris.org server.

Did python manage.py loaddata 2021-12-27-all.json to clone the server's database on the local machine.
Problems:
#. Needed to migrate first
#. Got an integrity error, need to dumpdata with that special command

Created Christmas2022 repository on github. Activated VCS in PyCharm. Carefully added files to git (not secrets).
Did first commit and first push.