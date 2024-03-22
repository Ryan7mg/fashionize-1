

from .models import UserProfile
from django.urls import reverse

from django.test import TestCase
from .forms import UserEditForm
from django.contrib.auth.models import User



class UserProfileTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        # Create a user profile for the user
        UserProfile.objects.create(user=self.user, bio='This is a bio.', phone='1234567890')

    def test_user_profile_creation(self):
        user_profile = UserProfile.objects.get(user__username='testuser')
        self.assertEqual(user_profile.bio, 'This is a bio.')
        self.assertEqual(user_profile.phone, '1234567890')

    def test_user_profile_str(self):
        user_profile = UserProfile.objects.get(user__username='testuser')
        self.assertEqual(str(user_profile), 'testuser')


class AccountViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_login_view_POST_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpassword'})
        self.assertContains(response, 'Invalid username or password', status_code=200)

    def test_login_view_POST_valid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, f'/{self.user.username}/dashboard/')

class UserEditFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_form_save(self):
        form_data = {'first_name': 'First', 'last_name': 'Last', 'email': 'newtest@example.com', 'bio': 'New bio', 'phone': '0987654321'}
        form = UserEditForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.first_name, 'First')
        self.assertEqual(updated_user.last_name, 'Last')
        self.assertEqual(updated_user.email, 'newtest@example.com')
        self.assertEqual(updated_user.userprofile.bio, 'New bio')
        self.assertEqual(updated_user.userprofile.phone, '0987654321')