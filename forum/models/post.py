from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    SlugField,
    TextField
)
from django.template.defaultfilters import slugify
from django.urls import reverse

from .community import Community

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
