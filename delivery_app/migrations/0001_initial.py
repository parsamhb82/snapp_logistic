# Generated by Django 5.1 on 2024-08-16 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('wallet', models.FloatField()),
                ('courier_status', models.IntegerField()),
                ('plate', models.CharField(max_length=8)),
                ('courier_phone_number', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=7)),
                ('delivery_status', models.IntegerField()),
                ('max_delivery_time', models.CharField(max_length=120)),
                ('delivery_price', models.FloatField()),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='delivery_app.courier')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_destiation', to='delivery_app.location')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_origin', to='delivery_app.location')),
            ],
        ),
    ]
