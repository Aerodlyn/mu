from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.test import (
    RequestFactory,
    TestCase
)
from django.urls import reverse

from .forms import (
    CommunityCreateForm,
    CommunityUpdateForm
)
from .models import (
    Community,
    Post,
    Membership,
    community_directory_path
)
from .validators import ValidateAgainstBlacklist
from .views import (
    CommunityCreateView,
    CommunityDeleteView,
    CommunityDetailView,
    CommunityListView,
    CommunitySubscribedListView,
    CommunityUpdateView,
    update_user_community_membership
)

# Form Tests
class CommunityCreateFormTestCase (TestCase):
    def setUp (self):
        self.form = CommunityCreateForm ()

    def test_helper (self):
        self.assertTrue (self.form.helper.form_tag)

class CommunityUpdateFormTestCase (TestCase):
    def setUp (self):
        self.form = CommunityUpdateForm ()

    def test_helper (self):
        self.assertTrue (self.form.helper.form_tag)

# Model Tests
class CommunityTestCase (TestCase):
    def setUp (self):
        self.user = User.objects.create (username = "test_user", password = "testpw123")
        self.community = Community.objects.create (name = "Test Community", created_by = self.user)

    def test_add_user (self):
        new_user = User.objects.create (username = "new_user", password = "testpw123")
        self.community.add_user (new_user, False)

        self.assertEqual (self.community.get_member_count (), 2)
        self.assertTrue (self.community.is_user_member (new_user))
        self.assertFalse (self.community.is_user_moderator (new_user))

    def test_delete (self):
        self.community.delete ()
        self.assertFalse (Community.objects.filter (name = self.community.name).exists ())

    def test_get_absolute_url (self):
        self.assertEqual (self.community.get_absolute_url (), "/communities/test-community")

    def test_get_member_count (self):
        self.assertEqual (self.community.get_member_count (), 1)

    def test_is_user_member_moderator (self):
        self.assertTrue (self.community.is_user_member (self.user))
    
    def test_is_user_member_not_member (self):
        self.assertFalse (
            self.community.is_user_member (
                User.objects.create (username = "new_user", password = "testpw123")
            )
        )

    def test_is_user_member_requested (self):
        requested_user = User.objects.create (username = "new_user", password = "testpw123")
        Membership.objects.create (
            user = requested_user,
            role = Membership.Role.REQUESTED,
            community = self.community
        )

        self.assertFalse (self.community.is_user_member (requested_user))

    def test_is_user_moderator (self):
        self.assertTrue (self.community.is_user_moderator (self.user))
        self.assertFalse (
            self.community.is_user_moderator (
                User.objects.create (username = "new_user", password = "testpw123")
            )
        )

    def test_remove_user (self):
        self.community.remove_user (self.user)

        self.assertEqual (self.community.get_member_count (), 0)
        self.assertFalse(self.community.is_user_member (self.user))
        self.assertFalse (self.community.is_user_moderator (self.user))
    
    def test_save (self):
        self.assertEqual (self.community.slug, "test-community")

        self.community.description = "test"
        self.community.save ()

        self.assertEqual (Community.objects.count (), 1)

class PostTestCase (TestCase):
    def setUp (self):
        self.user = User.objects.create (username = "test_user", password = "testpw123")
        self.community = Community.objects.create (name = "Test Community", created_by = self.user)
        self.post = Post.objects.create (
            title = "Test Post",
            content = "testing",
            created_by = self.user,
            posted_in = self.community
        )
    
    def test_get_absolute_url (self):
        self.assertEqual (
            self.post.get_absolute_url (),
            "/communities/test-community/posts/1/test-post"
        )

# Validator Tests
class ValidateAgainstBlacklistTestCase (TestCase):
    def setUp (self):
        self.validator = ValidateAgainstBlacklist ([ "hello", "world" ])

    def test__call__ (self):
        self.assertIsNone (self.validator ("test"))
        self.assertRaises (ValidationError, self.validator, "world")

# View Tests
class CommunityCreateViewTestCase (TestCase):
    def setUp (self):
        self.user = User.objects.create (username = "test_user", password = "testpw123")
        
        url = reverse ("forum:community-create", kwargs = {})
        
        request = RequestFactory ().get (url)
        request.user = self.user

        self.view = CommunityCreateView ()
        self.view.setup (request, **{})

        self.form = CommunityCreateForm ({ "name": "Test Community" })

    def test_form_valid (self):
        self.view.form_valid (self.form)
        self.assertEqual (self.form.instance.created_by, self.user)

