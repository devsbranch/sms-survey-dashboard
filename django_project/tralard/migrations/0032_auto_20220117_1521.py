# Generated by Django 3.1.13 on 2022-01-17 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tralard', '0031_auto_20220113_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subproject',
            name='district',
        ),
        migrations.AddField(
            model_name='project',
            name='project_status',
            field=models.CharField(blank=True, choices=[('Identified', 'Identified'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=50, null=True, verbose_name='Project Status'),
        ),
        migrations.AddField(
            model_name='subproject',
            name='sub_project_status',
            field=models.CharField(blank=True, choices=[('Identified', 'Identified'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=50, null=True, verbose_name='Project Status'),
        ),
        migrations.AddField(
            model_name='subproject',
            name='ward',
            field=models.ForeignKey(blank=True, help_text='The ward in which this subproject has been implemented.', null=True, on_delete=django.db.models.deletion.CASCADE, to='tralard.ward'),
        ),
    ]