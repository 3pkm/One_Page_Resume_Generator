# Generated by Django 5.0.2 on 2024-12-13 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='objective',
            field=models.TextField(),
        ),
    ]
