# Generated by Django 3.2.3 on 2022-01-14 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220114_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userkey',
            name='D',
            field=models.BigIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='userkey',
            name='E',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userkey',
            name='N',
            field=models.BigIntegerField(blank=True),
        ),
    ]
