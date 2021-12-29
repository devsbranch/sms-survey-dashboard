# Generated by Django 3.1.13 on 2021-12-29 11:52

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dj_beneficiary', '0001_initial'),
        ('tralard', '0006_auto_20211229_0343'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='is_comppleted',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Organization Name')),
                ('org_type', models.CharField(choices=[('coorperative', 'Co-orperative'), ('businessfirm', 'Business Firm'), ('Other', 'Other')], max_length=100, verbose_name='Organization Type')),
                ('logo', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='org_logos')),
                ('total_beneficiaries', models.IntegerField(blank=True, null=True, verbose_name='Total Individual Beneficiary Count')),
                ('total_females', models.IntegerField(blank=True, null=True, verbose_name='Total Female Count')),
                ('total_males', models.IntegerField(blank=True, null=True, verbose_name='Total Male Count')),
                ('total_hhs', models.IntegerField(blank=True, null=True, verbose_name='Total HHs')),
                ('female_hhs', models.IntegerField(blank=True, null=True, verbose_name='Female HHs')),
                ('below_sixteen', models.IntegerField(blank=True, null=True, verbose_name='Below 16 Years Old')),
                ('sixteen_to_thirty', models.IntegerField(blank=True, null=True, verbose_name='16 to 30 Years Old')),
                ('thirty_to_fourty_five', models.IntegerField(blank=True, null=True, verbose_name='30 to 40 Years Old')),
                ('above_fourty_five', models.IntegerField(blank=True, null=True, verbose_name='Above 40 Years Old')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('email', models.EmailField(blank=True, max_length=200, null=True, verbose_name='Email')),
                ('cell', models.CharField(blank=True, max_length=100, null=True, verbose_name='Phone Number')),
                ('registered_date', models.DateField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sub_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tralard.subproject')),
                ('ward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dj_beneficiary.ward')),
            ],
            options={
                'verbose_name': 'PPCR Beneficiary',
                'verbose_name_plural': 'PPCR Beneficiaries',
                'abstract': False,
            },
        ),
    ]
