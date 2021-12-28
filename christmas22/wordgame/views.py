from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import PermissionDenied
from django.db.models import Count, Sum
from django.conf import settings


from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import ChristmasWord, PlayerWord, WordComment, GameComment

from datetime import datetime, timedelta
from operator import itemgetter

import os

import utilities

def set_dates():
    '''
    Makes sure the dates for all the ChristmasWords are sequential
    :return: None
    '''
    for word in ChristmasWord.objects.all():
        if word.sequence_number == 1:
            start_date = word.date_published
        else:
            word.date_published = start_date + timedelta(days = word.sequence_number - 1)
            word.save()

def get_current_word_number():
    '''
    Uses today's date and the date_published of the first word to determine today's word
    :return: an integer representing the sequence_number of today's word
    '''
    delta = datetime.now().date() - ChristmasWord.objects.get(sequence_number=1).date_published
    if delta.days + 1 <= ChristmasWord.objects.count():
        return delta.days + 1
    else:
        return ChristmasWord.objects.count() + 1

def clean_words():
    """
    Eliminates all PlayerWords that are rejected for any reason besides "not in dictionary"
    :return: None
    """
    for word in PlayerWord.objects.all():
        if word.explanation:
            if word.explanation != 'not in dictionary':
                word.delete()

def add_dict_words(word_list):
    '''
    Adds the word_list to the dictionary, sorts and saves the dictionary
    :param word_list: list of str: the words to be added to the dictionary
    :return: None
    '''
    dict_file = os.path.join(settings.BASE_DIR, 'wordgame', '2of12-edited.txt')
    dictionary = [x.strip() for x in open(dict_file).readlines()]
    for word in word_list:
        if word not in dictionary:
            dictionary.append(word)
    dictionary.sort()
    f = open(dict_file, "w")
    for word in dictionary:
        f.write(word + '\n')
    f.close()

def reject_words(word_list):
    """
    Marks the explanation of the given words as 'rejected' in every PlayerWord where it appears then removes those
    entries with a call to clean_words()
    :parameter: word_list: str - the word that is to be rejected
    :return: None
    """
    for word in word_list:
        rejected = PlayerWord.objects.filter(word=word)
        for item in rejected:
            item.explanation = 'rejected'
            item.save()
    clean_words()

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
    dict_file = os.path.join(settings.BASE_DIR, 'wordgame', '2of12-edited.txt')
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

def can_make_word(word, given_word):
    '''
    Checks to see if the players word can be made from the letters of the given word
    :param word: str: the player's word
    :param given_word: the given_word
    :return: True if the word can be made, False otherwise
    '''
    letters = list(given_word)
    for letter in word:
        if letter in letters:
            letters.remove(letter)
        else:
            return False
    return True


def update_game(current_word_number, users, all=False):
    '''
    Updates player scores for all ChristmasWords not yet finalized
    Finalizes words with sequence_numbers < word_number
    :param word_number: int: the current word number for today's date
    :return: None
    '''
    if all:
        christmas_words = ChristmasWord.objects.filter(sequence_number__lte=current_word_number)
    else:
        christmas_words = ChristmasWord.objects.filter(sequence_number=current_word_number)
    # iterate through each of the ChristmasWords
    for given_word in christmas_words:
        # only check the ones that have been used so far
        score_word(given_word, users)
        if given_word.sequence_number < current_word_number:
            given_word.finalized = True
            given_word.save()

def score_word(given_word, users):
    """
    Calculates each user's score for the given_word and updates the database
    :param sequence_number: type: integer - the sequence_number of the ChristmasWord to be scored
    :param users: type: QuerySet - the set of users
    :return: None
    """
    shared = []
    unique = []
    # first give one point to each accepted word
    for user in users:
        player_words = PlayerWord.objects.filter(start_word=given_word, user=user)
        if player_words:
            word_list = []
            for word in player_words:
                word_list.append(word.word)
            checked = check_words(word_list, [], given_word.word)
            for item in checked:
                word = item['word']
                if not item['error_msg']:
                    if word not in shared:
                        if word in unique:
                            shared.append(word)
                            unique.remove(word)
                        else:
                            unique.append(word)
                    word_record = PlayerWord.objects.get(start_word=given_word, user=user, word=word)
                    word_record.score = 1
                    word_record.explanation = ''    # in case word has just been added to dictionary
                    word_record.save()
                else:       # update explanation
                    word_record = PlayerWord.objects.get(start_word=given_word, user=user, word=word)
                    word_record.explanation = item['error_msg']
                    word_record.save()
    # now add an extra point for each unique word
    for user in users:
        player_words = PlayerWord.objects.filter(start_word=given_word, user=user)
        if player_words:
            for word in player_words:
                if not word.explanation:
                    if word.word in unique:
                        word.score += 1
                        word.save()

