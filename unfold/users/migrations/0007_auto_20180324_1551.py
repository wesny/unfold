# Generated by Django 2.0.2 on 2018-03-24 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_user_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
