# Generated by Django 5.2.1 on 2025-07-05 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('act', '0002_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='varianteactivite',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('date_debut__isnull', True), ('date_fin__isnull', True), ('date_fin__gte', models.F('date_debut')), _connector='OR')), name='check_dates_variantes_deb_fin'),
        ),
    ]
