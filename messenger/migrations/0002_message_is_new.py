# Generated by Django 4.2.6 on 2023-11-19 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
    ]