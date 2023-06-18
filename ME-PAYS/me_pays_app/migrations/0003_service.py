# Generated by Django 4.2 on 2023-06-16 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('me_pays_app', '0002_initialize_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('is_active', models.BooleanField(default=True, null=True)),
            ],
        ),
    ]