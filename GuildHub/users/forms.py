from django import forms
from django.utils.translation import gettext_lazy as _
from users.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'avatar',
            'nickname',
            'first_name',
            'last_name',
            'gender',
            'date_birth',
            'user_timezone',
            'phone_number',
            'about_me',
            'discord_url_profile',
            'steam_url_profile',
            'telegram_nickname',
        )


class UserDeactivateForm(forms.Form):
    confirm_deactivation = forms.BooleanField(required=True, label=_('Confirm deactivation and delete'))
