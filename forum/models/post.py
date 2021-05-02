from django.contrib.auth.models import User
from django.db import DEFAULT_DB_ALIAS
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

from typing import (
    Dict,
    Tuple
)

from .community import Community

class Post (Model):
    title       : CharField     = CharField (max_length = 512)
    content     : TextField     = TextField ()
    slug        : SlugField     = SlugField (editable = False)
    created_at  : DateTimeField = DateTimeField (auto_now_add = True)
    created_by  : ForeignKey    = ForeignKey (User, null = True, on_delete = SET_NULL)
    posted_in   : ForeignKey    = ForeignKey (Community, null = True, on_delete = SET_NULL)

    def __str__ (self) -> str:
        return f"{ self.title }: { self.created_by } - { self.posted_in }"

    # Override
    def delete (
        self,
        using: str = DEFAULT_DB_ALIAS,
        keep_parents: bool = False
    ) -> Tuple [int, Dict [str, int]]:
        self.created_by = None
        self.content = "[Deleted]"
        self.posted_in = None
        self.save ()

        return (1, { "forum.Post": 1 })

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
