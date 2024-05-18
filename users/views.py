from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .models import Users
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, ProfileUpdateForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.

class RegisterView(View):
    def get(self, request):
        create_form = UserForm()
        context = {
            'form': create_form
        }
        return render(request, 'register.html', context=context)

    def post(self, request):
        create_form = UserForm(request.POST, request.FILES)
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                'form': create_form
            }
            return render(request, 'register.html', context=context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            'form': login_form
        }
        return render(request, 'login.html', context=context)

    def post(self, request):
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home:home')
        context = {
            'form': login_form
        }
        return render(request, 'login.html', context=context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home:home')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')

    def post(self, request):
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('imail')

        if username and email:
            user.username = username
            user.email = email
            user.save()
            return redirect('profile')

        return render(request, 'profile.html', {'error': "Invalid input"})


class ProfileUpdateView(View):
    def get(self, request):
        update_form = ProfileUpdateForm(instance=request.user)
        context = {
            'form': update_form
        }
        return render(request, 'profile_edit.html', context=context)

    def post(self, request):
        update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('users:profile')
        context = {
            'form': update_form
        }
        return render(request, 'profile_edit.html', context=context)

