def get_scores(sequence_number, users):
    '''
    gets the scores for each user for the given christmas_word
    :param sequence_number: type: int - the sequence_number of the ChristmasWord to be scored for all users
    :return: type: list - a list of dictionaries containing the scores for each user for christmas_word
            format: [ {'user':user, 'score':score}, ...]
    '''
    christmas_word = ChristmasWord.objects.get(sequence_number=sequence_number)
    unsorted_scores = []
    sorted_scores = []      # give it something to return if no players have a list for this word
    for user in users:
        player_list = PlayerWord.objects.filter(user=user, start_word=christmas_word)
        if player_list:
            score = 0
            for word in player_list:
                score += word.score
            unsorted_scores.append({'user':user, 'score':score})
            sorted_scores = sorted(unsorted_scores, key=itemgetter('score'), reverse=True)
    return sorted_scores

def get_total_scores(users):
    '''
    Gets every player's total score but returns it only if score > 0
    :return: type: list of dictionaries each dictionary of the form {'name': user_name, 'total_score': total_score
                                                                     'rounds': rounds, 'words': words}
    '''
    unsorted_totals = []
    for user in users:
        score_info = PlayerWord.objects.filter(user=user).aggregate(total_score=Sum('score'))
        if score_info['total_score']:
            score_info['name'] = user.username
            score_info['words'] = PlayerWord.objects.filter(user=user, explanation='').count()
            start_words = set()
            for word in PlayerWord.objects.filter(user=user):
                start_words.add(word.start_word)
            score_info['rounds'] = len(start_words)
            unsorted_totals.append(score_info)
    totals = sorted(unsorted_totals, key=itemgetter('total_score'), reverse=True)
    return totals


class ScoreboardView(View):
    template_name = 'wordgame/scoreboard.html'

    def get(self, request):
        christmas_words = ChristmasWord.objects.filter(date_published__lt=datetime.now())
        stats = []
        for word in christmas_words:
            word_dict = {'given_word': word, 'players': []}
            player_list = PlayerWord.objects.filter(start_word=word).distinct('user')
            for player in player_list:
                words = PlayerWord.objects.filter(start_word=word, user=player.user).order_by('score', 'word')
                word_dict['players'].append({'name': player.user.username, 'words': words})
            stats.append(word_dict)
        UserModel = get_user_model()
        users = UserModel.objects.all()
        total_scores = get_total_scores(users)
        context = {'memory': utilities.get_random_memory(), 'stats': stats, 'totals': total_scores}
        return render(request, self.template_name, context)


class DailyScoreView(View):
    template_name = 'wordgame/daily_scores.html'

    def get(self, request, word_number=None):
        word_number = get_current_word_number()
        if word_number >= 1:
            UserModel = get_user_model()
            users = UserModel.objects.all()
            daily_scores = []
            for day in range(1, word_number):
                date = ChristmasWord.objects.get(sequence_number=day).date_published
                word = ChristmasWord.objects.get(sequence_number=day).word
                heading = date.strftime("%b %d, %Y") + ": " + word
                daily_scores.append({ 'heading': heading, 'scores': get_scores(day, users)})
        context = {'memory': utilities.get_random_memory(), 'daily_scores': daily_scores}
        return render(request, self.template_name, context)

class EntryView(View):
    template_name = 'wordgame/entry.html'

    def get(self, request):
        set_dates()         # to do this only once after a new word is displayed you need a new field in ChristmasWord
        word_number = get_current_word_number()
        if word_number < 1:
            date_one = ChristmasWord.objects.get(sequence_number=1).date_published
        else:
            date_one = None
        try:
            current_word = ChristmasWord.objects.get(sequence_number=word_number)
        except:
            current_word = None
        # chores to be performed when a new ChristmasWord is first displayed
        if not PlayerWord.objects.filter(start_word=current_word):
            set_dates()
            clean_words()
        UserModel = get_user_model()
        users = UserModel.objects.all()
        update_game(word_number, users)
        if current_word:
            scores_today = get_scores(word_number, users)
        else:
            scores_today = None
        if word_number > 1:
            scores_yesterday = get_scores(word_number-1, users)   # after last day word_number-1 = last ChristmasWord number
        else:
            scores_yesterday = []                                 # on the first day there are no scores from yesterday
        if current_word:
            player_list = PlayerWord.objects.filter(user=request.user, start_word=current_word).order_by('word')
            comments = WordComment.objects.filter(daily_word=current_word)
        else:
            player_list = None
            comments = GameComment.objects.all()
        context = {'memory': utilities.get_random_memory(), 'current_word': current_word, 'date_one':date_one,
                   'player_list': player_list, 'today': scores_today, 'yesterday': scores_yesterday,
                   'comments': comments}
        return render(request, self.template_name, context)

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
                    if word.explanation != 'not in dictionary':
                        word.delete()
            # now get the new words if any
            old_word_list = []
            for word in player_list:
                old_word_list.append(word.word)
            new_word_list = [x.strip().lower() for x in request.POST['word_list'].split(',') if x.strip() != '']
            checked_list = check_words(new_word_list, old_word_list, current_word.word)
            # then add the new checked list - including those marked 'not in dictionary'
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

