# Generated by Django 5.0 on 2024-01-12 06:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0008_book_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="price",
            field=models.FloatField(default=500.0),
        ),
    ]