# Generated by Django 3.1.2 on 2020-12-23 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='creator',
            field=models.CharField(default='creator', max_length=64),
        ),
    ]