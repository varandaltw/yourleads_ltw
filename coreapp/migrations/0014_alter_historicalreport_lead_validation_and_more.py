# Generated by Django 4.2.16 on 2025-01-13 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0013_alter_historicalreport_lead_validation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalreport',
            name='lead_validation',
            field=models.CharField(choices=[('Valid', 'Valid'), ('Filtered', 'Filtered'), ('Duplicated', 'Duplicated'), ('Filtered,Duplicated', 'Filtered and Duplicated')], default='Valid', max_length=50, verbose_name='Lead Validation'),
        ),
        migrations.AlterField(
            model_name='report',
            name='lead_validation',
            field=models.CharField(choices=[('Valid', 'Valid'), ('Filtered', 'Filtered'), ('Duplicated', 'Duplicated'), ('Filtered,Duplicated', 'Filtered and Duplicated')], default='Valid', max_length=50, verbose_name='Lead Validation'),
        ),
    ]
