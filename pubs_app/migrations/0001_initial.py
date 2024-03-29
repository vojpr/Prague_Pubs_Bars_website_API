# Generated by Django 4.1.4 on 2022-12-07 00:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PubsBars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('map_url', models.URLField()),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('beer_rating', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('outside_tables', models.BooleanField(blank=True, null=True)),
                ('foosball', models.BooleanField(blank=True, null=True)),
                ('overall_rating', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
            ],
        ),
    ]
