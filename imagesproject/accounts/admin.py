import json

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms

from . import models
from images import models as img_models
from images import images_utils

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
        fields = ('__all__')

    def save(self, commit=True):
        pre_update_account =  models.Account.objects.get(
            id=self.instance.id)
        if pre_update_account.plan != self.cleaned_data['plan']:
            images = img_models.Image.objects.filter(owner=pre_update_account)
            for image in images:
                thumbnails=image.thumbnail_set.all()
                for thumbnail in thumbnails:
                    thumbnail.delete()
                if self.cleaned_data['plan']:
                    sizes = json.loads(self.cleaned_data['plan'].thumbnails_sizes['sizes'])
                    images_utils.create_thumbnails(image, sizes)
        updated_account = super().save(commit=False)
        updated_account.save()
        return updated_account

class AccountUserAdmin(UserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm
    list_display = ('email', 'username', 'plan')

    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
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
