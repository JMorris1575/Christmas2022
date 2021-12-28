from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import PermissionDenied


import utilities

from .models import ConcentrationPlayer, ConcentrationComment
from user.models import get_adjusted_name

class PortalView(View):
    template = 'concentration/portal.html'

    def get(self, request):
        context = {'memory': utilities.get_random_memory()}
        return render(request, self.template, context)


# class Info_View(View):
#
#     def get(self, request):
#         print('request = ', request)
# #        return render("James Alfred Thomas Morris")
#         return redirect("localhost:9000/concentration.html")

class GameView(View):
    template = 'concentration/game.html'

    def post(self, request):
        # First make sure there's a record for this user:
        try:
            player = ConcentrationPlayer.objects.get(user=request.user)
        except:
            player = ConcentrationPlayer(user=request.user, level=1)
            player.save()
        url = "https://concentration.jatmorris.org?forceFullscreen=true"
        url += "&name=" + get_adjusted_name(player.user)
        url += "&level=" + str(player.level)
        context = {'memory': utilities.get_random_memory(), 'url': url}
        return render(request, self.template, context)


class ScoreView(View):
    template = 'concentration/scores.html'

    def get(self, request):
        player = ConcentrationPlayer.objects.get(user=request.user)
        comments = ConcentrationComment.objects.all()
        msg = "Games Played: " + str(player.level) + " -- "
        if request.GET.get('from', '') == 'godot':
            player.level += 1
            player.save()
        if player.level < 4:
            msg += "Next time you will play puzzle " + str(player.level)
        else:
            msg += "Next time you will play a random puzzle."
        context = {'memory': utilities.get_random_memory(), 'msg': msg, 'comments': comments}
        return render(request, self.template, context)

    def post(self, request):
        if request.POST['button'] == 'comment':             # post a comment
            comment = request.POST['comment'].strip()
            new_comment = ConcentrationComment(user=request.user, comment=comment)
            new_comment.save()
            return redirect('concentration:scores')


class EditCommentView(View):
    template_name = 'concentration/edit_comment.html'

    def get(self, request, comment_id):
        comment = ConcentrationComment.objects.get(id=comment_id)
        context = {'memory': utilities.get_random_memory(), 'comment': comment}
        return render(request, self.template_name, context)

    def post(self, request, comment_id):
        comment = ConcentrationComment.objects.get(id=comment_id)
        button_clicked = request.POST['button']
        if button_clicked == 'save':
            if request.user == comment.user:
                new_version = request.POST['comment_text']
                comment.comment = new_version
                comment.save()
                return redirect('concentration:scores')
            else:
                raise PermissionDenied
        if button_clicked =='cancel':
            return redirect('concentration:scores')
        if button_clicked == 'delete':
            return redirect('concentration:delete_comment', comment_id=str(comment_id))


class DeleteCommentView(View):
    template_name = 'concentration/delete_comment.html'

    def get(self, request, comment_id):
        comment = ConcentrationComment.objects.get(pk=comment_id)
        context = {'memory': utilities.get_random_memory(), 'comment': comment}
        return render(request, self.template_name, context)

    def post(self, request, comment_id):
       comment = ConcentrationComment.objects.get(pk=comment_id)
       if request.POST['button'] == 'delete':
            if request.user == comment.user:
                comment.delete()
       return redirect('concentration:scores')
