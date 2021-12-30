from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

from .models import TriviaQuestion, TriviaChoice, TriviaResponse
from user.models import get_adjusted_name

from operator import itemgetter

import utilities

import os

def get_next_question(user):
    next_question = len(TriviaResponse.objects.filter(user=user)) + 1
    print('next_question = ', next_question)
    return next_question

class ScoreboardView(View):
    template_name = 'trivia/scoreboard.html'

    def get(self, request):
        stats, current_user_attempts = self.get_stats(request.user)
        context = {'memory':utilities.get_random_memory(), 'stats':stats, 'user_attempts':current_user_attempts}
        return render(request, self.template_name, context)

    def get_stats(self, current_user):
        users = User.objects.all()
        temp = []
        for user in users:
            user_responses = TriviaResponse.objects.filter(user=user)
            attempted_questions = len(user_responses)
            if user == current_user:
                current_user_attempts = attempted_questions
            correct = len(user_responses.filter(correct=True))
            if attempted_questions != 0:
                percent = '{:.1%}'.format(correct/attempted_questions)
            else:
                percent = '0.0%'
            name = get_adjusted_name(user)
            if attempted_questions > 0:
                temp.append( {'attempted_questions':attempted_questions, 'correct':correct, 'percent':percent, 'name':name} )
        temp_sorted = sorted(temp, key = itemgetter('attempted_questions', 'correct'), reverse=True)
        stats = []
        attempt_group = -1
        total = len(TriviaQuestion.objects.filter(publish=True))
        for stat in temp_sorted:
            if stat['attempted_questions'] == attempt_group:
                stats.append(dict(type='stat', value=stat))
            else:
                attempt_group = stat['attempted_questions']
                stats.append(dict(type='heading', value='Completing ' + str(attempt_group) + '/' + str(total)))
                stats.append(dict(type='stat', value=stat))
        return stats, current_user_attempts


class NextQuestionView(View):

    def get(self, request):
        return redirect('trivia:display_question', get_next_question(request.user))


class DisplayQuestionView(View):
    template_name = 'trivia/trivia_question.html'

    def get(self, request, question_number):
        try:                                                                # prevents going beyond end of questions
            question = TriviaQuestion.objects.get(number=question_number)
        except:
            question_number = get_next_question(request.user)
            return redirect('trivia:display_question', question_number=question_number) # goes to user's next question
        else:
            if int(question_number) > get_next_question(request.user):      # prevent going beyond user's next question
                question_number = get_next_question(request.user)
                return redirect('trivia:display_question', question_number=question_number)
            if int(question_number) < get_next_question(request.user):      # prevent answering a question twice
                response = TriviaResponse.objects.get(user=request.user, question=question).response
                return redirect('trivia:result', question_number=question.number, choice_id=response.id)
            if question.publish == False:
                return redirect('trivia:finished')                        # prevent displaying unpublished questions
            choices = question.triviachoice_set.all()
            context = {'memory':utilities.get_random_memory(), 'question':question, 'choices':choices}
            return render(request, self.template_name, context)

    def post(self, request, question_number):
        question = TriviaQuestion.objects.get(number=question_number)
        choices = question.triviachoice_set.all()
        if int(question_number) < get_next_question(request.user):
            user_response = TriviaResponse.objects.get(user=request.user, question=question)
            choice = user_response.response
            return redirect('trivia:result', question_number=question_number, choice_id=choice.id)
        try:
            choice_id = request.POST['choice']
        except KeyError:
            context = {'question': question, 'choices': choices, 'display_memory': utilities.get_random_memory(),
                       'error_message': 'You must choose one of the responses below.'}
            return render(request, self.template_name, context)
        else:
            choice = choices.get(id=choice_id)
            user_response = TriviaResponse(user=request.user, question=question, response=choice)
            user_response.correct = choice.correct
            user_response.save()
            question.attempted_count += 1
            if choice.correct:
                question.correct_count += 1
            question.save()
        return redirect('trivia:result', question_number=question_number, choice_id = choice.id)


class DisplayResultView(View):
    template_name = 'trivia/trivia_result.html'

    def get(self, request, question_number, choice_id):
        if int(question_number) >= get_next_question(request.user):  # prevents going beyond user's next question
            question_number = get_next_question(request.user)
            return redirect('trivia:display_question', question_number=question_number)
        question = TriviaQuestion.objects.get(number=question_number)
        user_choice = TriviaChoice.objects.get(id=choice_id)
        choices = question.triviachoice_set.all()
        correct_choice = question.triviachoice_set.get(correct=True)
        context = {'memory': utilities.get_random_memory(), 'question': question, 'choices': choices,
                   'user_choice': user_choice, 'correct_choice': correct_choice}
        return render(request, self.template_name, context)

def previous_question_view(request, question_number):
    previous = question_number - 1
    if previous < 1:
        previous = len(TriviaQuestion.objects.all())
    return redirect('trivia:display_question', previous)

def next_question_view(request, question_number):
    next = question_number + 1
    if next > len(TriviaQuestion.objects.all()):
        next = 1
    return redirect('trivia:display_question', next)

class FinishedView(View):
    template_name = 'trivia/finished.html'

    def get(self, request):
        context = {'memory': utilities.get_random_memory()}
        return render(request, self.template_name, context)


def save_trivia_view(request):
    questions = TriviaQuestion.objects.all()
    question_list = []
    answer_list = []
    question_number = 1
    for question in questions:
        question_list.append(str(question_number) + '. ' + str(question) + '\n')
        answer_list.append(str(question_number) + '. ' + str(question) + '\n')
        question_number += 1
        choices = question.triviachoice_set.all()
        choice_label = 'A'
        for choice in choices:
            question_list.append('\t' + choice_label + ') ' + str(choice) + '\n')
            if choice.correct:
                answer_list.append('\t' + choice_label + ') ' + str(choice).upper() + ' <--correct\n')
            else:
                answer_list.append('\t' + choice_label + ') ' + str(choice) + '\n')
            choice_label = chr(ord(choice_label) + 1)
        question_list.append('\n')
        if question.explanation:
            answer_list.append('Explanation: ' + str(question.explanation) + '\n')
        if question.link:
            answer_list.append('See: ' + str(question.link) + '\n')
        answer_list.append('\n')
    question_file = open(os.path.join(settings.BASE_DIR, 'Christmas_Trivia_Questions.txt', 'w'))
    question_file.writelines(question_list)
    question_file.close()
    answer_file = open(os.path.join(settings.BASE_DIR, 'Christmas_Trivia_Answers.txt', 'w'))
    answer_file.writelines(answer_list)
    answer_file.close()
    return redirect('trivia:scoreboard')