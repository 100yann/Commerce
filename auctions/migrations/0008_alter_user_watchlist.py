# Generated by Django 4.2.5 on 2023-09-29 14:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0007_alter_user_watchlist"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="watchlist",
            field=models.TextField(blank=True, null=True),
        ),
    ]
