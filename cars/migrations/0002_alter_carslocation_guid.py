# Generated by Django 4.1.5 on 2023-04-16 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carslocation',
            name='guid',
            field=models.CharField(max_length=255),
        ),
    ]