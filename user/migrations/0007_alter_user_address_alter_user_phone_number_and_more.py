# Generated by Django 5.1 on 2024-09-01 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13),
        ),
        migrations.AlterField(
            model_name='user',
            name='ssn',
            field=models.CharField(blank=True, max_length=55, unique=True),
        ),
    ]
