# Generated by Django 2.2 on 2022-01-19 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tralard', '0032_auto_20220113_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='approval_status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED'), ('CANCELLED', 'CANCELLED')], default='PENDING', help_text='Precise funding status on project fund has been approved for use yet.', max_length=20),
        ),
        migrations.AddField(
            model_name='fund',
            name='approval_status_comment',
            field=models.TextField(blank=True, help_text='Comment on the approval status of the project fund.', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='fund',
            name='approved_by',
            field=models.ForeignKey(blank=True, help_text='The user who approved the fund.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fund',
            name='approved_date',
            field=models.DateField(blank=True, help_text='The date the fund was approved.', null=True, verbose_name='Approved Date'),
        ),
        migrations.AddField(
            model_name='fund',
            name='requested_by',
            field=models.ForeignKey(blank=True, help_text='The user who requested the fund.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='requested_by', to=settings.AUTH_USER_MODEL),
        ),
    ]