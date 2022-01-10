# Generated by Django 3.2.3 on 2022-01-02 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photoapp', '0004_auto_20220103_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='submitter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='submitter', to=settings.AUTH_USER_MODEL),
        ),
    ]