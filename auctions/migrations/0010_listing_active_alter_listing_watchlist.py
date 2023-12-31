# Generated by Django 4.2.5 on 2023-09-30 15:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0009_remove_user_watchlist_listing_watchlist_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="active",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="listing",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="multiple_reference",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
