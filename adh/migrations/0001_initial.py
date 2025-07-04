# Generated by Django 5.2.1 on 2025-07-05 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adhesion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_adhesion', models.DateField()),
            ],
            options={
                'verbose_name': 'Adhésion au club',
                'verbose_name_plural': 'Adhésions aux club',
            },
        ),
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=150, unique=True)),
                ('bosses', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_naissance', models.CharField(max_length=150, verbose_name='Nom de naissance')),
                ('nom_usage', models.CharField(blank=True, max_length=150, null=True, verbose_name="Nom d'usage")),
                ('prenoms_naissance', models.CharField(max_length=250, verbose_name='Prénoms de naissance')),
                ('prenoms_usage', models.CharField(blank=True, max_length=250, null=True, verbose_name="Prénoms d'usage")),
                ('date_naissance', models.DateField(verbose_name='Date de naissance')),
                ('email', models.EmailField(blank=True, max_length=150, null=True, unique=True)),
                ('tgram', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('whatsapp', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('discord', models.CharField(blank=True, max_length=150, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeMembre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Type de membre',
                'verbose_name_plural': 'Types de membres',
            },
        ),
    ]
