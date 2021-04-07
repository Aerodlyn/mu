from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.test import (
    RequestFactory,
    TestCase
)
from django.urls import reverse

from .forms import (
    MuAuthenticationForm,
    MuUserCreationForm,
    ProfileUpdateForm,
    UserUpdateForm
)
from .models import (
    Profile,
    user_directory_path
)
from .views import (
    ProfileDetailView,
    ProfileUpdateView
)

# Form Tests
class MuAuthenicationFormTestCase (TestCase):
    def setUp (self):
        self.form = MuAuthenticationForm ()

    def test_helper (self):
        self.assertFalse (self.form.helper.form_tag)

class MuUserCreationFormTestCase (TestCase):
    def setUp (self):
        self.form = MuUserCreationForm ()

    def test_helper (self):
        self.assertFalse (self.form.helper.form_tag)

    def test_save (self):
        self.form.cleaned_data = {
            "password1": "testpw123",
            "password2": "testpw123"
        }
        
        user = self.form.save ()
        self.assertEqual (Profile.objects.get (user = user).user, user)

class ProfileUpdateFormTestCase (TestCase):
    def setUp (self):
        self.form = ProfileUpdateForm ()

    def test_helper (self):
        self.assertFalse (self.form.helper.form_tag)

class UserUpdateFormTestCase (TestCase):
    def setUp (self):
        self.form = UserUpdateForm ()

    def test_helper (self):
        self.assertFalse (self.form.helper.form_tag)

# Model Tests
class ProfileTestCase (TestCase):
    def setUp (self):
        self.user = User.objects.create (username = "test_user", password = "testpw123")
        self.profile = Profile.objects.create (user = self.user)

    def test_profile_creation (self):
        self.assertEqual (str (self.profile), "test_user's profile")
        self.assertEqual (self.profile.user, self.user)

    def test_get_absolute_url (self):
        self.assertEqual ("/users/test_user", self.profile.get_absolute_url ())

    def test_user_directory_path (self):
        self.assertEqual (
            user_directory_path (self.profile, "test.png"),
            "user/test_user/test.png"
        )

# View Tests
class ProfileDetailViewTestCase (TestCase):
    def setUp (self):
        self.user = User.objects.create (username = "test_user", password = "testpw123")
        self.profile = Profile.objects.create (user = self.user)

        kwargs = { "username": self.user.username }
        url = reverse ("user:profile-detail", kwargs = kwargs)

        request = RequestFactory ().get (url)

        self.view = ProfileDetailView ()
        self.view.setup (request, **kwargs)

    def test_get_object_no_queryset (self):
        self.assertEqual (self.view.get_object ().user.username, self.user.username)

    def test_get_object_queryset (self):
        self.assertEqual (
            self.view.get_object (Profile.objects.all ()).user.username,
            self.user.username
        )

class ProfileUpdateViewTestCase (TestCase):
    def setUp (self):
        self.user = User.objects.create (username = "test_user", password = "testpw123")
        self.profile = Profile.objects.create (user = self.user)

        self.kwargs = { "username": self.user.username }
        url = reverse ("user:profile-update", kwargs = self.kwargs)

        self.request = RequestFactory ().get (url)
        self.request.user = self.user

        self.view = ProfileUpdateView ()
        self.view.setup (self.request, **self.kwargs)

    def test_get_success_url (self):
        self.assertEqual (
            self.view.get_success_url (),
            reverse ("user:profile-detail", kwargs = self.kwargs)
        )

    def test_get_same_user (self):
        self.assertNotIsInstance (
            self.view.get (self.request, **self.kwargs),
            HttpResponseRedirect
        )

    def test_get_different_user (self):
        self.assertIsInstance (
            self.view.get (self.request, **{ "username": "different_user" }),
            HttpResponseRedirect
        )
