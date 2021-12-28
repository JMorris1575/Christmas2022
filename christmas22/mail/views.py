from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.mail import send_mail
from django.contrib.auth.models import User
from user.models import get_adjusted_name

from .models import Minor

from config.settings.base import get_secret


def convert_tags(subject, message, user):
    """
    Converts the following tags in the message or subject line of an e-mail to their equivalent for the given user:
    [first] = first name
    [last] = last name
    [full] = full name
    [user] = username
    [pwrd] = password
    :param subject: string containing the subject line to be sent
    :param message: string containing the message to be sent
    :param user: User object containing data for the given user
    :return: a subject string and message string with all the tags filled in
    """
    user_info = {'[first]':user.first_name,
                 '[last]': user.last_name,
                 '[full]': user.get_full_name(),
                 '[user]': user.username,
                 '[pwd]': get_secret(user.username.upper())}
    for tag in user_info.keys():
        subject = subject.replace(tag, user_info[tag])
        message = message.replace(tag, user_info[tag])

    return subject, message


class SendMail(View):
    template_name = 'mail/send-mail.html'

    def get(self, request):
        users = User.objects.all().order_by('first_name')
        context = {'users': users}
        return render(request, self.template_name, context)

    def post(self, request):
        if request.POST['button'] == 'send':
            recipients = list(set(request.POST.getlist('recipients')))
            subject_template = request.POST['subject']
            message_template = request.POST['message']
            for recipient in recipients:
                member = User.objects.get(username=recipient)
                subject, message = convert_tags(subject_template, message_template, member)
                if not Minor.objects.filter(minor=member).exists():  # check to see if member is a minor
                    send_mail(subject, message,
                          'jmorris@ecybermind.net',
                          [member.email], fail_silently=False)
                else:                                               # if member is a minor send emails to both parents
                    minor = Minor.objects.get(minor=member)
                    mail_list = [member.email]
                    if minor.father.email != member.email:
                        mail_list.append(minor.father.email)
                    if minor.mother.email != member.email:
                        mail_list.append(minor.mother.email)
                    send_mail(subject, message,
                              'jmorris@ecybermind.net',
                              mail_list, fail_silently=False)

        return redirect('landing')