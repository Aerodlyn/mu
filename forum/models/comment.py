from django.contrib.auth.models import User
from django.db import DEFAULT_DB_ALIAS
from django.db.models import (
    CASCADE,
    DO_NOTHING,
    SET_NULL,
    ForeignKey,
    TextField
)

from mptt.models import (
    MPTTModel,
    TreeForeignKey
)

from typing import (
    Dict,
    Tuple
)

from .post import Post

class Comment (MPTTModel):
    # ? Deletion behavior
    content     : TextField     = TextField ()
    made_on     : ForeignKey    = ForeignKey (Post, null = True, on_delete = SET_NULL)
    created_by  : ForeignKey    = ForeignKey (User, null = True, on_delete = SET_NULL)
    parent      : ForeignKey    = TreeForeignKey (
                                    'self',
                                    blank = True,
                                    null = True,
                                    default = None,
                                    on_delete = DO_NOTHING,
                                    related_name = "children"
                                  )

    def __str__ (self) -> str:
        return f"{ self.made_on } - { self.created_by }"
    
    # Override
    def delete (
        self,
        using: str = DEFAULT_DB_ALIAS,
        keep_parents: bool = False
    ) -> Tuple [int, Dict [str, int]]:
        self.created_by = None
        self.content = "[Deleted]"
        self.save ()

        return (1, { "forum.Comment": 1 })
