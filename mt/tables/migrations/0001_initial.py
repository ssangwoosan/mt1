# Generated by Django 4.2.19 on 2025-03-04 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('seats', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
    ]
