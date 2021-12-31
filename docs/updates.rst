####################
Updating the Website
####################

Here I will document the changes I made to the website as compared to last year's version. As I begin it is December 30,
2021 so the things I have in mind to change are still fresh in my mind.

*************
Initial Ideas
*************

#. Modify ``wordgame`` to keep a rejected word list and simplify the verification of submitted words. (See
   :ref:`wordgame_update`)
#. Modify ``trivia`` to use Base_Dir to save the question and answer files instead of hard-coding the directory. (See
   :ref:`trivia_update`)
#. Improve the interface with the Concentration game, such as the game being able to send a ``post`` request. (See
   :ref:`concentration_update`)
#. Create a new game involving St. Nicholas. (See :ref:`new_game`)

.. _wordgame_update:

******************************************
Plans for Updating the Christmas Word Game
******************************************

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

Rejecting Words
===============

This will probably be the most difficult change to make. I'm thinking I should create a separate "dictionary" of
rejected words and add to it every time I reject one. This dictionary can be searched for any words that a player
enters that is not included in the main dictionary. If it is there it can be marked "rejected" and displayed in red
in the player's word list for that day. If not, it can be marked to be checked and displayed in grey.

Preliminaries
-------------

Studying ``views.py``
^^^^^^^^^^^^^^^^^^^^^

A quick glance over ``views.py`` indicates that the following functions will be affected:

#. ``clean_words()`` may not be needed, or perhaps it is for when a new ChristmasWord is made available. (It is called
   by ``EntryView()``).
#. ``add_dict_words(word_list)`` may take another parameter (argument?) as to which dictionary to use.
#. ``reject_words`` may end with a call to ``add_dict_words(word_list, dictionary)`` instead of a call to
   ``clean_words()``
#. ``check_words(wordlist, oldlist, current_word)`` will be modified to include checking the list of rejected words.
#. Change ``player_list`` to ``player_word_list`` to make it more clear what the variable represents.
#. Continue from here...

Changes to ``entry.html``
^^^^^^^^^^^^^^^^^^^^^^^^^

Looking over ``entry.html``, and considering the changes above, I see the following possible changes:

#. Change references to ``player_list`` to ``player_word_list``.
#. Add a third box to words that have been rejected for that player on this word so they don't have to add them again.
#. The titles for the three boxes can be: ``Words Accepted``, ``Words To Be Checked`` and ``Words Rejected``.

Changes to ``scoreboard.html``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Some means of identifying the rejected words will have to be developed. Currently the words with a score of 2 get
   displayed in bold green, the ones with a score of 1 in regular green and the rest in light grey. I need a way to
   identify the rejected words that does not affect the score so they can be displayed in red.

Changes to ``check.html``
^^^^^^^^^^^^^^^^^^^^^^^^^

#. The buttons next to each word need to be radio buttons, not checkboxes. It should not be possible for a word to
   be both accepted and rejected.

Miscellaneous Items
^^^^^^^^^^^^^^^^^^^

#. I removed the word "ain't" from the dictionary.
#. I noticed it had some hyphenated words. Should I allow hyphenated words?
#. I changed the name of ``2of12-edited.txt`` to ``dictionary.txt``, changed the two references to it in ``views.py``
   and added it to Git.
#. I created an empty file ``rejected_words.txt`` to hold the rejected words.

Changing How Words are Checked
------------------------------

First I will modify ``check_words(wordlist, oldlist, current_word)`` and get it working, then move on to automatically
adding words to the rejected list when they are rejected and then, finally, adjust the ``html`` files to take this new
feature into account.

Modifying ``check_words()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is the current form of the function::

    def check_words(wordlist, oldlist, current_word):
        '''
        Checks each of the words in wordlist in the following ways:
            1. Is it at least three letters long?
            2. Is it not the same as the given word?
            3. Is it made up only from the letters of the current word?
            4. Is it in the dictionary?
            5. Does it repeat any of the other words in this list?
        :param wordlist: type: list of str - the single words to be checked
        :param oldlist: type: list - the previous words to include in checking for duplicates
        :param current_word: type: str
        :return: type: list - dictionaries for each word in word list each dictionary has the structure:
            { 'word':<player's word>, 'error_msg':<error message about word if any>}
        '''
        dict_file = os.path.join(settings.BASE_DIR, 'wordgame', 'dictionary.txt')
        dictionary = [x.strip() for x in open(dict_file).readlines()]

        given_word = current_word.strip().lower()
        word_info = []      # create the list of dictionaries
        seen = set(oldlist)
        for word in wordlist:
            info = {'word': word, 'error_msg': None}  # create the output information for this word
            # Check against original word
            if word == given_word:
                info['error_msg'] = 'same as given word'
            elif len(word) < 3:                         # check word length
                info['error_msg'] = 'too short'
            elif not can_make_word(word, given_word):   # check to see if word can be made from given_word
                info['error_msg'] = "can't be formed from " + current_word
            elif word not in dictionary:                # check to see if word is in dictionary
                info['error_msg'] = "not in dictionary"
            # Check to see if the word is a duplicate
            if word not in seen:
                seen.add(word)
            else:
                info['error_msg'] = "duplicate"
            word_info.append(info)
        return word_info

