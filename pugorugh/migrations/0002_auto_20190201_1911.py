# Generated by Django 2.1.5 on 2019-02-01 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='breed',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
