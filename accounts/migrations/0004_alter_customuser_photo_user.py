# Generated by Django 4.2.6 on 2023-11-05 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='photo_user',
            field=models.ImageField(upload_to='media/user_photos/'),
        ),
    ]
