# Generated by Django 4.2.16 on 2025-01-03 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0008_alter_historicalreport_lead_validation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalreport',
            name='city',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='company_name',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Company Name'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='course_name',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='district',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='District'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='energy_supplier',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Energy Supplier'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='has_credit_card',
            field=models.BooleanField(db_index=True, null=True, verbose_name='Has Credit Card?'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='has_debt',
            field=models.BooleanField(db_index=True, null=True, verbose_name='Has Debt?'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='holder_status_1',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='First Holder Status'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='holder_status_2',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Second Holder Status'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='housing',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='House Type'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='interest_rate',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=5, null=True, verbose_name='Interest Rate'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='is_interested',
            field=models.BooleanField(db_index=True, null=True, verbose_name='Is Interested?'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='is_owner',
            field=models.BooleanField(db_index=True, null=True, verbose_name='Is Owner?'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='language',
            field=models.CharField(choices=[('EN', 'English'), ('ES', 'Spanish'), ('FR', 'French'), ('DE', 'German'), ('NL', 'Dutch'), ('PT', 'Portuguese'), ('PL', 'Polish'), ('UA', 'Ukrainian'), ('LT', 'Lithuanian')], max_length=2, null=True, verbose_name='LP Language'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='marital_status',
            field=models.CharField(choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')], db_index=True, max_length=20, null=True, verbose_name='Marital Status'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='mortgage_value',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=12, null=True, verbose_name='Mortgage Amount'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='nationality',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Nationality'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='on_time_payments',
            field=models.BooleanField(db_index=True, null=True, verbose_name='Pays On Time?'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='product',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='utm_assignment',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Utm Assignment'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='utm_campaign',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Utm Campaign'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='utm_content',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Utm Content'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='utm_medium',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Utm Medium'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='utm_source',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Utm Source'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='utm_term',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Utm Term'),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='vehicle_type',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Vehicle Type'),
        ),
        migrations.AlterField(
            model_name='report',
            name='city',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='report',
            name='company_name',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Company Name'),
        ),
        migrations.AlterField(
            model_name='report',
            name='course_name',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='report',
            name='district',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='District'),
        ),
        migrations.AlterField(
            model_name='report',
            name='energy_supplier',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Energy Supplier'),
        ),
        migrations.AlterField(
            model_name='report',
            name='has_credit_card',
            field=models.BooleanField(db_index=True, null=True, verbose_name='Has Credit Card?'),
        ),
        migrations.AlterField(
            model_name='report',
            name='has_debt',
            field=models.BooleanField(db_index=True, null=True, verbose_name='Has Debt?'),
        ),
        migrations.AlterField(
            model_name='report',
            name='holder_status_1',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='First Holder Status'),
        ),
        migrations.AlterField(
            model_name='report',
            name='holder_status_2',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Second Holder Status'),
        ),
        migrations.AlterField(
            model_name='report',
            name='housing',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='House Type'),
        ),
        migrations.AlterField(
            model_name='report',
            name='interest_rate',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=5, null=True, verbose_name='Interest Rate'),
        ),
        migrations.AlterField(
            model_name='report',
            name='is_interested',
            field=models.BooleanField(db_index=True, null=True, verbose_name='Is Interested?'),
        ),
        migrations.AlterField(
            model_name='report',
            name='is_owner',
            field=models.BooleanField(db_index=True, null=True, verbose_name='Is Owner?'),
        ),
        migrations.AlterField(
            model_name='report',
            name='language',
            field=models.CharField(choices=[('EN', 'English'), ('ES', 'Spanish'), ('FR', 'French'), ('DE', 'German'), ('NL', 'Dutch'), ('PT', 'Portuguese'), ('PL', 'Polish'), ('UA', 'Ukrainian'), ('LT', 'Lithuanian')], max_length=2, null=True, verbose_name='LP Language'),
        ),
        migrations.AlterField(
            model_name='report',
            name='marital_status',
            field=models.CharField(choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')], db_index=True, max_length=20, null=True, verbose_name='Marital Status'),
        ),
        migrations.AlterField(
            model_name='report',
            name='mortgage_value',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=12, null=True, verbose_name='Mortgage Amount'),
        ),
        migrations.AlterField(
            model_name='report',
            name='nationality',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Nationality'),
        ),
        migrations.AlterField(
            model_name='report',
            name='on_time_payments',
            field=models.BooleanField(db_index=True, null=True, verbose_name='Pays On Time?'),
        ),
        migrations.AlterField(
            model_name='report',
            name='product',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='report',
            name='utm_assignment',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Utm Assignment'),
        ),
        migrations.AlterField(
            model_name='report',
            name='utm_campaign',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Utm Campaign'),
        ),
        migrations.AlterField(
            model_name='report',
            name='utm_content',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Utm Content'),
        ),
        migrations.AlterField(
            model_name='report',
            name='utm_medium',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Utm Medium'),
        ),
        migrations.AlterField(
            model_name='report',
            name='utm_source',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Utm Source'),
        ),
        migrations.AlterField(
            model_name='report',
            name='utm_term',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Utm Term'),
        ),
        migrations.AlterField(
            model_name='report',
            name='vehicle_type',
            field=models.CharField(blank=True, db_index=True, max_length=80, null=True, verbose_name='Vehicle Type'),
        ),
    ]
