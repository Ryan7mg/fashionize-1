from django.test import TestCase
from django.contrib.auth.models import User

from .forms import ClothingForm
from .models import Clothing
from django.urls import reverse, resolve

from .views import ClosetListView, ClothingCreateView


class ClothingModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='12345')
        test_user.save()
        Clothing.objects.create(owner=test_user, name="T-Shirt", type="top", photo="path/to/photo.jpg")

    def test_clothing_content(self):
        clothing = Clothing.objects.get(id=1)
        expected_owner = f'{clothing.owner}'
        expected_name = f'{clothing.name}'
        expected_type = f'{clothing.type}'
        self.assertEqual(expected_owner, 'testuser')
        self.assertEqual(expected_name, 'T-Shirt')
        self.assertEqual(expected_type, 'top')

    def test_clothing_str(self):
        clothing = Clothing.objects.get(id=1)
        expected_object_name = f'{clothing.name}'
        self.assertEqual(str(clothing), expected_object_name)




class ClosetListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='123456')
        self.client.login(username='testuser2', password='123456')
        self.user2 = User.objects.create_user(username='testuser3', password='1234567')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/closet/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('closet:closet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'closet/closet_list.html')

    def test_lists_only_user_clothing(self):
        Clothing.objects.create(owner=self.user, name="T-Shirt", type="top", photo="path/to/photo.jpg")
        Clothing.objects.create(owner=self.user2, name="Sneakers", type="shoe", photo="path/to/photo2.jpg")
        response = self.client.get(reverse('closet:closet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('clothings' in response.context)
        self.assertEqual(len(response.context['clothings']), 1)



class ClothingFormTest(TestCase):

    def test_clothing_form_valid_data(self):
        form = ClothingForm(data={
            'name': "New T-Shirt",
            'type': "top",
            'photo': "path/to/photo3.jpg"
        })
        self.assertTrue(form.is_valid())

    def test_clothing_form_no_data(self):
        form = ClothingForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # 因为所有字段都是必填的


class ClosetURLsTest(TestCase):

    def test_closet_list_url(self):
        url = reverse('closet:closet_list')
        self.assertEqual(resolve(url).func.view_class, ClosetListView)

    def test_clothing_add_url(self):
        url = reverse('closet:clothing_add')
        self.assertEqual(resolve(url).func.view_class, ClothingCreateView)
