from django.db.models import (
    BooleanField,
    CharField,
    Model,
    SlugField,
    TextField
)
from django.template.defaultfilters import slugify
from django.urls import reverse

from .validators import validate_against_blacklist

# Community Model
class Community (Model):
    class Meta:
        verbose_name_plural: str = "communities"

    name        : CharField     = CharField (max_length = 64, primary_key = True, validators = [ validate_against_blacklist ([ "new" ]) ])
    description : TextField     = TextField (blank = True, null = True)
    private     : BooleanField  = BooleanField (default = False)
    slug        : SlugField     = SlugField (editable = False)

    def __str__ (self) -> str:
        return f"{ self.name }: /communities/{ self.slug }"

    # Override
    def get_absolute_url (self) -> str:
        return reverse ("community-detail", kwargs = { "slug": self.slug })

    def save (self, *args: list, **kwargs: dict):
        # TODO: Create member group and moderator group
        self.slug = slugify (self.name)
        super ().save (*args, **kwargs)
# End Community Model
