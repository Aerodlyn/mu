from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    BooleanField,
    ImageField,
    Model,
    OneToOneField,
    TextField
)

# Profile Model
class Profile (Model):
    private : BooleanField  = BooleanField (default = True)
    avatar  : ImageField    = ImageField (blank = True, null = True)
    user    : OneToOneField = OneToOneField (User, on_delete = CASCADE)
    bio     : TextField     = TextField (blank = True, null = True)

    def __str__ (self) -> str:
        return f"{ self.user.username }'s profile"
# End Profile Model
