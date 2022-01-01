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

.. _entry_view_post:

Yet, even after doing that my words that were stubbed into ``rejected_words.txt`` were being removed from
``PlayerWords``. I finally found the culprit in ``EntryView``'s ``post`` routine. It was removing all words
that had previously been rejected. I commented that section out for the time being. If it doesn't cause problems
I will delete those lines.

.. note:: These lines are necessary but need to be modified to include words marked "not accepted." The correct form is
    shown below.

Here is the correct current form of the ``post`` method::

    def post(self, request):
        word_number = get_current_word_number()
        try:
            current_word = ChristmasWord.objects.get(sequence_number=word_number)
        except:
            current_word = None
        player_list = PlayerWord.objects.filter(user=request.user, start_word=current_word)
        if request.POST['button'] == 'check':
            # first remove words previously rejected
            for word in player_list:
                if word.explanation:
                    if word.explanation not in ['not in dictionary', 'not accepted']:
                        word.delete()
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

The selected radio buttons send their information in ``request.POST`` with the words themselves as the keys and the
values being ``accept``, ``reject`` or ``wait``. This meant there had to be a few changes in ``VerifyView``'s ``post``
method. I needed to get the ``word_list`` of all distince words that were marked ``not in dictionary``. I iterated
through these words, the same list the ``get`` method sent to ``verify.html`` and, if they were in ``request.POST``'s
keys, because the ones I didn't click wouldn't be, they got sorted into the accepted or rejected words. These lists were
used to update their respective dictionaries and marked accordingly. The current form of the ``post`` method is
displayed below::

    def post(self, request, ):
        if request.POST['button'] == 'ok':
            word_list = PlayerWord.objects.filter(explanation='not in dictionary').distinct('word')
            accepted_words = []
            rejected_words = []
            for word in word_list:
                if word.word in request.POST.keys():
                    if request.POST[word.word] == 'accept':
                        accepted_words.append(word.word)
                    elif request.POST[word.word] == 'reject':
                        rejected_words.append(word.word)
                    # else I clicked on "Wait" or didn't click at all
            add_dict_words(accepted_words, 'dictionary.txt')
            reject_words(rejected_words)        # marks them 'not accepted' and puts them in rejected_words.txt
            word_number = get_current_word_number()
            UserModel = get_user_model()
            users = UserModel.objects.all()
            update_game(word_number, users, all=True)
            clean_words()
        return redirect('wordgame:scoreboard')

Editing ``entry.html``
^^^^^^^^^^^^^^^^^^^^^^

Planning
""""""""

Currently, when a player enters words, one box opens with a simple list of the words accepted and another box next to
it, now marked "Words Currently Rejected", that shows a vertical list of those words with the reason each was rejected.
The next time the player entered words the ones that could not be made with the letters of the given word, or were
rejected for some other fatal reason, were removed from ``PlayerWords`` and did not appear. The words that had not been
found in the dictionary, however, remained until I accepted or rejected them. Previously, once I rejected a word, it
was removed from ``PlayerWords`` and no longer appeared in this list. Words I accepted moved to their first list.

I want to maintain a lot of that behavior but use the list of words marked ``not accepted`` to signal to the player that
they need not use them again and also not keep showing up in the verify list. I think I need to do a narrative walk-
through to get a clear idea of what I want:

Janet comes to the wordgame and finds that the word of the day is "Festive." She writes "feast, vest, stive, vit, vits,
fives" in the entry box and clicks the "Check Words" button.

Unknown to her, Madeline had already played the game and I had rejected the words "vit" and "vits." Thus, when the
entry page refreshes Janet now sees, three boxes under the entry box: one for her words that have been accepted, one for
her word that have been rejected, and one to report on the unscored words and the reason they were not scored. It might
look something like the following::

    Accepted:                    Rejected:                  Unscored:
    vest                         vit, vits                  feast - can't be formed from festive
                                                            fives - not in dictionary
                                                            stive - not in dictionary

The next time she adds words, the word "feast" will not appear in the ``Unscored`` column but "stive" and "fives" will
remain there until I accept or reject them. In this examples "fives" would be accepted but "stive" would not.

Implementation
""""""""""""""

All the sifting of the words seems to be done in the templeate ``entry.html`` rather than the ``get`` method so that's
all I have to change. Here is what I ended up with in the section after the form where the words are entered::

    {% if player_word_list %}
        <div class="row justify-content-around mb-3">
            <div class="card col-md-3 text-success border-success pb-2">
                <h4 class="card-header bg-white px-0">Accepted:</h4>
                {% for word in player_word_list %}
                    {% if not word.explanation %}
                        {% if forloop.last %}
                            {{ word }}
                        {% else %}
                            {{ word }},
                        {% endif %}
                    {% endif %}
                {% endfor %}
            </div>
            <div class="card col-md-3 border-success text-danger pb-2">
                <h4 class="card-header px-0 bg-white">Rejected:</h4>
                {% for word in player_word_list %}
                    {% if word.explanation == 'not accepted' %}
                        {% if forloop.last %}
                            {{ word }}
                        {% else %}
                            {{ word }},
                        {% endif %}
                    {% endif %}
                {% endfor %}
            </div>
            <div class="card col-md-3 border-success text-success pb-2">
                <h4 class="card-header px-0 bg-white">Unscored:</h4>
                {% for word in player_word_list %}
                    {% if word.explanation and word.explanation != 'not accepted' %}
                        {{ word }} - {{ word.explanation }}<br>
                    {% endif %}
                {% endfor %}
            </div>
        </div>
    {% endif %}

While checking this I discovered the real use for the word deletion that was taking place in the ``post`` method. It was
originally meant to delete the words that were rejected for reasons other than not being in the dictionary. I had to
modify it so that it also doesn't delete words that have been tried but ``not accepted``. See
:ref:`EntryView.post <entry_view_post>`.

In order to fit everything into the narrower boxes, I had to change the "can't be formed from..." message to
"not from...".

Editing ``scoreboard.html``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This turned out to be easy, though it also required one small change to ``ScoreboardView``'s ``get`` method. Here are
the changes made to the section of ``scoreboard.html`` that prints the list of words::

    <td>
        {% for word in player.words %}
            {% if word.score == 2 %}
                <strong>{{ word.word }}</strong>
            {% elif word.score == 1 %}
                {{ word.word }}
            {% elif word.explanation == 'not in dictionary' %}
                <inline class="text-black-50">{{ word.word }}</inline>
            {% elif word.explanation == 'not accepted' %}
                <inline class="text-danger">{{ word.word }}</inline>
            {% endif %}                 # a professional programmer would have an else here to catch outliers
        {% endfor %}
    </td>

The change needed in ``ScoreboardView``'s ``get`` method was one single character! I noticed that the red words, the
rejected ones were coming first. It turned out to be because the lists of each player's words in ``stats`` were ordered
by the score and then by the word. Adding a negative sign before ``score`` changed it to reverse order -- which is good
in another way too: it makes sense to have the highest scoring words come first.

Here is the section of the ``get`` method I changed::

    for player in player_list:
        words = PlayerWord.objects.filter(start_word=word, user=player.user).order_by('-score', 'word')
        word_dict['players'].append({'name': player.user.username, 'words': words})
    stats.append(word_dict)

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