class CheckView(View):
    template_name = 'wordgame/check.html'

    def get(self, request):
        word_number = get_current_word_number()
        current_word = ChristmasWord.objects.get(sequence_number=word_number)
        word_list = PlayerWord.objects.filter(user=request.user, start_word=current_word)
        context = {'memory': utilities.get_random_memory(), 'current_word': current_word, 'word_list': word_list}
        return render(request, self.template_name, context)


class VerifyView(View):
    template_name = 'wordgame/verify.html'

    def get(self, request):
        rejected_words = PlayerWord.objects.exclude(explanation='').order_by('word').distinct('word')
        context = {'memory': utilities.get_random_memory(), 'rejected': rejected_words}
        return render(request, self.template_name, context)

    def post(self, request, ):
        if request.POST['button'] == 'ok':
            if 'accept' in request.POST:
                accepted_words = list(request.POST.getlist('accept'))
                add_dict_words(accepted_words)
            if 'reject' in request.POST:
                rejected_words = list(request.POST.getlist('reject'))
                reject_words(rejected_words)
            word_number = get_current_word_number()
            UserModel = get_user_model()
            users = UserModel.objects.all()
            update_game(word_number, users, all=True)
            clean_words()
        return redirect('wordgame:scoreboard')


class EditCommentView(View):
    template_name = 'wordgame/edit_comment.html'

    def get(self, request, comment_id):
        # find out if the game is over
        word_number = get_current_word_number()
        try:
            current_word = ChristmasWord.objects.get(sequence_number=word_number)
        except:
            current_word = None
        if current_word:
            comment = WordComment.objects.get(id=comment_id)
        else:
            comment = GameComment.objects.get(id=comment_id)
        context = {'memory': utilities.get_random_memory(), 'comment': comment}
        return render(request, self.template_name, context)

    def post(self, request, comment_id):
        # find out if the game is over
        word_number = get_current_word_number()
        try:
            current_word = ChristmasWord.objects.get(sequence_number=word_number)
        except:
            current_word = None
        if current_word:
            comment = WordComment.objects.get(id=comment_id)
        else:
            comment = GameComment.objects.get(id=comment_id)
        button_clicked = request.POST['button']
        if button_clicked == 'save':
            if request.user == comment.player:
                new_version = request.POST['comment_text']
                comment.comment = new_version
                comment.save()
                return redirect('wordgame:entry')
            else:
                raise PermissionDenied
        if button_clicked =='cancel':
            return redirect('wordgame:entry')
        if button_clicked == 'delete':
            return redirect('wordgame:delete_comment', comment_id=str(comment_id))


class DeleteCommentView(View):
    template_name = 'wordgame/delete_comment.html'

    def get(self, request, comment_id):
        # find out if the game is over
        word_number = get_current_word_number()
        try:
            current_word = ChristmasWord.objects.get(sequence_number=word_number)
        except:
            current_word = None
        if current_word:
            comment = WordComment.objects.get(pk=comment_id)
        else:
            comment = GameComment.objects.get(pk=comment_id)
        context = {'memory': utilities.get_random_memory(), 'comment': comment}
        return render(request, self.template_name, context)

    def post(self, request, comment_id):
        # find out if the game is over
        word_number = get_current_word_number()
        try:
            current_word = ChristmasWord.objects.get(sequence_number=word_number)
        except:
            current_word = None
        if current_word:
            comment = WordComment.objects.get(pk=comment_id)
        else:
            comment = GameComment.objects.get(pk=comment_id)
        if request.POST['button'] == 'delete':
            if request.user == comment.player:
                comment.delete()
        return redirect('wordgame:entry')
