# Generated by Django 3.1.13 on 2022-01-09 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tralard', '0026_merge_20220109_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Birth Date')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender'), ('Other', 'Other')], max_length=100, null=True, verbose_name='Gender')),
                ('about_me', models.CharField(blank=True, max_length=300, null=True, verbose_name='About Me')),
                ('profile_photo', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='profile_photo')),
                ('cell', models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone Number')),
                ('address', models.CharField(blank=True, max_length=300, null=True, verbose_name='Address')),
                ('postal_code', models.CharField(blank=True, max_length=100, null=True, verbose_name='Postal Code')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tralard.district')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
    ]