from django.shortcuts import render
from django.views import View

import utilities

class LandingView(View):
    template = 'landing.html'

    def get(self, request):
        context = {'memory': utilities.get_random_memory()}
        return render(request, self.template, context)


class WaitingView(View):
    template = 'waiting.html'

    def get(self, request):
        context = {'memory': utilities.get_random_memory()}
        return render(request, self.template, context)
