# Generated by Django 5.1 on 2024-09-01 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_phone_number_user_ssn'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
