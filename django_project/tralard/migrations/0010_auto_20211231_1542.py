# Generated by Django 3.1.13 on 2021-12-31 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tralard', '0009_training_moderators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='completed',
            field=models.BooleanField(blank=True, default=False, help_text='Has this Training schedule been conducted andd completed?', null=True),
        ),
    ]