# Generated by Django 3.2.9 on 2021-12-02 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_image_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
