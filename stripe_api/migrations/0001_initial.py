# Generated by Django 3.0.2 on 2020-01-24 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance_transaction', models.IntegerField(blank=True, null=True)),
                ('charge_id', models.CharField(blank=True, max_length=255, null=True)),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
                ('date_backed', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
    ]
