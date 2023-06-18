# Generated by Django 4.2 on 2023-06-16 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('me_pays_app', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='reference_number',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='order',
            name='school_id',
            field=models.IntegerField(null=True),
        ),
    ]
