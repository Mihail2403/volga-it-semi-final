# Generated by Django 4.2.6 on 2023-10-21 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0003_renttype_rent_renttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='finalPrice',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
