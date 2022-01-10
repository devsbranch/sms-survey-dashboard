# Generated by Django 3.1.13 on 2022-01-10 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tralard', '0026_merge_20220109_2226'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='subproject',
        #     name='subproject_managers',
        # ),
        # migrations.RemoveField(
        #     model_name='subproject',
        #     name='supervisor',
        # ),
        migrations.AddField(
            model_name='subproject',
            name='managers',
            field=models.ManyToManyField(blank=True, help_text='Managers of all trainings and project activities in this Sub project. They will be allowed to create or delete subproject data.', related_name='subproject_managers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subproject',
            name='representative',
            field=models.ForeignKey(blank=True, help_text='Sub Project Supervisor. This name will be used on trainings and any other references. ', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='moderator',
            field=models.ForeignKey(blank=True, help_text='Feedback Moderator. This name will be used on project feedback and any other references. ', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='feedback_moderator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='program',
            name='program_representative',
            field=models.ForeignKey(blank=True, help_text='Program representative. This name will be used on programs and any other references. ', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='program_representatives', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_representative',
            field=models.ForeignKey(blank=True, help_text='Project representative. This name will be used on trainings and any other references. ', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='training',
            name='moderator',
            field=models.ForeignKey(blank=True, help_text='Training Moderator. This is the person supervising and or conducting the training, the name will be used on trainings and any other references. ', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Representative',
        ),
    ]
