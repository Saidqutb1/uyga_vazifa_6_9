from django import forms
from .models import Users


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'image']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'email', 'first_name', 'last_name', 'image']