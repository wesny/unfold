# Generated by Django 2.0.2 on 2018-03-18 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_auto_20180318_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
