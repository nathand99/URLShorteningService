# Generated by Django 4.0.2 on 2022-02-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shorten', '0003_url_shortened'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='shortened',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