I didn't have to change that much, just added the ``rejects`` list and added a check for rejected words BEFORE
the check to see if the word is in the dictionary. (Why check a rejected word to see if it's in the dictionary?)
Here is the result with the changes marked::

    def check_words(wordlist, oldlist, current_word):
        '''
        Checks each of the words in wordlist in the following ways:
            1. Is it at least three letters long?
            2. Is it not the same as the given word?
            3. Is it made up only from the letters of the current word?
            4. Is it in the dictionary?
            5. Has it already been rejected?
            6. Does it repeat any of the other words in this list?
        :param wordlist: type: list of str - the single words to be checked
        :param oldlist: type: list - the previous words to include in checking for duplicates
        :param current_word: type: str
        :return: type: list - dictionaries for each word in word list each dictionary has the structure:
            { 'word':<player's word>, 'error_msg':<error message about word if any>}
        '''
        dict_file = os.path.join(settings.BASE_DIR, 'wordgame', 'dictionary.txt')
        dictionary = [x.strip() for x in open(dict_file).readlines()]
        reject_file = os.path.join(settings.BASE_DIR, 'wordgame', 'rejected_words.txt') # <---Change
        rejects = [x.strip() for x in open(reject_file).readlines()]                    # <---Change

        given_word = current_word.strip().lower()
        word_info = []      # create the list of dictionaries
        seen = set(oldlist)
        for word in wordlist:
            info = {'word': word, 'error_msg': None}  # create the output information for this word
            # Check against original word
            if word == given_word:
                info['error_msg'] = 'same as given word'
            elif len(word) < 3:                         # check word length
                info['error_msg'] = 'too short'
            elif not can_make_word(word, given_word):   # check to see if word can be made from given_word
                info['error_msg'] = "can't be formed from " + current_word
            elif word in rejects:                       # <---Change
                info['error_msg'] = "not accepted"      # <---Change - settled on "not accepted" over "rejected"
            elif word not in dictionary:                # check to see if word is in dictionary
                info['error_msg'] = "not in dictionary"
            # Check to see if the word is a duplicate
            if word not in seen:
                seen.add(word)
            else:
                info['error_msg'] = "duplicate"
            word_info.append(info)
        return word_info

Other changes were needed too. First, in ``clean_words`` I save both the words that were marked
``not in dictionary`` and the ones marked ``not accepted``. Here is how it now looks::

    def clean_words():
        """
        Eliminates all PlayerWords that are rejected for any reason besides "not in dictionary"
        :return: None
        """
        for word in PlayerWord.objects.all():
            if word.explanation:
                if word.explanation not in ['not in dictionary', 'not accepted']:   # <---Change
                    word.delete()

Yet, even after doing that my words that were stubbed into ``rejected_words.txt`` were being removed from
``PlayerWords``. I finally found the culprit in ``EntryView``'s ``post`` routine. It was removing all words
that had previously been rejected. I commented that section out for the time being. If it doesn't cause problems
I will delete those lines.::

    def post(self, request):
        word_number = get_current_word_number()
        try:
            current_word = ChristmasWord.objects.get(sequence_number=word_number)
        except:
            current_word = None
        player_list = PlayerWord.objects.filter(user=request.user, start_word=current_word)
        if request.POST['button'] == 'check':
            # # first remove words previously rejected                  # <---Change
            # for word in player_list:                                  # <---Change
            #     if word.explanation:                                  # <---Change
            #         if word.explanation != 'not in dictionary':       # <---Change
            #             word.delete()                                 # <---Change
            # now get the new words if any
            old_word_list = []
            for word in player_list:
                old_word_list.append(word.word)
            new_word_list = [x.strip().lower() for x in request.POST['word_list'].split(',') if x.strip() != '']
            checked_list = check_words(new_word_list, old_word_list, current_word.word)
            # then add the new checked list - including those marked 'not in dictionary' and 'not accepted'
            for word in checked_list:
                if len(word['word']) > 25:
                    word['word'] = word['word'][0:20] + '...'
                    word['error_msg'] = 'too long'
                # create a new PlayerWord
                player_word = PlayerWord(word=word['word'], user=request.user, start_word=current_word)
                if word['error_msg']:
                    player_word.explanation = word['error_msg']
                if player_word.explanation != 'duplicate':      # saving the duplicates is causing trouble
                    player_word.save()
            return redirect('wordgame:entry')
        if request.POST['button'] == 'comment':
            comment = request.POST['comment'].strip()
            if current_word:
                new_comment = WordComment(comment=comment, player=request.user, daily_word=current_word)
            else:
                new_comment = GameComment(comment=comment, player=request.user)
            new_comment.save()
            return redirect('wordgame:entry')

Implementing the Rejection of Words
-----------------------------------

There are a few things to do here:

#. Add to the ``rejected_words.txt`` file when I have marked words as rejected.
#. Improve the functionality of ``verify.html``.
#. Report the rejected words to the players in both ``entry.html`` and ``scoreboard.html``.

Adding to ``rejected_words.txt``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This was amazingly easy. I changed the definition of ``add_dict_words`` to the following::

    def add_dict_words(word_list, dict_filename):
        '''
        Adds the word_list to the given dictionary, sorts and saves the dictionary
        :param word_list: list of str: the words to be added to the dictionary
        :return: None
        '''
        dict_file = os.path.join(settings.BASE_DIR, 'wordgame', dict_filename)
        dictionary = [x.strip() for x in open(dict_file).readlines()]
        for word in word_list:
            if word not in dictionary:
                dictionary.append(word)
        dictionary.sort()
        f = open(dict_file, "w")
        for word in dictionary:
            f.write(word + '\n')
        f.close()

And then altered the two calls to ``add_dict_words()``, one in ``reject_words`` and one in the ``post`` method of
``VerifyView``, to include the appropriate dictionary filename, either ``dictionary.txt`` or ``rejected_words.txt``.

Radio Buttons in ``verify.html``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For radio buttons to work they must all be in the same group, indicated by the ``name=`` parameter(?). I need to have
several groups of radio buttons, one group for each word so I used the word itself as the group name.

I decided to use bootstrap's fancier radio buttons which are labelled with their name.

Also, I needed a way to leave a word to be checked later if I so desired and that would be impossible if I only had two
radio buttons: ``Accept`` and ``Reject``. Once I clicked on one I would not be able to unclick it. I decided to add a
third button: ``Wait`` which will turn off the other two if selected. The default is no to do anything so I guess I can
set the ``Wait`` button to checked at the beginning. I could do that by typing ``checked`` after value="wait" in the
``Wait`` button's ``<input>`` line, but I decided I didn't like the way it looked.

Finally I wanted all three buttons to be the same size and eventually figured out how to use ``col`` and ``px`` to make
it look the way I wanted.

The last button, the ``Wait`` button is rounded on the right. I couldn't figure out how to change that.

Here is the final form of the changes I made::

    <table class="table text-center text-success">
        <thead>
            <tr>
                <th scope="col">Start Word</th>
                <th scope="col">Player Word</th>
                <th scope="col">Options</th>
            </tr>
        </thead>
        <tbody>
            {% for word in rejected %}
                <tr>
                    <th scope="row">{{ word.start_word }}</th>
                    <td>{{ word.word }}</td>
                    <td>
                        <div class="btn-group" role="group">
                            <input type="radio" class="btn-check" name="{{ word.word }}" id="{{ word.word }}-1" value="accept"/>
                            <label class="btn btn-outline-success col-4 px-4" for="{{ word.word }}-1">Accept</label>
                            <input type="radio" class="btn-check" name="{{ word.word }}" id="{{ word.word }}-2" value="reject"/>
                            <label class="btn btn-outline-danger col-4 px-4" for="{{ word.word }}-2">Reject</label>
                            <input type="radio" class="btn-check" name="{{ word.word }}" id="{{ word.word }}-3" value="wait"/>
                            <label class="btn btn-outline-info col-4 px-4" for="{{ word.word }}-3">Wait</label>
                        </div>
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>

Editing the ``post`` Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^


made changes to the post method of VerifyView having to do with how radio buttons work.


.. _trivia_update:

****************************************************************
Updating the Way the Trivia Game Saves Question and Answer Files
****************************************************************

This was the easiest update and so the one I started with. All I had to do was add a couple of imports at the beginning
of ``trivia/views.py`` and alter the ``open`` statements that set up writing to the files. Note the use of
``os.path.join`` rather than just ``os.join`` (I had tried the latter first.)::

    from django.conf import settings
    import os

    question_file = open(os.path.join(settings.BASE_DIR, 'Christmas_Trivia_Questions.txt', 'w'))
    ...
    answer_file = open(os.path.join(settings.BASE_DIR, 'Christmas_Trivia_Answers.txt', 'w'))


.. _concentration_update:

*************************************************************
Plans for Improving the Interface with the Concentration Game
*************************************************************

.. _new_game:

*******************************************
Plans for a New Game Involving St. Nicholas
*******************************************

I got this idea when I started working with Godot but haven't been ready to implement it until now. I'm hoping that this
sort of game will attract the kids to the website while still being fun for the adults too. The game will be based on
topdown-shooter tutorials, such as the one at https://www.youtube.com/channel/UCLzFt-NdfCm8WFKTyqD0yJw but that doesn't
involve shooting people, but instead, St. Nicholas throwing bags of gold into the homes of poor people.

I am working on the tutorial cited above and hope to learn enough to develop a fully-working game with several levels
that are fun to play.

