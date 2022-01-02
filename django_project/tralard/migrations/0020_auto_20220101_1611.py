# Generated by Django 3.1.13 on 2022-01-01 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tralard', '0019_auto_20220101_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='representative',
            name='ward',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='tralard.ward'),
        ),
        migrations.AlterField(
            model_name='subproject',
            name='description',
            field=models.TextField(blank=True, help_text='A detailed summary of the Sub Project. Rich text edditing is supported.', max_length=2000, null=True),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Create Date')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('moderator', models.ForeignKey(blank=True, help_text='Feedback Moderator. This name will be used on project feedback and any other references. ', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='feedback_moderator', to='tralard.representative')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tralard.project')),
            ],
        ),
    ]
