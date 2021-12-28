from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import PermissionDenied

from .models import Object, Description, Contribution

import utilities


class ObjectListView(View):
    template_name = 'whatsit/object_list.html'

    def get(self, request):
        objects = Object.objects.filter(publish=True)
        context = {'memory':utilities.get_random_memory(), 'objects': objects}
        return render(request, self.template_name, context)


class SingleObjectView(View):

    def get(self, request, object_number):
        try:
            object = Object.objects.get(number=object_number)
        except:
            return redirect('whatsit:object_list')
        else:
            context = {'memory': utilities.get_random_memory(), 'object': object}
            if object.stage == object.ONE:
                self.template_name = 'whatsit/stage_one.html'
                description = Description.objects.filter(object=object, author=request.user)
                if len(description) == 1:
                    context['description'] = description[0]
            elif object.stage == object.TWO:
                self.template_name = 'whatsit/stage_two.html'
                descriptions = Description.objects.filter(object=object)
                context['descriptions'] = descriptions
                test = len(Contribution.objects.filter(object=object, user=request.user, type=Contribution.VOTE))
                print('Number of votes this user has made for this object: ', test)
                if len(Contribution.objects.filter(object=object, user=request.user, type=Contribution.VOTE)) != 0:
                    can_vote = False
                else:
                    can_vote = True
                print('Jim can vote = ', can_vote)
                context['can_vote'] = can_vote
            else:                                   # must be in stage THREE
                self.template_name = 'whatsit/stage_three.html'
                descriptions = Description.objects.filter(object=object)
                context['descriptions'] = descriptions
        return render(request, self.template_name, context)

    def post(self, request, object_number):
        try:
            object = Object.objects.get(number=object_number)
        except:
            return redirect('whatsit:object_list')
        else:
            if object.stage == object.ONE:
                self.template_name = 'whatsit/stage_one.html'
                if request.POST['button'] == 'cancel':
                    return redirect('whatsit:object_list')
                elif request.POST['button'] == 'delete':
                    return redirect('whatsit:description_delete', object_number=object_number)
                else:
                    try:
                        old_description = Description.objects.get(object=object, author=request.user)
                    except:
                        old_description = None
                    description_text = request.POST['description_text']
                    if description_text:                    # there is something here to save, else an error
                        if old_description:                 # user is editing a former description
                            old_description.description = description_text
                            old_description.save()
                        else:                               # this is a new description
                            new_description = Description(object=object, author=request.user,
                                                          description=description_text)
                            new_description.save()
                            contribution = Contribution(object=object, user=request.user, type=Contribution.DESCRIPTION)
                            contribution.save()
                    else:
                        context = {'memory': utilities.get_random_memory(), 'object': object, 'description': None,
                                   'error_message': 'Some text must appear in the box below or Save will not work.'}
                        if old_description:
                            context['description'] = old_description.description
                        return render(request, self.template_name, context)
                    return redirect('whatsit:object_list')
            elif object.stage == object.TWO:
                self.template_name = 'whatsit/stage_two.html'
                if request.POST['button'] == 'cancel':
                    return redirect('whatsit:object_list')
                try:
                    chosen_description = Description.objects.get(id=request.POST['vote'])
                except:                                         # they didn't cast a vote... just looking?
                    return redirect('whatsit:object_list')
                else:
                    descriptions = Description.objects.filter(object=object)
                    context = {'memory': utilities.get_random_memory(), 'object': object,
                               'descriptions': descriptions}
                    if chosen_description.author == request.user:       # they voted for their own entry
                        context['error_message'] = 'Sorry, you cannot vote for your own entry.'
                        context['can_vote'] = True
                        return render(request, self.template_name, context)
                    elif len(Contribution.objects.filter(object=object, user=request.user, type = Contribution.VOTE)) != 0:
                        context['error_message'] = 'Sorry, you already voted for one of these.'
                        return render(request, self.template_name, context)
                    else:
                        chosen_description.votes += 1
                        chosen_description.save()
                        contribution = Contribution(object=object, user=request.user, type=Contribution.VOTE)
                        contribution.save()
                        return redirect('whatsit:object_list')
            else:
                self.template_name = 'whatsit/stage_three.html'
                return redirect('whatsit:object_list')


class DescriptionDeleteView(View):
    template_name = 'whatsit/description_delete.html'

    def get(self, request, object_number):
        try:
            object = Object.objects.get(number=object_number)
        except:
            return redirect('whatsit:object_list')
        try:
            description_to_delete = Description.objects.get(object=object, author=request.user)
        except:
            return redirect('whatsit:object_list')
        if description_to_delete.author == request.user:
            context = {'memory':utilities.get_random_memory(), 'object_number': object_number,
                       'description_to_delete': description_to_delete}
            return render(request, self.template_name, context)
        else:
            raise PermissionDenied

    def post(self, request, object_number):
        try:
            object = Object.objects.get(number=object_number)
        except:
            return redirect('whatsit:object_list')
        try:
            description_to_delete = Description.objects.get(object=object, author=request.user)
        except:
            return redirect('whatsit:object_list')
        if request.user == description_to_delete.author:
            if request.POST['button'] == 'yes':
                description_to_delete.delete()
                contribution = Contribution.objects.get(object=object, user=request.user, type=Contribution.DESCRIPTION)
                contribution.delete()
                return redirect('whatsit:object_list')
            else:
                return redirect('whatsit:object_view', object.number)
        else:
            raise PermissionDenied





