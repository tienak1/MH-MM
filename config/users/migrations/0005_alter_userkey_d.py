# Generated by Django 3.2.3 on 2022-01-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220114_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userkey',
            name='D',
            field=models.TextField(null=True),
        ),
    ]
