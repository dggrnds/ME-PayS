# Generated by Django 4.2 on 2023-06-18 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('me_pays_app', '0009_alter_order_enduser'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]