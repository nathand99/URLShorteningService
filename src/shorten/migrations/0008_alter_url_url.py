# Generated by Django 4.0.2 on 2022-02-16 04:24

from django.db import migrations, models
import shorten.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shorten', '0007_rename_active_urls_url_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='url',
            field=models.CharField(max_length=220, validators=[shorten.validators.validate_url]),
        ),
    ]