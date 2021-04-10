from django.contrib.auth.models import (
    Group,
    User
)
from django.db import (
    DEFAULT_DB_ALIAS,
    transaction
)
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
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
        self.get_member_group ().delete ()
        self.get_moderator_group ().delete ()

        return super ().delete (using, keep_parents)

    # Override
    def get_absolute_url (self) -> str:
        return reverse ("forum:community-detail", kwargs = { "slug": self.slug })

    # Override
    def save (self, *args: list, **kwargs: dict):
        self.slug = slugify (self.name)
        try:
            with transaction.atomic ():
                self.add_user (self.created_by, True)
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
        return Group.objects.get_or_create (name = f"{ self.slug }: members") [0]

    def get_moderator_group (self) -> Group:
        return Group.objects.get_or_create (name = f"{ self.slug }: moderators") [0]

    def add_user (self, user: User, include_moderator: bool = False) -> None:
        """
        Adds the given user to the members group for this Community, and to the moderator group if
        `include_moderator` is True.

        user -- The User to add to the members  
        include_moderator -- True to also add the user to the moderators group, otherwise ignore
        """
        self.get_member_group ().user_set.add (user)
        if include_moderator:
            self.get_moderator_group ().user_set.add (user)

    def remove_user (self, user: User) -> None:
        """
        Removes the given user from both the members and moderators groups for this Community.

        user -- The User to remove from both membership groups
        """
        self.get_member_group ().user_set.remove (user)
        self.get_moderator_group ().user_set.remove (user)
# End Community Model

# Post Model
class Post (Model):
    title       : CharField     = CharField (max_length = 512)
    content     : TextField     = TextField ()
    slug        : SlugField     = SlugField (editable = False)
    created_at  : DateTimeField = DateTimeField (null = False, blank = False, auto_now_add = True)
    created_by  : ForeignKey    = ForeignKey (User, null = True, on_delete = SET_NULL)
    posted_in   : ForeignKey    = ForeignKey (Community, on_delete = CASCADE)

    def __str__ (self) -> str:
        return f"{ self.title }: { self.created_by } - { self.posted_in }"

    # Override
    def get_absolute_url (self) -> str:
        return reverse (
            "forum:post-detail",
            kwargs = {
                "community_slug": self.posted_in.slug,
                "post_id": self.id,
                "post_slug": self.slug
            }
        )

    # Override
    def save (self, *args: list, **kwargs: dict):
        self.slug = slugify (self.title)
        super ().save (*args, **kwargs)
# End Post Model
