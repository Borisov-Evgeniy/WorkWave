from django.test import TestCase, Client

class ViewTestsMessenger(TestCase):

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

