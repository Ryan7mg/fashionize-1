from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import resolve
from .forms import OutfitForm
from .models import Outfit
from closet.models import Clothing
from django.urls import reverse
from .views import OutfitListView , OutfitCreateView

class OutfitModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # 创建测试用户和衣物
        test_user = User.objects.create_user(username='testuser', password='12345')
        test_top = Clothing.objects.create(owner=test_user, name="Test Top", type="top", photo="top_photo.jpg")
        # 可以继续为 bottom 和 shoe 添加更多测试数据

        # 创建测试Outfit
        Outfit.objects.create(owner=test_user, name="Test Outfit", top=test_top)  # 根据需要填写其他字段

    def test_outfit_creation(self):
        outfit = Outfit.objects.get(id=1)
        self.assertEqual(outfit.name, "Test Outfit")
        self.assertEqual(outfit.top.name, "Test Top")
        # 测试其他字段...

    def test_outfit_str(self):
        outfit = Outfit.objects.get(id=1)
        expected_object_name = outfit.name
        self.assertEqual(str(outfit), expected_object_name)




class OutfitListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='123456')
        self.client.login(username='testuser2', password='123456')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/outfits/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('outfits:my_outfits'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'outfits/my_outfits.html')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('outfits:my_outfits'))
        self.assertTrue(response.url.startswith('/accounts/login/'))



class OutfitFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser3', password='123456')

    def test_outfit_form_valid_data(self):
        form = OutfitForm(data={
            'name': "New Outfit",
            'top': 1,
            'bottom': 2,
            'shoe': 3,
        }, user=self.user)
        self.assertTrue(form.is_valid())

    def test_outfit_form_no_data(self):
        form = OutfitForm(data={}, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # name是必填字段




class OutfitURLsTest(TestCase):

    def test_outfit_list_url_resolves(self):
        view = resolve('/outfits/')
        self.assertEqual(view.func.view_class, OutfitListView)

    def test_outfit_create_url_resolves(self):
        view = resolve('/outfits/create/')
        self.assertEqual(view.func.view_class, OutfitCreateView)
