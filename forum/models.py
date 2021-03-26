from django.db.models import (
    BooleanField,
    CharField,
    Model,
    SlugField,
    TextField
)
from django.template.defaultfilters import slugify

# Community Model
class Community (Model):
    class Meta:
        verbose_name_plural: str = "communities"

    name        : CharField     = CharField (max_length = 64, primary_key = True)
    description : TextField     = TextField ()
    private     : BooleanField  = BooleanField (default = False)
    slug        : SlugField     = SlugField (editable = False)

    def __str__ (self) -> str:
        return f"{ self.name }: /communities/{ self.slug }"

    # Override
    def save (self, *args: list, **kwargs: dict):
        # TODO: Create member group and moderator group
        self.slug = slugify (self.name)
        super ().save (*args, **kwargs)
# End Community Model