class CommunityDeleteViewTestCase (TestCase):
    def setUp (self):
        self.user = User.objects.create (username = "test_user", password = "testpw123")
        self.community = Community.objects.create (name = "Test Community", created_by = self.user)
        
        self.kwargs = { "slug": self.community.slug }
        url = reverse ("forum:community-delete", kwargs = self.kwargs)
        
        request = RequestFactory ().get (url)
        request.user = self.user

        self.view = CommunityDeleteView ()
        self.view.setup (request, **self.kwargs)

    def test_has_permission (self):
        self.assertTrue (self.view.has_permission ())

class CommunityDetailViewTestCase (TestCase):
    def setUp (self):
        self.user = User.objects.create (username = "test_user", password = "testpw123")
        self.community = Community.objects.create (name = "Test Community", created_by = self.user)
        
        self.kwargs = { "slug": self.community.slug }
        url = reverse ("forum:community-detail", kwargs = self.kwargs)
        
        request = RequestFactory ().get (url)
        request.user = self.user

        self.view = CommunityDetailView ()
        self.view.setup (request, **self.kwargs)

    def test_has_permission (self):
        self.assertTrue (self.view.has_permission ())

    def test_is_request_user_member (self):
        self.assertTrue (self.view.is_request_user_member ())

    def test_is_request_user_moderator (self):
        self.assertTrue (self.view.is_request_user_moderator ())

class CommunitySubscribedListViewTestCase (TestCase):
    def test_get_queryset_is_member (self):
        user = User.objects.create (username = "test_user", password = "testpw123")
        community = Community.objects.create (name = "Test Community", created_by = user)

        url = reverse ("forum:community-list-subscribed")
        
        request = RequestFactory ().get (url)
        request.user = user

        view = CommunitySubscribedListView ()
        view.setup (request)

        self.assertIn (community, view.get_queryset ())

    def test_get_queryset_is_not_member (self):
        user = User.objects.create (username = "test_user", password = "testpw123")
        community = Community.objects.create (name = "Test Community", created_by = user)

        url = reverse ("forum:community-list-subscribed")
        
        request = RequestFactory ().get (url)
        request.user = User.objects.create (username = "test_user_2", password = "testpw123")

        view = CommunitySubscribedListView ()
        view.setup (request)

        self.assertNotIn (community, view.get_queryset ())

class CommunityUpdateViewTestCase (TestCase):
    def setUp (self):
        self.user = User.objects.create (username = "test_user", password = "testpw123")
        self.community = Community.objects.create (name = "Test Community", created_by = self.user)
        
        kwargs = { "slug": self.community.slug }
        url = reverse ("forum:community-update", kwargs = kwargs)
        
        request = RequestFactory ().get (url)
        request.user = self.user

        self.view = CommunityUpdateView ()
        self.view.setup (request, **kwargs)

        self.form = CommunityUpdateForm ({ "description": "Test Community" })
        self.form.instance = self.community

    def test_form_valid (self):
        self.view.form_valid (self.form)
        self.assertEqual (self.form.instance.created_by, self.user)

class UpdateUserCommunityMembershipTestCase (TestCase):
    def setUp (self):
        self.user = User.objects.create (username = "test_user", password = "testpw123")
        self.community = Community.objects.create (name = "Test Community", created_by = self.user)

        self.kwargs = { "slug": self.community.slug }
        url = reverse ("forum:community-update-membership", kwargs = self.kwargs)
        
        self.request = RequestFactory ().post (url)
        self.request.user = self.user

    def test (self):
        response = update_user_community_membership (self.request, self.community.slug)

        self.assertIsInstance (response, HttpResponseRedirect)
        self.assertFalse (self.community.is_user_member (self.user))
        self.assertFalse (self.community.is_user_moderator (self.user))

        response = update_user_community_membership (self.request, self.community.slug)

        self.assertIsInstance (response, HttpResponseRedirect)
        self.assertTrue (self.community.is_user_member (self.user))
        self.assertFalse (self.community.is_user_moderator (self.user))
