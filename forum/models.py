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
    ImageField,
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
def community_directory_path (instance, filename: str) -> str:
    return f"community/{ instance.slug }/{ filename }"

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
    image       : ImageField    = ImageField (
                                    upload_to = community_directory_path,
                                    blank = True,
                                    null = True
                                  )
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
        Group.objects.get (name = f"{ self.slug }: members").delete ()
        Group.objects.get (name = f"{ self.slug }: moderators").delete ()

        return super ().delete (using, keep_parents)

    # Override
    def get_absolute_url (self) -> str:
        return reverse ("community-detail", kwargs = { "slug": self.slug })

    # Override
    def save (self, *args: list, **kwargs: dict):
        self.slug = slugify (self.name)
        try:
            with transaction.atomic ():
                member_group = Group.objects.create (name = f"{ self.slug }: members")
                moderator_group = Group.objects.create (name = f"{ self.slug }: moderators")

                member_group.user_set.add (self.created_by)
                moderator_group.user_set.add (self.created_by)
        except IntegrityError:
            # Description and/or Private is/are the only things changing, so new groups are not
            # needed
            pass

        super ().save (*args, **kwargs)

    def is_user_member (self, user: User) -> bool:
        """
        If the user is part of the <community slug: members> group, then they are a member of this
        community.

        user -- The user to check if they are a member of this community's member group
        """
        return self.get_member_group ().user_set.filter (username = user.username).exists ()

    def is_user_moderator (self, user: User) -> bool:
        """
        If the user is part of the <community slug: moderators> group, then they are a member of
        this community.

        user -- The user to check if they are a member of this community's moderator group
        """
        return self.get_moderator_group ().user_set.filter (username = user.username).exists ()

    def get_member_count (self) -> int:
        """Returns the current count of members for this Community."""
        return len (self.get_member_group ().user_set.all ())

    def get_member_group (self) -> Group:
        return Group.objects.get (name = f"{ self.slug }: members")

    def get_moderator_group (self) -> Group:
        return Group.objects.get (name = f"{ self.slug }: moderators")
# End Community Model
