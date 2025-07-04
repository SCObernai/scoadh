# Generated by Django 5.2.1 on 2025-07-05 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hab', '0003_rename_type_habilite_domainehabilete_type_habilete'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemenotation',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='domainehabilete',
            name='type_habilete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='domaines_habiletes', to='hab.typehabilete', verbose_name="Type d'habileté"),
        ),
    ]
