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
    IntegerChoices,
    IntegerField,
    ManyToManyField,
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

    name        : CharField         = CharField (
                                        max_length = 64,
                                        primary_key = True,
                                        validators = [
                                            ValidateAgainstBlacklist ([
                                                "all",
                                                "new",
                                                "subscribed",
                                                "update"
                                            ])
                                        ]
                                      )
    description : TextField         = TextField (blank = True, null = True)
    private     : BooleanField      = BooleanField (default = False)
    image       : ImageField        = ImageField (
                                        upload_to = community_directory_path,
                                        blank = True,
                                        null = True
                                      )
    slug        : SlugField         = SlugField (editable = False)
    created_by  : ForeignKey        = ForeignKey (User, null = True, on_delete = SET_NULL)
    members     : ManyToManyField   = ManyToManyField (
                                        User,
                                        through = "Membership",
                                        related_name = "memberships"
                                      )

    def __str__ (self) -> str:
        return f"{ self.name }: /communities/{ self.slug }"

    # Override
    def get_absolute_url (self) -> str:
        return reverse ("forum:community-detail", kwargs = { "slug": self.slug })

    # Override
    def save (self, *args: list, **kwargs: dict):
        self.slug = slugify (self.name)
        super ().save (*args, **kwargs)

        try:
            self.add_user (self.created_by, True)
        except IntegrityError:
            # Description and/or Private is/are the only things changing, so new groups are not
            # needed
            pass

    def is_user_member (self, user: User) -> bool:
        """
        If the user has a record in the Membership table for this Community, and it is either MEMBER
        or MODERATOR, then they are a member.

        user -- The user to check if they are a member of this Community
        """
        return user.is_authenticated and self.membership_set.filter (user = user).exclude (role = Membership.Role.REQUESTED).exists ()

    def is_user_moderator (self, user: User) -> bool:
        """
        If the user has a record in the Membership table for this Community and has the role of
        Moderator, then they are a moderator

        user -- The user to check if they are a moderator of this Community
        """
        return self.membership_set.filter (user = user, role = Membership.Role.MODERATOR).exists ()

    def get_member_count (self) -> int:
        """Returns the current count of members for this Community."""
        return self.members.count ()

    def add_user (self, user: User, as_moderator: bool = False) -> None:
        """
        Adds the given user to the Membership table as a member of this Community, optionally as a
        moderator if `as_moderator` is True.

        user -- The User to add as a member of this Community 
        as_moderator -- True to also add the user as a moderator, otherwise as a regular member
        """
        membership = Membership.objects.get_or_create (user = user, community = self) [0]
        if as_moderator:
            membership.role = Membership.Role.MODERATOR

        membership.save ()

    def remove_user (self, user: User) -> None:
        """
        Removes the given user from the Membership table for this Community.

        user -- The User to remove
        """
        self.members.remove (user)
# End Community Model

# Membership Model
class Membership (Model):
    class Role (IntegerChoices):
        MEMBER      = 0, "Member"
        MODERATOR   = 1, "Moderator"
        REQUESTED   = 2, "Requested"

    community   : ForeignKey    = ForeignKey (Community, on_delete = CASCADE)
    user        : ForeignKey    = ForeignKey (User, on_delete = CASCADE)

    role        : IntegerField  = IntegerField (choices = Role.choices, default = Role.MEMBER)

    def __str__ (self) -> str:
        return f"{ self.community } - { self.user }: { self.Role (self.role).label }"
    
# End Membership Model

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
                "id": self.id,
                "slug": self.slug
            }
        )

    # Override
    def save (self, *args: list, **kwargs: dict):
        self.slug = slugify (self.title)
        super ().save (*args, **kwargs)
# End Post Model
