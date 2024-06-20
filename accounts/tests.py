from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.forms import CustomUserCreationForm, UserProfileForm
from accounts.models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts import views

class CustomUserCreationFormTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password1': '123password123',
            'password2': '123password123',
            'email': 'testuser@example.com',
            'role': 'customer',
            'name': 'Test User',
            'description': 'This is a test user.',
        }
        self.photo_path = 'C:\\Users\evgen\OneDrive\Рабочий стол\img_forsage\car.jpg'
        with open(self.photo_path, 'rb') as image_file:
            self.photo_data = {
            'photo_user': SimpleUploadedFile(
                name='test_image.jpg',
                content=image_file.read(),
                content_type='image/jpeg'
            )
        }

    def test_form_valid(self):
        form = CustomUserCreationForm(data=self.user_data, files=self.photo_data)
        if not form.is_valid():
           print(f'Form error:{form.errors}')
        self.assertTrue(form.is_valid())

    def test_form_invalid_missing_email(self):
        self.user_data['email'] = ''
        form = CustomUserCreationForm(data=self.user_data, files=self.photo_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_invalid_password_mismatch(self):
        self.user_data['password2'] = 'differentpassword'
        form = CustomUserCreationForm(data=self.user_data, files=self.photo_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_save(self):
        form = CustomUserCreationForm(data=self.user_data, files=self.photo_data)
        if form.is_valid():
            user = form.save()
            self.assertEqual(user.username, 'testuser')
            self.assertEqual(user.email, 'testuser@example.com')
            self.assertTrue(user.check_password('123password123'))
            self.assertEqual(user.role, 'customer')
            self.assertEqual(user.name, 'Test User')
            self.assertEqual(user.description, 'This is a test user.')
            self.assertIsNotNone(user.photo_user)

class UserProfileFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='123password123'
        )
        self.form_data = {
            'name': 'Updated User',
            'description': 'This is an updated description.',
            'role': 'executor'
        }
        self.photo_data = {
            'photo_user': SimpleUploadedFile(
                name='new_test_image.jpg',
                content=b'\x00\x01',
                content_type='image/jpeg'
            )
        }

    def test_form_valid(self):
        form = UserProfileForm(data=self.form_data, files=self.photo_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form = UserProfileForm(data=self.form_data, files=self.photo_data, instance=self.user)
        if form.is_valid():
            user = form.save()
            self.assertEqual(user.name, 'Updated User')
            self.assertEqual(user.description, 'This is an updated description.')
            self.assertEqual(user.role, 'executor')
            self.assertIsNotNone(user.photo_user)

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'password1': '123password123',
            'password2': '123password123',
            'email': 'testuser@example.com',
            'role': 'customer',
            'name': 'Test User',
            'description': 'This is a test user.',
        }
        self.photo_path = 'C:\\Users\evgen\OneDrive\Рабочий стол\img_forsage\car.jpg'
        with open(self.photo_path, 'rb') as image_file:
            self.photo_data = {
                'photo_user': SimpleUploadedFile(
                    name='test_image.jpg',
                    content=image_file.read(),
                    content_type='image/jpeg'
                )
            }
            # Создаем пользователя через CustomUserCreationForm
            form_data = self.user_data.copy()
            form_data.update(self.photo_data)
            form = CustomUserCreationForm(data=form_data)
            if form.is_valid():
                self.user = form.save()
            else:
                raise ValueError("Form data is not valid. Check the setup data.")
    def test_main_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertIn('executors_count',response.context)
        self.assertIn('tasks_count',response.context)

    def test_logoutuser(self):
        self.client.login(username='testuser', password='123password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('home'))

    def test_profile_view_get(self):
        self.client.login(username='testuser', password='123password123')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['profile_form'], UserProfileForm)

    def test_profile_view_post_valid(self):
        self.client.login(username='testuser', password='123password123')
        response = self.client.post(reverse('profile'), {
            'name': 'Updated Name',
            'description': 'Updated Description',
            'role': 'customer',
            'photo_user': self.photo_data['photo_user']
        })
        self.assertEqual(response.status_code, 200)
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.name, 'Updated Name')
        self.assertEqual(user.description, 'Updated Description')

    def test_registration_view_get(self):
        response = self.client.post(reverse('register'))
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.context['registration_form'], CustomUserCreationForm)
        self.assertIsInstance(response.context['profile_form'], UserProfileForm)

    def test_registration_view_post_valid(self):
        with open(self.photo_path, 'rb') as img:
            response = self.client.post(reverse('register'),{
                'username': 'newuser',
                'password1': 'ComplexPassword123!',
                'password2': 'ComplexPassword123!',
                'email': 'newuser@example.com',
                'role': 'executor',
                'name': 'New User',
                'description': 'New Description',
                'photo_user': img,
                'register': True
            })
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('profile'))
            user = CustomUser.objects.get(username='newuser')
            self.assertIsNotNone(user)
            self.assertTrue(user.check_password('ComplexPassword123!'))
            self.assertEqual(user.email, 'newuser@example.com')
            self.assertEqual(user.role, 'executor')
            self.assertEqual(user.name, 'New User')
            self.assertEqual(user.description, 'New Description')

    def test_registration_view_post_invalid(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'ComplexPassword123!',
            'password2': 'WrongPassword',
            'email': 'newuser@example.com',
            'role': 'executor',
            'name': 'New User',
            'description': 'New Description',
            'register': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['registration_form'].is_valid())
        self.assertIn('password2', response.context['registration_form'].errors)