# Generated by Django 2.2.16 on 2022-01-31 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tralard', '0041_merge_20220128_0055'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndicatorUnitOfMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_of_measure', models.CharField(blank=True, max_length=200, null=True, verbose_name='Unit of Measure')),
                ('data_source', models.CharField(choices=[('size', 'Sub Project Size'), ('total_beneficiaries', 'Total Beneficiaries'), ('total_females', 'Total Beneficiary Female Count'), ('total_males', 'Total Beneficiary Male Count'), ('total_hhs', 'Total HHS'), ('female_hhs', 'Female HHS'), ('expenditure_amount', 'Expenditure Amount')], max_length=200, verbose_name='Source of data')),
            ],
        ),
        migrations.RemoveField(
            model_name='indicatortargetvalue',
            name='actual_value',
        ),
        migrations.AlterField(
            model_name='indicatortarget',
            name='unit_of_measure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tralard.IndicatorUnitOfMeasure'),
        ),
    ]