from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    DO_NOTHING,
    SET_NULL,
    ForeignKey,
    Model,
    TextField
)

from .community import Community

class Comment (Model):
    content     : TextField     = TextField ()
    made_in     : ForeignKey    = ForeignKey (Community, on_delete = CASCADE)
    created_by  : ForeignKey    = ForeignKey (User, null = True, on_delete = SET_NULL)
    parent      : ForeignKey    = ForeignKey (
                                    'self',
                                    null = True,
                                    default = None,
                                    on_delete = DO_NOTHING
                                  )
