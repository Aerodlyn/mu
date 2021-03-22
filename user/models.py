from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    BooleanField,
    ImageField,
    Model,
    OneToOneField,
    TextField
)
from django.urls import reverse_lazy

# Profile Model
def user_directory_path(instance, filename: str) -> str:
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{ instance.user.username }/{ filename }"

class Profile (Model):
    private : BooleanField  = BooleanField (default = True)
    avatar  : ImageField    = ImageField (upload_to = user_directory_path, blank = True, null = True)
    user    : OneToOneField = OneToOneField (User, on_delete = CASCADE)
    bio     : TextField     = TextField (blank = True, null = True)

    def __str__ (self) -> str:
        return f"{ self.user.username }'s profile"

    # Override
    def get_absolute_url (self):
        return reverse_lazy ("profile-view", kwargs = { "username": self.user.username })
# End Profile Model
