from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    ButtonHolder,
    Field,
    Layout,
    Submit
)

from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm
)
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Profile

class MuAuthenticationForm (AuthenticationForm):
    @property
    def helper (self) -> FormHelper:
        helper = FormHelper ()
        helper.form_tag = False

        helper.label_class = "col-sm-2 col-form-label"
        helper.field_class = "col-sm"

        helper.layout = Layout (
            Field ("username", wrapper_class = "row mb-3"),
            Field ("password", wrapper_class = "row mb-3"),
            ButtonHolder (
                Submit ("log-in", "Log in"),
                css_class = "row mb-3"
            )
        )

        return helper

class MuUserCreationForm (UserCreationForm):
    @property
    def helper (self) -> FormHelper:
        helper = FormHelper ()
        helper.form_tag = False

        helper.label_class = "col-sm-2 col-form-label"
        helper.field_class = "col-sm"

        helper.layout = Layout (
            Field ("username", wrapper_class = "row mb-3"),
            Field ("password1", wrapper_class = "row mb-3"),
            Field ("password2", wrapper_class = "row mb-3"),
            ButtonHolder (
                Submit ("sign-up", "Sign up"),
                css_class = "row mb-3"
            )
        )

        return helper

    # Override
    def save (self, commit = True) -> User:
        user = super ().save (commit)
        Profile (user = user).save (commit)

        return user

class ProfileUpdateForm (ModelForm):
    class Meta:
        fields  : list      = [ "avatar", "bio", "private" ]
        model   : Profile   = Profile

    @property
    def helper (self) -> FormHelper:
        helper = FormHelper ()
        helper.form_tag = False

        helper.label_class = "col-sm-2 col-form-label"
        helper.field_class = "col-sm"

        helper.layout = Layout (
            Field ("bio", wrapper_class = "row mb-3"),
            Field ("avatar", wrapper_class = "row mb-3"),
            Field ("private", wrapper_class = "d-flex flex-row-reverse justify-content-between mb-3"),
            ButtonHolder (
                Submit ("update-profile", "Update"),
                css_class = "row"
            )
        )

        return helper
