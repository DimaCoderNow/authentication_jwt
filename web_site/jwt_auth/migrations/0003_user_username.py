# Generated by Django 5.0.4 on 2024-04-28 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0002_refreshtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=50, unique=True),
        ),
    ]
