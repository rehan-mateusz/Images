from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms

from . import models


class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password')
    password2 = forms.CharField(label='Repeat Password')

    class Meta:
        model = models.Account
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["password1"]==self.cleaned_data["password2"]:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AccountChangeForm(forms.ModelForm):

    class Meta:
        model = models.Account
        fields = '__all__'

class AccountUserAdmin(UserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm
    list_display = ('email', 'username', 'password', 'plan')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Plan', {'fields': ('plan',)}),
        ('Permissions', {'fields': ('is_admin','is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
admin.site.register(models.Plan)
admin.site.register(models.Account, AccountUserAdmin)
