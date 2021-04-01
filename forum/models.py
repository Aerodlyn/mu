from django.contrib.auth.models import (
    Group,
    User
)
from django.db import (
    DEFAULT_DB_ALIAS,
    transaction
)
from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    ForeignKey,
    Model,
    SlugField,
    TextField
)
from django.db.utils import IntegrityError
from django.template.defaultfilters import slugify
from django.urls import reverse

from typing import (
    Dict,
    Tuple
)

from .validators import ValidateAgainstBlacklist

# Community Model
class Community (Model):
    class Meta:
        verbose_name_plural: str = "communities"

    name        : CharField     = CharField (
                                    max_length = 64,
                                    primary_key = True,
                                    validators = [ ValidateAgainstBlacklist ([ "new" ]) ]
                                  )
    description : TextField     = TextField (blank = True, null = True)
    private     : BooleanField  = BooleanField (default = False)
    slug        : SlugField     = SlugField (editable = False)
    created_by  : ForeignKey    = ForeignKey (User, null = True, on_delete = SET_NULL)

    def __str__ (self) -> str:
        return f"{ self.name }: /communities/{ self.slug }"

    # Override
    def delete (
        self,
        using: str = DEFAULT_DB_ALIAS,
        keep_parents: bool = False
    ) -> Tuple [int, Dict [str, int]]:
        Group.objects.get (name = f"{ self.name }: members").delete ()
        Group.objects.get (name = f"{ self.name }: moderators").delete ()

        return super ().delete (using, keep_parents)

    # Override
    def get_absolute_url (self) -> str:
        return reverse ("community-detail", kwargs = { "slug": self.slug })

    # Override
    def save (self, *args: list, **kwargs: dict):
        try:
            with transaction.atomic ():
                member_group = Group.objects.create (name = f"{ self.name }: members")
                moderator_group = Group.objects.create (name = f"{ self.name }: moderators")

                member_group.user_set.add (self.created_by)
                moderator_group.user_set.add (self.created_by)
        except IntegrityError:
            pass

        self.slug = slugify (self.name)
        super ().save (*args, **kwargs)

    def get_member_count (self) -> int:
        """Returns the current count of members for this Community."""
        return len (Group.objects.get (name = f"{ self.name }: members").user_set.all ())
# End Community Model
