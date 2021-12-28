from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import PermissionDenied

from .models import Memory
from user.models import get_adjusted_name

from operator import itemgetter

import utilities


class MemoryListView(View):
    template_name = 'memory/memory_list.html'

    def sorter(self, e):
        return get_adjusted_name(e['user'])

    def get(self, request):
        memories = Memory.objects.all()
        collection = []
        for user in User.objects.all():
            user_memories = memories.filter(user=user)
            if user_memories:
                name = get_adjusted_name(user)
                collection.append({'user': user, 'name':name, 'memories':user_memories})
            collection.sort(key=self.sorter)
        context = {'memory':utilities.get_random_memory(), 'collection':collection}
        return render(request, self.template_name, context)


class MemoryEditView(View):
    template_name = 'memory/memory_edit.html'

    def get(self, request, memory_id=None):
        if memory_id:
            current_memory = Memory.objects.get(pk=memory_id)
        else:
            current_memory = None
        context = {'memory':utilities.get_random_memory(), 'current_memory':current_memory}
        return render(request, self.template_name, context)

    def post(self, request, memory_id=None):
        if request.POST['button'] == 'cancel':
            return redirect('memory:memory_list')
        elif request.POST['button'] == 'delete':
            return redirect('memory:delete', memory_id=memory_id)
        memory_text = request.POST['memory_text']
        if memory_id:
            memory_to_edit = Memory.objects.get(id=memory_id)
        if memory_text:             # there is text in the memory box to be saved
            if memory_id:           # this is an edit of a previous entry
                memory_to_edit.memory = memory_text
                memory_to_edit.save()
            else:                   # this memory is newly entered
                user = request.user
                new_memory = Memory(memory=memory_text, user=user)
                new_memory.save()
            return redirect('memory:memory_list')
        else:
            context = {'memory':utilities.get_random_memory(),
                       'error_message': 'Some text must be present in the box below or "Save" will not work.'}
            if memory_id:
                context['current_memory'] = memory_to_edit
            return render(request, self.template_name, context)


class MemoryDeleteView(View):
    template_name = 'memory/memory_delete.html'

    def get(self, request, memory_id):
        memory_to_delete = Memory.objects.get(id=memory_id)
        if request.user == memory_to_delete.user:
            context = {'memory':utilities.get_random_memory(), 'memory_to_delete': memory_to_delete}
            return render(request, self.template_name, context)
        else:
            raise PermissionDenied

    def post(self, request, memory_id):
        memory_to_delete = Memory.objects.get(id=memory_id)
        if request.user == memory_to_delete.user:
            if request.POST['button'] == 'yes':
                memory_to_delete.delete()
                return redirect('memory:memory_list')
            else:
                return redirect('memory:edit', memory_id)
        else:
            raise PermissionDenied

