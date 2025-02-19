# Generated by Django 4.2.16 on 2025-01-02 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0002_historicalreport_description_report_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalreport',
            name='lead_validation',
            field=models.CharField(choices=[('Valid', 'Valid Lead'), ('Filtered', 'Filtered Lead'), ('Duplicated', 'Duplicated Lead')], default='Valid', max_length=20, verbose_name='Lead Validity'),
        ),
        migrations.AlterField(
            model_name='report',
            name='lead_validation',
            field=models.CharField(choices=[('Valid', 'Valid Lead'), ('Filtered', 'Filtered Lead'), ('Duplicated', 'Duplicated Lead')], default='Valid', max_length=20, verbose_name='Lead Validity'),
        ),
    ]
