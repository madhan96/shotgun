from django.contrib.auth.forms import AuthenticationForm

from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-text-box",
                "placeholder": "Username",
                "onkeypress": "resetField(this)",
                "autocomplete": "off",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-text-box",
                "placeholder": "Password",
                "onkeypress": "resetField(this)",
                "autocomplete": "off",
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        print("cleaned here", cleaned_data)
        print(
            "user",
            super().get_user().username,
            "auth",
            super().get_user().is_authenticated,
        )


class CustomUserCreationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    roles = (
        ("ARTIST", "artist"),
        ("PRODUCTION", "production"),
        ("TEAMLEAD", "team-lead"),
        ("IT", "It-support"),
    )
    usercriteria = forms.ChoiceField(choices=roles)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"], code="password_mismatch",
            )
        return password2
