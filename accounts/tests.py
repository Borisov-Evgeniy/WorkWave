from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.forms import CustomUserCreationForm, UserProfileForm
from accounts.models import CustomUser

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
