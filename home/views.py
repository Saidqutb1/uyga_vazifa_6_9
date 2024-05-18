from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

def home_page(request):
    return render(request, 'home.html')


class GetTestAuth(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'product:book_list')
        else:
            return redirect('')


