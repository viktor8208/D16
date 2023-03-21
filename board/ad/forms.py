

from django import forms


from .models import Ad, UserResponse


class AdForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = [
            'title',
            'text',
            'category',
        ]


class UserResponseForm(forms.ModelForm):

    class Meta:
        model = UserResponse
        fields = [
            'text',
        ]


class UserResponseUpdateForm(forms.ModelForm):

    class Meta:
        model = UserResponse
        fields = [
        ]

