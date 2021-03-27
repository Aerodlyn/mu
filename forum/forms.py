from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    ButtonHolder,
    Field,
    Layout,
    Submit
)

from django.forms import ModelForm

from .models import Community

class CommunityCreateForm (ModelForm):
    class Meta:
        fields  : list      = [ "name", "description", "private" ]
        model   : Community = Community

    @property
    def helper (self) -> FormHelper:
        helper = FormHelper ()

        helper.form_class = "container needs-validation"
        helper.label_class = "col-sm-2 col-form-label"
        helper.field_class = "col-sm"

        helper.layout = Layout (
            Field ("name", wrapper_class = "row mb-3"),
            Field ("description", wrapper_class = "row mb-3"),
            Field ("private", wrapper_class = "d-flex flex-row-reverse justify-content-between mb-3"),
            ButtonHolder (
                Submit ("create", "Create"),
                css_class = "row mb-3"
            )
        )

        return helper
