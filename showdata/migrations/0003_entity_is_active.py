# Generated by Django 4.0.3 on 2022-04-15 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showdata', '0002_remove_tempdata_trialnumber_entity_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
