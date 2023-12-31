# Generated by Django 4.2.5 on 2023-09-26 12:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0002_listing_listingdetails"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listingdetails",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("1", "Fashion"),
                    ("2", "Home"),
                    ("3", "Toys"),
                    ("4", "Electronics"),
                    ("5", "Books"),
                    ("6", "Misc"),
                ],
                max_length=50,
            ),
        ),
    ]
